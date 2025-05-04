# Internet Service Provider Management System

A secure web application for managing internet service customers with a FastAPI backend and React frontend, featuring robust user authentication and session management.

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

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture Diagram](#architecture-diagram)
- [Detailed Project Structure](#detailed-project-structure)
- [Technology Stack](#technology-stack)
  - [Backend](#backend)
  - [Frontend](#frontend)
  - [Database](#database)
  - [Infrastructure](#infrastructure)
- [Enhanced Security Features](#enhanced-security-features)
  - [Advanced Authentication Protection](#advanced-authentication-protection)
  - [Centralized Security Configuration](#centralized-security-configuration)
- [Detailed Security Implementation](#detailed-security-implementation)
  - [Authentication Security](#authentication-security)
  - [Data Security](#data-security)
- [Prerequisites](#prerequisites)
- [Comprehensive Setup Guide](#comprehensive-setup-guide)
  - [Clone the repository](#1-clone-the-repository)
  - [Backend Configuration](#2-backend-configuration)
  - [Frontend Configuration](#3-frontend-configuration)
  - [Start the Backend Services](#4-start-the-backend-services)
  - [Start the Frontend Development Server](#5-start-the-frontend-development-server)
  - [Access the Complete Application](#6-access-the-complete-application)
  - [Default Administrator Access](#7-default-administrator-access)
- [Authentication Process Flow](#authentication-process-flow)
- [Testing Password Reset](#testing-password-reset-development-mode)
- [Detailed API Documentation](#detailed-api-documentation)
  - [Authentication Endpoints](#authentication-endpoints)
  - [Customer Management Endpoints](#customer-management-endpoints)
- [Data Validation Rules](#data-validation-rules)
  - [Username Validation](#username-validation)
  - [Password Validation](#password-validation)
  - [Email Validation](#email-validation)
  - [Customer Name Validation](#customer-name-validation)
  - [Internet Package Validation](#internet-package-validation)
  - [Sector Validation](#sector-validation)

## Overview

This comprehensive system provides a secure and user-friendly interface for managing Internet Service Provider (ISP) customers. Built with security best practices at every level, it implements a layered defense approach to protect sensitive customer data while maintaining a smooth user experience.

## Key Features

- 🔐 **Enterprise-Grade Authentication**
  - JWT-based user sessions with token expiration
  - Password hashing with PBKDF2-HMAC-SHA256 (1,200,000 iterations)
  - Database-stored cryptographic salt for consistent security
  - Protection against brute force and replay attacks
  - Multi-level account security with both username and IP-based lockouts
  - Account lockout after 3 failed login attempts
  - IP address lockout after 10 failed login attempts
  - Prevention of password reuse (last 3 passwords)
  - Dictionary-based password blacklist
  - Secure password reset flow with time-limited verification

- 👤 **Comprehensive User Management**
  - Secure registration with email validation
  - Login with sanitized error messages to prevent username enumeration
  - Self-service password management with secure validation
  - Three-step password reset process with verification codes
  - Role-based access for future extensibility
  - IP address tracking for enhanced security monitoring

- 👥 **Customer Management**
  - Add new customers with validated information
  - View customers with secure data presentation
  - Input validation to prevent malicious data entry
  - Protection against XSS through automatic HTML escaping

- 🔒 **Full-Stack Security Implementation**
  - Robust server-side validation using Pydantic models
  - Login page frontend validation for user experience
  - Content Security Policy implementation
  - Automatic input sanitization and output escaping
  - Enhanced brute force protection mechanisms

- 🌐 **Production-Ready Architecture**
  - Responsive React-based interface
  - Dockerized deployment for consistency
  - Environment-based configuration
  - Modular, maintainable codebase with proper separation of concerns

## Architecture Diagram

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

## Detailed Project Structure

```
/project_root/
├── README.md                     # Project documentation
├── .gitignore                    # Git ignore file
│
├── backend/
│   ├── .env                      # Backend environment variables (not in git)
│   ├── .env.example              # Example backend environment variables
│   ├── docker-compose.yml        # Docker Compose configuration
│   ├── Dockerfile                # Backend Docker configuration
│   ├── init.sql                  # Database initialization script
│   ├── database.py               # Database connection & configuration
│   ├── models.py                 # SQLAlchemy database models
│   ├── main.py                   # FastAPI application entry point
│   │   ├── API routes            # HTTP endpoints
│   │   ├── Authentication        # Token validation
│   │   ├── Pydantic models       # Request/response validation
│   │   └── Middleware            # CORS, error handling
│   ├── auth_utils.py             # JWT token generation and verification
│   ├── email_utils.py            # Email service for password reset
│   ├── password_utils.py         # Secure password hashing and verification
│   │   ├── Salt management       # Database-stored salt generation/retrieval
│   │   ├── PBKDF2 hashing        # High-iteration password hashing
│   │   └── Verification          # Secure comparison functions
│   ├── validation_utils.py       # Input data validation
│   │   ├── Username rules        # Length, character restrictions
│   │   ├── Password rules        # Complexity requirements
│   │   └── Business rules        # Customer data validation
│   ├── security_utils.py         # Enhanced security features
│   │   ├── Password history      # Previous password tracking
│   │   ├── Login attempts        # Failed login tracking
│   │   └── Account locking       # Temporary account lockouts
│   ├── password_config.py        # Password policy configuration
│   └── requirements.txt          # Python dependencies
│
└── frontend/
    ├── .env                      # Frontend environment variables (not in git)
    ├── .env.example              # Example frontend environment variables
    ├── package.json              # Frontend dependencies
    ├── package-lock.json         # Dependency lock file (not in git)
    ├── public/                   # Static files
    │   ├── favicon.ico           # Application icon
    │   ├── index.html            # HTML entry point
    │   └── robots.txt            # Crawler instructions
    └── src/                      # React source code
        ├── App.js                # Main application component
        ├── App.css               # Main application styles
        ├── AuthContext.js        # Authentication context provider
        ├── config.js             # Configuration settings
        ├── index.js              # React entry point
        ├── index.css             # Global styles
        ├── utils/                # Utility functions
        ├── ChangePassword.js     # Password management component
        ├── CustomerManagement.js # Customer CRUD operations
        ├── ForgotPassword.js     # Password recovery component
        └── Register.js           # User registration component
```

## Technology Stack

### Backend
- **FastAPI**: High-performance Python web framework with automatic OpenAPI documentation
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **Pydantic**: Data validation and settings management
- **PyJWT**: JSON Web Token implementation
- **Cryptography**: Secure cryptographic recipes and primitives
- **Python-dotenv**: Environment variable management
- **Uvicorn**: ASGI server for FastAPI

### Frontend
- **React**: JavaScript library for building user interfaces
- **React Context API**: State management across components
- **HTML5/CSS3**: Modern layout and styling
- **Fetch API**: Network requests to backend services
- **localStorage**: Client-side token storage

### Database
- **MySQL**: Reliable relational database system
- **SQLAlchemy ORM**: Object-relational mapping for database access

### Infrastructure
- **Docker**: Containerization for consistent environments
- **Docker Compose**: Multi-container orchestration

## Enhanced Security Features

### Advanced Authentication Protection

#### Password Policy Enforcement
The system now enforces a robust password policy:

1. **Password History Tracking**:
   - Prevents reuse of the last 3 passwords
   - Stores securely hashed password history
   - Enforces during password change operations
   - Applied to both password change and password reset flows

2. **Dictionary Password Prevention**:
   - Maintains a comprehensive list of common passwords
   - Prevents use of easily guessable passwords
   - Case-insensitive matching for better protection

3. **Multi-Layered Brute Force Protection**:
   - **User Account Protection**:
     - Account lockout after 3 failed login attempts
     - 30-minute lockout duration
     - Protection against targeted account attacks
   
   - **IP-Based Protection**:
     - IP address lockout after 10 failed login attempts
     - Sliding 24-hour window for tracking attempts
     - 60-minute lockout duration
     - Protection against distributed brute force attacks
     - Prevents attackers from targeting multiple accounts
   
   - **Comprehensive Tracking**:
     - IP address logging for all login attempts
     - Records both successful and unsuccessful attempts
     - Enables security forensics and pattern detection

4. **Secure Password Reset**:
   - Three-step verification process (email → token → password)
   - Time-limited verification codes (20-minute expiration)
   - Single-use verification tokens
   - Separation of verification and password reset steps
   - Password history validation during reset

#### Centralized Security Configuration
The system uses a modular approach to security settings:

1. **Configurable Security Parameters**:
   - Password complexity requirements in `password_config.py`
   - Password history depth setting
   - Failed login attempt thresholds (both user and IP-based)
   - Account lockout duration settings
   - IP lockout duration settings

2. **Database Structure for Security**:
   - Password history tracking tables
   - Login attempt monitoring tables with IP tracking
   - Account status tracking tables
   - Password reset token tables

## Detailed Security Implementation

### Authentication Security

#### Password Hashing Process
The system employs a secure password hashing implementation:

1. **Salt Generation & Storage**:
   - A 32-byte (256-bit) cryptographically secure random salt is generated at first application startup
   - The salt is stored in a dedicated `secrets` table in the database with ID "main"
   - This approach ensures consistent salt usage across application instances

2. **Password Hashing Algorithm**:
   - PBKDF2-HMAC-SHA256 with 1,200,000 iterations (significantly above NIST recommendations)
   - 32-byte (256-bit) derived key length
   - Base64 encoding for database storage

3. **Verification Process**:
   - Constant-time comparison to prevent timing attacks
   - Same salt and parameters ensure consistent verification

#### JWT Authentication
The system implements secure JWT (JSON Web Token) authentication:

1. **JWT Secret Key Management**:
   - The system generates and stores a secure random JWT secret key in the database
   - This approach provides consistent authentication across multiple application instances
   - The environment variable JWT_SECRET_KEY is used as a fallback option only
   - Secret key is securely stored in the database `secrets` table with ID "jwt_secret"

2. **Token Generation**:
   - HS256 (HMAC with SHA-256) algorithm for signing tokens
   - 1-hour expiration time to limit attack window
   - Username stored as subject claim

3. **Token Validation**:
   - Full signature validation
   - Expiration time checking
   - Token extraction from Authorization header

4. **Frontend Token Management**:
   - Secure storage in localStorage
   - Automatic inclusion in API request headers
   - Session termination on logout

#### Password Reset Process
The system implements a secure three-step password reset flow:

1. **Email Request (Step 1)**:
   - User submits email address
   - System generates a secure SHA-1 verification code
   - Code is stored with a 20-minute expiration time
   - In development mode, code is displayed in console
   - In production mode, code is sent via Web3Forms email service

2. **Code Verification (Step 2)**:
   - User submits verification code
   - Backend validates code against stored token
   - Token must be unexpired and unused
   - Authorization to reset password granted only after verification

3. **Password Reset (Step 3)**:
   - User submits new password with verified token
   - Password is validated against security policy and password history
   - System ensures new password differs from previous passwords
   - Token is marked as used after successful reset
   - User receives confirmation of successful reset

#### Brute Force Defense
The system implements a multilayered approach to defend against brute force attacks:

1. **Per-User Account Protection**:
   - Tracks failed login attempts per username
   - Implements account lockout after threshold is reached
   - Prevents targeted attacks against specific accounts
   - Uses the `AccountStatus` table to track lockout status

2. **IP-Based Protection**:
   - Tracks failed login attempts by IP address
   - Implements IP lockout after threshold is reached
   - Uses a sliding window approach (24-hour period)
   - Prevents distributed attacks across multiple accounts
   - Uses the `LoginAttempt` table for IP tracking

3. **Progressive Security Logic**:
   - First checks IP-based restrictions
   - Then checks user-based restrictions
   - Ensures complete protection against various attack patterns
   - Records all attempts with timestamps for analysis

### Data Security

#### Input Validation
The system implements a two-tier validation strategy:

1. **Login Page Frontend Validation**:
   - Real-time feedback on login page only
   - Basic validation for user experience

2. **Robust Server-Side Validation**:
   - Primary validation mechanism for all endpoints
   - Pydantic models for request body validation
   - Type checking and constraint enforcement
   - Detailed error messaging for debugging
   - Protection against malformed or malicious data

3. **Database Validation**:
   - SQLAlchemy column constraints
   - Unique constraints for username/email
   - Foreign key constraints for data integrity

#### Output Security
The system protects against XSS and injection attacks:

1. **HTML Escaping**:
   - Automatic escaping of HTML special characters
   - Custom `sanitize_string()` function
   - Pydantic validators for response models

2. **Safe Rendering**:
   - React's built-in XSS protection
   - Custom helper to handle sanitized content
   - Type-safe rendering in components

## Prerequisites

Before setting up the application, ensure you have the following tools installed on your system:

### Docker and Docker Compose (v1.29+)

Docker is used to containerize the application and its dependencies.

**Installation:**
1. Download and install Docker Desktop from the [official Docker website](https://www.docker.com/products/docker-desktop)
2. Docker Desktop includes both Docker Engine and Docker Compose
3. After installation, verify with:
   ```bash
   docker --version
   docker-compose --version
   ```

### Git

Git is needed to clone the repository and manage version control.

**Installation:**
- **Windows**: Download and install from [Git for Windows](https://gitforwindows.org/)
- **macOS**: 
  - Using Homebrew: `brew install git`
  - Or download from [Git website](https://git-scm.com/download/mac)
- **Linux**: 
  - Debian/Ubuntu: `sudo apt-get update && sudo apt-get install git`
  - Fedora: `sudo dnf install git`

Verify installation with:
```bash
git --version
```

### Node.js (v14+) and npm (v6+)

Required for frontend development and building the React application.

**Installation:**
- **Option 1**: Download the LTS version from [Node.js official website](https://nodejs.org/)
- **Option 2**: Use a version manager (recommended for developers):
  - For Windows: Use [nvm-windows](https://github.com/coreybutler/nvm-windows)
  - For macOS/Linux: Use [nvm](https://github.com/nvm-sh/nvm)
    ```bash
    # Install nvm
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
    
    # Install Node.js
    nvm install --lts
    ```

Verify installation with:
```bash
node --version
npm --version
```

### Modern Web Browser

For accessing and testing the application frontend.

**Recommended browsers:**
- [Google Chrome](https://www.google.com/chrome/) (Latest version)
- [Mozilla Firefox](https://www.mozilla.org/firefox/new/) (Latest version)
- [Microsoft Edge](https://www.microsoft.com/edge) (Latest version)
- [Safari](https://www.apple.com/safari/) (for macOS users, latest version)

## Comprehensive Setup Guide

### 1. Clone the repository

```bash
git clone https://github.com/eliorabaev/CyberSecurity.git
cd CyberSecurity
```

### 2. Backend Configuration

Create and configure the backend environment variables:

```bash
cd backend
cp .env.example .env
```

Edit the `.env` file with secure credentials:

```
# Database Configuration
DB_USER=your_username         # Choose your own username
DB_PASSWORD=your_password     # Choose your own secure password (min. 12 chars recommended)
DB_HOST=localhost             # Keep as localhost for local development
DB_NAME=internet_service_provider

# Docker specific variables
DB_ROOT_PASSWORD=your_root_password  # Change this for production (min. 16 chars recommended)
DB_PORT=3307                    # Change if port 3307 is already in use
API_PORT=8000                   # Change if port 8000 is already in use

# Frontend URL for CORS - update for production
FRONTEND_URL=http://localhost:3000

# Always use MySQL - future support for other databases planned
USE_MYSQL=true

# Email Settings for password reset
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_FROM=noreply@yourcompany.com

# Web3Forms API Key
# Replace with your actual Web3Forms API key
# The verification key for password reset will be sent to the mail associated with the API key
# You can get your API key from https://web3forms.com
WEB3FORMS_API_KEY=enter_your_api_key_here
```

> **Security Note**: For production environments, use a password manager or secure secret generator to create unique, high-entropy passwords and keys.

### 3. Frontend Configuration

Configure the React frontend:

```bash
cd ../frontend
cp .env.example .env
```

The frontend `.env` file should contain:

```
# API connection settings - update for production
REACT_APP_API_HOST=localhost
REACT_APP_API_PORT=8000
```

### 4. Start the Backend Services

Launch the backend with Docker Compose:

```bash
cd ../backend
docker-compose up -d
```

This command:
- Builds the Python FastAPI backend container
- Initializes a MySQL database container
- Creates required volumes and networking
- Sets up a secure communication channel between containers

Verify the services are running:

```bash
docker-compose ps
```

You should see both services with status "Up".

### 5. Start the Frontend Development Server

For development or standalone frontend:

```bash
cd ../frontend
npm install
npm start
```

This will:
- Install all required dependencies
- Start the React development server on port 3000
- Open your default browser to the application

### 6. Access the Complete Application

- **Frontend UI**: http://localhost:3000
- **API Endpoints**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

### 7. Default Administrator Access

The system creates a default admin user on first startup:
- Username: `admin`
- Password: `admin`

**⚠️ CRITICAL SECURITY ACTION**: Change the default admin password immediately after first login using the Change Password feature. This default password is intended for initial setup only and poses a significant security risk if not changed.

## Authentication Process Flow

The system implements a secure JWT-based authentication flow:

1. **User Registration**:
   - Client submits username, email, and password
   - Server validates input data, checking against the password blacklist
   - Password is hashed using PBKDF2-HMAC-SHA256
   - User record is created in database
   - Initial password is added to password history
   - Success response is returned (no auto-login)

2. **User Login**:
   - Client provides basic validation on the login form
   - Client submits username and password
   - Server first checks if the client's IP is temporarily locked
   - If IP is not locked, server checks for previous failed attempts for the username
   - If account is locked, login is denied with appropriate message
   - If not locked, server validates credentials
   - Failed attempts are recorded with IP address
   - If user failure limit is reached, account is locked for 30 minutes
   - If IP failure limit is reached, IP is locked for 60 minutes
   - On success, failed attempt counters are reset
   - Server creates signed JWT with the database-stored secret key
   - Token is returned to client with 1-hour expiration
   - Client stores token in localStorage

3. **Authenticated Requests**:
   - Client includes token in Authorization header
   - Server validates token signature and expiration
   - Server extracts username from token
   - Server verifies user exists in database
   - Request is processed if authentication succeeds

4. **Password Reset Flow**:
   - User requests password reset by entering email
   - System generates verification code with 20-minute expiration
   - In development mode, code appears in server console
   - In production mode, code is sent via Web3Forms email service
   - User enters verification code for validation
   - After successful validation, user sets new password
   - New password is checked against password history and blacklist
   - Token is invalidated after successful password reset

5. **Password Change**:
   - Client submits old and new passwords with token
   - Server validates token and old password
   - New password is checked against password history and blacklist
   - New password is hashed and stored
   - Password is added to password history
   - Success response indicates completion

6. **Logout Process**:
   - Client removes token from localStorage
   - No server-side action required (stateless authentication)
   - User must re-authenticate to access protected resources

## Testing Password Reset (Development Mode)

For development testing of the password reset functionality:

1. Request a password reset by entering an email address
2. Check the server console output for the verification code
   ```
   [DEV MODE] Password reset verification code for user@example.com: a1b2c3d4e5...
   ```
3. Enter this code in the verification step
4. Create a new password after verification

For production use, configure `WEB3FORMS_API_KEY` in your `.env` file. The verification code will be sent to the email address associated with your Web3Forms API key. You can get your API key from https://web3forms.com/dashboard.

## Detailed API Documentation

### Authentication Endpoints

#### `POST /login`
Authenticates a user and provides a JWT token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

**Error Responses:**
- `400 Bad Request`: Missing username or password
- `401 Unauthorized`: Invalid credentials
- `423 Locked`: Account is temporarily locked
- `429 Too Many Requests`: Too many failed login attempts (either user-based or IP-based)

#### `POST /register`
Creates a new user account.

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "message": "Registration successful"
}
```

**Error Responses:**
- `400 Bad Request`: Validation error, common password, or existing username/email

#### `POST /forgot-password`
Initiates the password reset process.

**Request Body:**
```json
{
  "email": "string"
}
```

**Response (200 OK):**
```json
{
  "message": "If an account with this email exists, a verification code has been sent."
}
```

#### `POST /verify-reset-token`
Verifies the reset token before allowing password change.

**Request Body:**
```json
{
  "email": "string",
  "token": "string"
}
```

**Response (200 OK):**
```json
{
  "message": "Verification code is valid. Please set a new password."
}
```

**Error Responses:**
- `400 Bad Request`: Invalid or expired verification code

#### `POST /reset-password`
Resets the password using a verified token.

**Request Body:**
```json
{
  "email": "string",
  "token": "string",
  "new_password": "string"
}
```

**Response (200 OK):**
```json
{
  "message": "Password has been reset successfully"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid token, password validation failure, or password in history

#### `GET /me`
Retrieves information about the authenticated user.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "username": "string",
  "email": "string"
}
```

**Error Responses:**
- `401 Unauthorized`: Missing or invalid token

#### `POST /change-password`
Changes the password for the authenticated user.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "oldPassword": "string",
  "newPassword": "string"
}
```

**Response (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid new password, common password, or password in history
- `401 Unauthorized`: Invalid old password or token

### Customer Management Endpoints

#### `GET /customers`
Retrieves a list of all customers.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "customers": [
    {
      "id": 1,
      "name": "string",
      "internet_package": "string",
      "sector": "string",
      "date_added": "YYYY-MM-DD"
    }
  ]
}
```

**Error Responses:**
- `401 Unauthorized`: Missing or invalid token

#### `POST /customers`
Adds a new customer.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "string",
  "internet_package": "string",
  "sector": "string"
}
```

**Response (200 OK):**
```json
{
  "message": "Customer added successfully"
}
```

**Error Responses:**
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Missing or invalid token

## Data Validation Rules

### Username Validation
- 3-20 characters in length
- Only English letters (a-z, A-Z) and numbers (0-9)
- No spaces or special characters
- Required field (cannot be empty)

### Password Validation
- Minimum 10 characters (configurable)
- Maximum 50 characters (configurable)
- Must include at least one uppercase letter
- Must include at least one lowercase letter
- Must include at least one number
- Must include at least one special character
- Cannot be one of the common passwords in the blacklist
- Cannot be one of the user's last 3 passwords
- Required field (cannot be empty)

### Email Validation
- Must follow standard email format (user@domain.tld)
- Required field (cannot be empty)

### Customer Name Validation
- Only English letters (a-z, A-Z) and spaces
- Minimum 2 characters
- Maximum 100 characters
- Required field (cannot be empty)

### Internet Package Validation
- Must be one of the predefined options:
  - "Basic (10 Mbps)"
  - "Standard (50 Mbps)"
  - "Premium (100 Mbps)"
  - "Enterprise (500 Mbps)"
- Required field (cannot be empty)

### Sector Validation
- Must be one of the predefined options:
  - "North"
  - "South"
  - "East"
  - "West"
  - "Central"
- Required field (cannot be empty)
