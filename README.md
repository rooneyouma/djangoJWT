# Django JWT Authentication

This project is a demonstration of Django authentication with JSON Web Tokens (JWT). It includes user signup, login, logout, and an API for the user model with authentication and permission handling.

## Features
- User registration (Signup)
- User login with JWT authentication
- User logout
- Protected API endpoints for user management
- Token-based authentication using access and refresh tokens

## Technologies Used
- Django
- Django REST Framework (DRF)
- Simple JWT for token-based authentication
- PostgreSQL / SQLite (depending on configuration)
- Postman (for API testing)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/rooneyouma/djangoJWT.git
cd djangoJWT
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create a Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

## Authentication & Permissions
This project uses JWT authentication:
- **Access Token:** Used for authentication and expires in a short time.
- **Refresh Token:** Used to obtain a new access token when the current one expires.

Users must include their token in the request headers:
```
Authorization: Bearer <your_access_token>
```
### Permissions
- **Authenticated users** can view and update their details.
- **Admin users** can manage all users.

## Testing with Postman
1. Use the access token for authorized requests (add it to the `Authorization` header as `Bearer <token>`)

