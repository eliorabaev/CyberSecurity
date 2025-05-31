# Internet Service Provider Management System (Communication_LTD)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.2.0-green.svg)
![Python](https://img.shields.io/badge/python-3.9-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-teal.svg)
![React](https://img.shields.io/badge/react-19.0.0-61DAFB.svg?logo=react&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg?logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg?logo=docker&logoColor=white)
![Security](https://img.shields.io/badge/security-enhanced-brightgreen.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTEyIDEyaDdjLS41IDQuMS0zLjMgNy44LTcgOXYtOXptLTEgOUM3LjMgMTkuOCA0LjUgMTYuMSA0IDEyaDd2OXptLTctOWMuNS00LjEgMy4zLTcuOCA3LTlWM2g2djFjMy43IDEuMiA2LjUgNC45IDcgOUgxOGgtMkg0eiIvPjwvc3ZnPg==)
![Maintenance](https://img.shields.io/badge/maintained-yes-brightgreen.svg)
![PBKDF2](https://img.shields.io/badge/PBKDF2-1,200,000%20iterations-red.svg)
![JWT](https://img.shields.io/badge/JWT-authentication-yellow.svg)
![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

A secure web application for managing Internet service customers, featuring robust user authentication and comprehensive security measures.

## ⚡ Quick Start

```bash
# Clone the repository
git clone https://github.com/eliorabaev/CyberSecurity.git && cd CyberSecurity

# Start the backend (Docker required)
cd backend && cp .env.example .env

# Update Web3Forms API key in .env file (required for password reset)
# Replace "your_actual_api_key_here" with the API key from https://web3forms.com
sed -i 's/enter_your_api_key_here/your_actual_api_key_here/' .env

# Start backend services (remove any volumes and rebuild the images - in case you are coming from the vulnerable version)
docker compose down -v && docker compose up --build -d

# Start the frontend
cd ../frontend && cp .env.example .env && npm install && npm start
```

Default admin credentials: `admin` / `uO?{q312?5` (change immediately after first login)

[➡️ Jump to Project Requirements](#appendix-project-requirements)

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Security Implementation Details](#security-implementation-details)
- [Setup Guide](#setup-guide)
- [Authentication & Password Management](#authentication--password-management)
- [API Documentation](#api-documentation)
- [Data Validation](#data-validation)
- [License](#license)
- [Appendix: Project Requirements](#appendix-project-requirements)

## Overview

This system provides a secure, user-friendly interface for managing Internet Service Provider (ISP) customers. Built with security best practices at every level, it implements a layered defense approach to protect sensitive customer data while maintaining a smooth user experience.

## Key Features

- 🔐 **Enterprise-Grade Authentication**
  - User registration with email validation [Part 1a, 1d]
  - Complex password requirements managed through configuration [Part 1b]
  - PBKDF2-HMAC-SHA256 password hashing (1,200,000 iterations) with database-stored salt [Part 1c]
  - Multi-level account security with both username and IP-based lockouts [Config item 5]
  - Three-step forgot password flow using SHA-1 for verification codes [Part 5]
  - Password history checking to prevent reuse of last 3 passwords [Config item 3]
  - Dictionary-based password blacklist [Config item 4]

  **Security Proof Points:**
  - Salt is cryptographically generated and centrally stored to prevent rainbow table attacks
  - Iteration count of 1,200,000 exceeds NIST recommendations for protection against brute force
  - Login flow incorporates multiple layers of security checks to prevent account enumeration
  - Password reset tokens are time-limited and single-use to prevent replay attacks

- 🔒 **Comprehensive Security Measures**
  - Defense against XSS through automatic HTML escaping of user input [Part B.1]
  - SQL Injection protection using parameterized queries and ORM [Part B.2]
  - Proper input validation and sanitization throughout
  - Content Security Policy implementation

  **Security Proof Points:**
  - All user-generated content passes through HTML escaping functions before display
  - SQLAlchemy ORM with prepared statements prevents SQL injection by design
  - Custom `sanitize_string()` function ensures proper encoding of special characters
  - Pydantic validation models enforce strict typing and constraints

- 👥 **Customer Management**
  - Add new customers with validated information [Part 4a]
  - View customers with secure data presentation [Part 4b]
  - Input validation to prevent malicious data entry

  **Security Proof Points:**
  - Customer data is sanitized at both input and output stages
  - Strict validation rules prevent insertion of malicious or malformed data
  - React's built-in XSS protections provide additional frontend security layer

## Technology Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **Pydantic**: Data validation and settings management
- **PyJWT**: JSON Web Token implementation
- **MySQL**: Relational database system

### Frontend
- **React**: UI library with Context API for state management
- **HTML5/CSS3**: Modern layout and styling
- **Fetch API**: Network requests to backend services

### Infrastructure
- **Docker & Docker Compose**: Containerization and orchestration

## Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│                 │      │                  │      │                  │
│ React Frontend  │◄────►│ FastAPI Backend  │◄────►│  MySQL Database  │
│                 │      │                  │      │                  │
└─────────────────┘      └──────────────────┘      └──────────────────┘
       ▲                         ▲                        ▲
       │                         │                        │
       │                         │                        │
       │     ┌──────────────┐    │                        │
       └────►│   JWT Auth   │◄───┘                        │
             │              │                             │
             └──────────────┘                             │
                                    ┌──────────────────┐  │
                                    │   Secure Salt &  │◄─┘
                                    │   JWT Secrets    │
                                    └──────────────────┘
```

## Security Implementation Details

### Password Hashing Implementation [Part 1c]

Our solution implements state-of-the-art password security:

1. **Salt Generation & Storage**:
   - A 32-byte (256-bit) cryptographically secure random salt is generated at first application startup
   - Salt is stored in a dedicated `secrets` table in the database with ID "main"
   - Centralized salt storage ensures consistent hashing across application instances
   - This approach prevents rainbow table attacks while maintaining consistent verification

2. **Password Hashing Algorithm**:
   - PBKDF2-HMAC-SHA256 with 1,200,000 iterations (significantly exceeding NIST SP 800-63B recommendations)
   - 32-byte (256-bit) derived key length for maximum security
   - Base64 encoding for database storage
   - Implementation in `password_utils.py` using the cryptography library

3. **Verification Process**:
   - Constant-time comparison to prevent timing attacks
   - Same salt and parameters ensure consistent verification
   - Secure error handling that doesn't leak information

### Multi-Layered Brute Force Protection [Config item 5]

The system implements a sophisticated approach to brute force attack prevention:

1. **Per-User Account Protection**:
   - Tracks failed login attempts per username in `AccountStatus` table
   - Locks account after 3 failed attempts (configurable)
   - 30-minute lockout duration prevents targeted attacks
   - Counter reset on successful authentication

2. **IP-Based Protection**:
   - Tracks failed login attempts by IP address in `LoginAttempt` table
   - Implements IP lockout after 10 failed attempts (configurable)
   - Uses a sliding 24-hour window approach for attempt counting
   - 60-minute lockout duration provides strong protection
   - Prevents distributed attacks across multiple accounts

3. **Progressive Security Logic**:
   - Initial check verifies if IP is already locked
   - Secondary check for account-level lockout status
   - Prioritizes most restrictive policy
   - Comprehensive logging of all authentication attempts 
   - Records timestamps, IP addresses, and success/failure status

### XSS and SQL Injection Protection [Part B.1, B.2]

The system implements multiple layers of defense against common web vulnerabilities:

1. **Cross-Site Scripting (XSS) Prevention**:
   - **HTML Escaping**: All user-generated content is automatically escaped
   - **Custom Sanitization**: `sanitize_string()` function in `main.py` encodes special characters
   - **Validated Outputs**: Pydantic models use custom validators to sanitize response data
   - **React Protection**: Inherent XSS protection in React's rendering engine
   - **Implementation Example**:
     ```python
     def sanitize_string(value: str) -> str:
         """Escape HTML special characters to prevent XSS"""
         if value is None:
             return None
         return html.escape(value)
     ```

2. **SQL Injection Prevention**:
   - **ORM Usage**: SQLAlchemy provides parameterized queries by default
   - **Type Validation**: Pydantic models enforce strict type checking
   - **Prepared Statements**: All database operations use bound parameters
   - **Input Sanitization**: Multiple validation layers before database interaction
   - **Implementation Example**:
     ```python
     @app.post("/customers")
     def add_customer(data: CustomerData, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
         # Pydantic model ensures sanitized, validated data
         new_customer = Customer(
             name=data.name,
             internet_package=data.internet_package,
             sector=data.sector
         )
         db.add(new_customer)  # ORM handles SQL injection protection
         db.commit()
     ```

### JWT Authentication Security

The system implements a robust JSON Web Token (JWT) authentication mechanism:

1. **Secret Key Management**:
   - Secure random JWT secret key generated at first startup
   - 32-byte secret key stored in database `secrets` table with ID "jwt_secret"
   - Consistent authentication across multiple application instances
   - Fallback to environment variable only when database is unavailable

2. **Token Generation & Validation**:
   - HS256 (HMAC with SHA-256) algorithm for signing tokens
   - 1-hour expiration time to limit attack window
   - Username stored as subject claim for user identification
   - Full signature validation on every request
   - Expiration time checking to prevent use of outdated tokens

3. **Implementation Highlights**:
   ```python
   # From auth_utils.py
   def verify_token(token: str, db: Session = None):
       try:
           secret_key = get_or_create_jwt_secret(db)
           payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
           return payload
       except JWTError:
           return None
   ```

### Password Reset Security [Part 5]

The system implements a secure three-step password reset flow:

1. **Email Request (Step 1)**:
   - User submits email address
   - System generates SHA-1 verification code as required by specifications
   - Code stored with 20-minute expiration time in `PasswordResetToken` table
   - Existing tokens for the user are invalidated to prevent confusion

2. **Code Verification (Step 2)**:
   - Backend validates code against stored token
   - Checks for expiration and previous usage
   - Success grants authorization to proceed to password reset

3. **Password Reset (Step 3)**:
   - New password validated against security policy and history
   - History check prevents reuse of previous passwords
   - Token marked as used after successful reset to prevent replay attacks
   - Success confirmed to user

## Setup Guide

### Prerequisites

- **Docker and Docker Compose** (v1.29+)
- **Git**
- **Node.js** (v14+) and **npm** (v6+)
- Modern web browser (Chrome, Firefox, Edge, or Safari)

### Detailed Installation Steps

#### 1. Clone the repository

```bash
git clone https://github.com/eliorabaev/CyberSecurity.git
cd CyberSecurity
```

#### 2. Backend Configuration

```bash
cd backend
cp .env.example .env
```

Edit the `.env` file with secure credentials:

```
# Database Configuration
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=internet_service_provider

# Docker specific variables
DB_ROOT_PASSWORD=your_root_password
DB_PORT=3307
API_PORT=8000

# Frontend URL for CORS
FRONTEND_URL=http://localhost:3000

# Web3Forms API Key
# Replace with your actual Web3Forms API key
# The verification key for password reset will be sent to the mail associated with the API key
# You can get your API key from https://web3forms.com
WEB3FORMS_API_KEY=enter_your_api_key_here
```

> **⚠️ IMPORTANT:** Password reset verification codes will be sent to the email address associated with your Web3Forms account. Make sure you have access to this email.

#### 3. Start the Backend Services

```bash
docker-compose up -d
```

#### 4. Frontend Configuration

```bash
cd ../frontend
cp .env.example .env
```

#### 5. Start the Frontend Development Server

```bash
npm install
npm start
```

#### 6. Access the Application

- **Frontend UI**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

#### 7. Default Administrator Access

- Username: `admin`
- Password: `uO?{q312?5`

**⚠️ CRITICAL SECURITY ACTION**: Change the default admin password immediately after first login.

## Authentication & Password Management

### User Registration and Login [Part 1, Part 3]

The system implements a secure user registration and authentication flow:

1. **Registration Process**:
   - Collects username, email, and password
   - Validates password complexity requirements (10+ chars, upper/lower/number/special)
   - Hashes password with PBKDF2-HMAC-SHA256 (1,200,000 iterations)
   - Creates database record with username, email, and hashed password
   - Adds initial password to password history tracking

2. **Login Process**:
   - Initial check: Is the client's IP address temporarily locked?
   - Secondary check: Is the user account temporarily locked?
   - Validates credentials against database with constant-time comparison
   - Records IP address and timestamp of attempt (success or failure)
   - Increments failure counters on unsuccessful attempts
   - Applies account lockout after 3 failures, IP lockout after 10 failures
   - On success: resets failure counters, issues 1-hour JWT token

3. **Authentication Flow**:
   - JWT token included in Authorization header with each request
   - Backend validates token signature and expiration
   - Username extracted from token and verified against database
   - Request processed only after successful verification

### Password Management [Part 2, Part 5]

1. **Password Change**:
   - Requires current password verification to prevent unauthorized changes
   - Validates new password against:
     - Complexity requirements (10+ chars, mixed case, numbers, special)
     - Password history (last 3 passwords)
     - Common password blacklist
   - Updates stored hash with new PBKDF2 value
   - Adds previous password to history table

2. **Password Reset**:
   - **Step 1**: User requests reset by providing email address
     - System generates SHA-1 verification code
     - Code stored with 20-minute expiration time
     - Code sent via email or shown in console (development mode)
   - **Step 2**: User verifies code to gain reset authorization
     - Backend validates code against stored token
     - Code must be unexpired and unused
   - **Step 3**: User sets new password with verification
     - New password validated against all security policies
     - Password added to history to prevent future reuse
     - Token marked as used to prevent replay attacks

## API Documentation

### Authentication Endpoints

- `POST /login`: User authentication with credentials
- `POST /register`: New user registration
- `POST /forgot-password`: Initiate password reset
- `POST /verify-reset-token`: Verify password reset code
- `POST /reset-password`: Complete password reset
- `GET /me`: Retrieve current user information
- `POST /change-password`: Change password for authenticated user

### Customer Management Endpoints

- `GET /customers`: Retrieve all customers
- `POST /customers`: Add a new customer

See the [API Documentation](http://localhost:8000/docs) for complete details on requests, responses, and error codes.

## Data Validation

The system implements comprehensive validation for all user inputs:

- **Username**: 3-20 characters, letters and numbers only
- **Password**: 10+ characters with uppercase, lowercase, numbers, and special characters
- **Email**: Standard email format validation
- **Customer Name**: Letters and spaces only, 2-100 characters
- **Internet Package**: Must be one of the predefined service options
- **Sector**: Must be one of the predefined geographic sectors

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Appendix: Project Requirements

**Quick Reference:** [User Registration (1a-1d)](#part-a-secure-development-principles) | [Password Change (2a-2b)](#part-a-secure-development-principles) | [Login (3a-3c)](#part-a-secure-development-principles) | [Interface (4a-4b)](#part-a-secure-development-principles) | [Password Reset (5a-5d)](#part-a-secure-development-principles) | [XSS/SQLi Protection (B.1-B.2)](#part-b-protection-against-xss-and-sqli) | [Config Requirements (1-5)](#configuration-file-requirements)

This project was developed as a Cybersecurity final project implementing the following requirements:

### Part A: Secure Development Principles

1. **User Registration**
   - User definition (Part 1a)
   - Complex password requirements (Part 1b)
   - PBKDF2+Salt password storage (Part 1c)
   - Email collection (Part 1d)

2. **Password Change**
   - Current password verification (Part 2a)
   - New password validation (Part 2b)

3. **Login System**
   - Username input (Part 3a)
   - Password input (Part 3b)
   - Appropriate user verification and responses (Part 3c)

4. **System Interface**
   - New customer creation (Part 4a)
   - Customer data display (Part 4b)

5. **Password Reset**
   - Forgot password flow (Part 5a)
   - Random value email delivery (Part 5b)
   - SHA-1 value generation (Part 5c)
   - Verification code validation (Part 5d)

### Part B: Protection Against XSS and SQLi

1. Special character encoding to prevent XSS (Part B.1)
2. Parameterized queries and stored procedures for SQLi protection (Part B.2)

### Configuration File Requirements

1. Password length: 10 characters minimum
2. Password complexity: uppercase, lowercase, numbers, special characters
3. Password history: last 3 passwords
4. Dictionary-based prevention
5. Login attempt limiting: 3 attempts

[⬆️ Back to Quick Start](#-quick-start)
