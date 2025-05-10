from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from typing import Optional, List
import html
import password_config as config
from datetime import datetime, timedelta
from models import PasswordResetToken

# Import from our new modules
from database import engine, get_db, Base
from models import User, Customer, Secret, PasswordHistory, LoginAttempt, AccountStatus
from password_utils import hash_password, verify_password, get_or_create_salt
from auth_utils import create_access_token, verify_token, get_or_create_jwt_secret
from email_utils import generate_reset_token, send_password_reset_email 
from validation_utils import (
    validate_username, 
    validate_password, 
    validate_email, 
    validate_customer_name,
    validate_internet_package,
    validate_sector
)
from security_utils import (
    record_login_attempt, 
    get_recent_failed_attempts, 
    is_account_locked, 
    increment_failed_attempts, 
    reset_failed_attempts,
    add_password_to_history,
    is_ip_locked
)

from sqlalchemy.orm import Session

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI()

# Allow requests from the React app
origins = [os.getenv("FRONTEND_URL", "http://localhost:3000")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Helper function to sanitize strings
def sanitize_string(value: str) -> str:
    """Escape HTML special characters to prevent XSS"""
    if value is None:
        return None
    return html.escape(value)

# Get current user from token
async def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(
            status_code=401, 
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    scheme, token = authorization.split()
    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401, 
            detail="Invalid authentication scheme",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    payload = verify_token(token, db=db)
    if payload is None:
        raise HTTPException(
            status_code=401, 
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=401, 
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user

# Pydantic models for request/response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class LoginData(BaseModel):
    username: str
    password: str

class RegisterData(BaseModel):
    username: str
    email: str
    password: str

class ChangePasswordData(BaseModel):
    oldPassword: str
    newPassword: str

class CustomerData(BaseModel):
    name: str
    internet_package: str
    sector: str

class UserResponse(BaseModel):
    username: str
    email: str
    
    # Sanitize data to prevent XSS
    @validator('username', 'email')
    def sanitize_fields(cls, v):
        return sanitize_string(v)
    
    class Config:
        from_attributes = True  # Updated from orm_mode = True

class CustomerResponse(BaseModel):
    id: int
    name: str
    internet_package: str
    sector: str
    date_added: str  # Use string instead of date type
    
    # Sanitize data to prevent XSS
    @validator('name', 'internet_package', 'sector')
    def sanitize_fields(cls, v):
        return sanitize_string(v)
    
    class Config:
        from_attributes = True  # Updated from orm_mode = True

class CustomerListResponse(BaseModel):
    customers: List[CustomerResponse]

class MessageResponse(BaseModel):
    message: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    token: str
    new_password: str

class VerifyTokenRequest(BaseModel):
    email: str
    token: str

# User endpoints
@app.post("/login", response_model=TokenResponse)
def login(data: LoginData, request: Request, db: Session = Depends(get_db)):
    if not data.username or not data.password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    # Get user's IP address for logging
    client_ip = request.client.host if request.client else "unknown"
    
    # FIRST: Check if IP is locked due to too many failed attempts
    is_locked_ip, lock_message_ip = is_ip_locked(client_ip, db)
    if is_locked_ip:
        # Record the attempt
        record_login_attempt(data.username, False, client_ip, db)
        raise HTTPException(status_code=429, detail=lock_message_ip)
    
    # Check if username exists
    user = db.query(User).filter(User.username == data.username).first()
    
    # Check max login attempts for this username
    recent_attempts = get_recent_failed_attempts(data.username, db)
    if recent_attempts >= config.MAX_LOGIN_ATTEMPTS:
        # Record the attempt
        record_login_attempt(data.username, False, client_ip, db)
        raise HTTPException(status_code=429, detail="Too many failed login attempts. Try again later.")
    
    # Check if user exists
    if not user:
        # Record failed attempt
        record_login_attempt(data.username, False, client_ip, db)
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Check if account is locked
    is_locked, lock_message = is_account_locked(user.id, db)
    if is_locked:
        # Record the attempt
        record_login_attempt(data.username, False, client_ip, db)
        raise HTTPException(status_code=423, detail=lock_message)
    
    # Verify password
    if not verify_password(data.password, user.password, db):
        # Record failed attempt and increment counter
        record_login_attempt(data.username, False, client_ip, db)
        increment_failed_attempts(user.id, db)
        
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Login successful - reset failed attempts and record success
    record_login_attempt(data.username, True, client_ip, db)
    reset_failed_attempts(user.id, db)
    
    # Create access token with username as subject
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=60),  # Token valid for 1 hour
        db=db
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=MessageResponse)
def register(data: RegisterData, db: Session = Depends(get_db)):
    # Validate username
    is_valid, error_message = validate_username(data.username)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    # Validate email
    is_valid, error_message = validate_email(data.email)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    # Validate password
    is_valid, error_message = validate_password(data.password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    # Check if username or email already exists
    existing_user = db.query(User).filter(
        (User.username == data.username) | (User.email == data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Create new user with hashed password
    hashed_password = hash_password(data.password, db)
    new_user = User(username=data.username, email=data.email, password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Add the password to history
    add_password_to_history(new_user.id, hashed_password, db)
    
    return {"message": "Registration successful"}

@app.post("/forgot-password", response_model=MessageResponse)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Initiate password reset process by sending a reset token via email"""
    # Validate email
    is_valid, error_message = validate_email(data.email)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    # Find user by email
    user = db.query(User).filter(User.email == data.email).first()
    
    # Don't reveal if email exists or not for security
    # Still generate and store a token even if user doesn't exist to prevent timing attacks
    reset_token = generate_reset_token()
    
    if user:
        # Expire any existing unused tokens for this user
        existing_tokens = db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.is_used == False,
            PasswordResetToken.expires_at > datetime.now()
        ).all()
        
        for token in existing_tokens:
            token.is_used = True
        
        # Create token with 20-minute expiration
        token_expiry = datetime.now() + timedelta(minutes=20)
        new_token = PasswordResetToken(
            user_id=user.id,
            email=data.email,
            token=reset_token,
            expires_at=token_expiry
        )
        
        db.add(new_token)
        db.commit()
        
        # Send email with token
        send_password_reset_email(data.email, reset_token)
    
    # Always return the same message for security (don't indicate if email exists)
    return {"message": "If an account with this email exists, a password reset link has been sent."}

@app.post("/reset-password", response_model=MessageResponse)
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password using the token sent via email"""
    # Find the token
    token_record = db.query(PasswordResetToken).filter(
        PasswordResetToken.email == data.email,
        PasswordResetToken.token == data.token,
        PasswordResetToken.is_used == False,
        PasswordResetToken.expires_at > datetime.now()
    ).first()
    
    if not token_record:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    # Find the user associated with this token
    user = db.query(User).filter(User.id == token_record.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Validate the new password, including history check
    is_valid, error_message = validate_password(data.new_password, user.id, db)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    # Hash the new password
    hashed_password = hash_password(data.new_password, db)
    
    # Update user's password
    user.password = hashed_password
    
    # Mark token as used
    token_record.is_used = True
    
    # Add the new password to history
    add_password_to_history(user.id, hashed_password, db)
    
    db.commit()
    
    return {"message": "Password has been reset successfully"}

@app.post("/change-password", response_model=MessageResponse)
def change_password(data: ChangePasswordData, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Validate old password exists
    if not data.oldPassword:
        raise HTTPException(status_code=400, detail="Current password is required")
    
    # Validate new password with history check
    is_valid, error_message = validate_password(data.newPassword, current_user.id, db)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    # Verify the old password matches the user's current password
    if not verify_password(data.oldPassword, current_user.password, db):
        raise HTTPException(status_code=401, detail="Invalid current password")
    
    # Update password with new hash
    new_hashed_password = hash_password(data.newPassword, db)
    current_user.password = new_hashed_password
    db.commit()
    
    # Add the new password to history
    add_password_to_history(current_user.id, new_hashed_password, db)
    
    return {"message": "Password changed successfully"}

@app.post("/verify-reset-token", response_model=MessageResponse)
def verify_reset_token(data: VerifyTokenRequest, db: Session = Depends(get_db)):
    """Verify a password reset token before allowing password change"""
    # Find the token
    token_record = db.query(PasswordResetToken).filter(
        PasswordResetToken.email == data.email,
        PasswordResetToken.token == data.token,
        PasswordResetToken.is_used == False,
        PasswordResetToken.expires_at > datetime.now()
    ).first()
    
    if not token_record:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")
    
    # Find the user associated with this token
    user = db.query(User).filter(User.id == token_record.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Do not mark token as used yet - it will be marked when password is reset
    
    return {"message": "Verification code is valid. Please set a new password."}


# Customer endpoints (protected by authentication)
@app.post("/customers", response_model=MessageResponse)
def add_customer(data: CustomerData, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Validate customer name
    is_valid, error_message = validate_customer_name(data.name)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    # Validate internet package
    is_valid, error_message = validate_internet_package(data.internet_package)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    # Validate sector
    is_valid, error_message = validate_sector(data.sector)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    # Create new customer
    new_customer = Customer(
        name=data.name,
        internet_package=data.internet_package,
        sector=data.sector
    )
    
    db.add(new_customer)
    db.commit()
    
    return {"message": "Customer added successfully"}

@app.get("/customers", response_model=CustomerListResponse)
def get_customers(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    
    # Convert to Pydantic models to leverage automatic validation and sanitization
    customer_responses = []
    for customer in customers:
        customer_responses.append(CustomerResponse(
            id=customer.id,
            name=customer.name,
            internet_package=customer.internet_package,
            sector=customer.sector,
            date_added=customer.date_added.strftime("%Y-%m-%d")
        ))
    
    # Return in format matching CustomerListResponse
    return {"customers": customer_responses}

# Endpoint to get current user info
@app.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

# Initialize salt on application startup
@app.on_event("startup")
def initialize_application():
    db = next(get_db())
    try:
        # Initialize salt if it doesn't exist
        get_or_create_salt(db)
        
        # Initialize JWT secret if it doesn't exist
        get_or_create_jwt_secret(db)
        
        # Create admin user if it doesn't exist
        admin_exists = db.query(User).filter(User.username == "admin").first()
        if not admin_exists:
            # Create admin with hashed password
            hashed_password = hash_password("uO?{q312?5", db)
            admin_user = User(
                username="admin",
                email="admin@example.com",
                password=hashed_password
            )
            db.add(admin_user)
            db.commit()
            print("Created admin user with secure password")
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)