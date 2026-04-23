# Event Manager - Technical Event Management System

A comprehensive FastAPI-based event item management and ordering system with role-based access control for Admin, Vendor, and User roles.

## Project Overview

This system enables:
- **Users** to browse products, create carts, place orders, track order status, and request unavailable items
- **Vendors** to manage their products, update inventory, respond to item requests, and manage order fulfillment
- **Admins** to oversee the entire platform, manage users and vendors, monitor orders, and handle item requests

## Technology Stack

- **Backend**: FastAPI (modern Python web framework)
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL/MySQL support
- **Authentication**: JWT-based token authentication
- **Password Security**: bcrypt hashing with passlib
- **API Validation**: Pydantic schemas
- **Package Management**: pip with requirements.txt

## Project Structure

```
event_manager/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration and environment variables
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # JWT and password hashing utilities
│   │   └── roles.py            # Role-based access control
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py             # SQLAlchemy base class
│   │   └── session.py          # Database session management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── enums.py            # Enum definitions for roles and statuses
│   │   ├── admin.py            # Admin model
│   │   ├── user.py             # User model
│   │   ├── vendor.py           # Vendor model
│   │   ├── product.py          # Product model
│   │   ├── cart.py             # Cart and CartItem models
│   │   ├── order.py            # Order and OrderItem models
│   │   └── item_request.py     # ItemRequest model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication request/response schemas
│   │   ├── product.py          # Product schemas
│   │   ├── cart.py             # Cart schemas
│   │   ├── order.py            # Order schemas
│   │   └── item_request.py     # Item request schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Authentication business logic
│   │   ├── product_service.py  # Product CRUD and management
│   │   ├── cart_service.py     # Shopping cart operations
│   │   ├── order_service.py    # Order management
│   │   └── item_request_service.py  # Item request handling
│   └── api/
│       ├── __init__.py
│       └── routes/
│           ├── __init__.py
│           ├── auth.py         # Authentication endpoints
│           ├── admins.py       # Admin endpoints
│           ├── vendors.py      # Vendor endpoints
│           ├── users.py        # User endpoints
│           ├── products.py     # Product endpoints
│           ├── carts.py        # Cart endpoints
│           ├── checkout.py     # Checkout endpoints
│           ├── orders.py       # Order endpoints
│           └── item_requests.py    # Item request endpoints
├── tests/                      # Test files
├── .env                        # Environment variables (configure for your setup)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Database Schema

### Tables

1. **admins**: Admin user accounts
   - id, name, email (unique), password_hash, created_at

2. **users**: Regular platform users
   - id, name, email (unique), password_hash, phone, created_at, is_active

3. **vendors**: Item suppliers
   - id, name, email (unique), password_hash, company_name, phone, status, created_at

4. **products**: Event items
   - id, name, description, category, quantity, price, status, vendor_id (FK), created_at, updated_at

5. **carts**: User shopping carts
   - id, user_id (FK), created_at, updated_at

6. **cart_items**: Items in shopping cart
   - id, cart_id (FK), product_id (FK), quantity, created_at

7. **orders**: User purchase orders
   - id, user_id (FK), order_number (unique), total_amount, status, created_at, updated_at

8. **order_items**: Items in an order
   - id, order_id (FK), product_id (FK), quantity, price, created_at

9. **item_requests**: User requests for unavailable items
   - id, user_id (FK), item_name, description, category, status, vendor_id (FK), created_at, updated_at

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Database: SQLite (default, no setup needed) or PostgreSQL/MySQL (optional)

### 1. Clone/Create Project

```bash
cd event_manager
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy and configure the `.env` file:

```bash
cp .env .env.local  # Create your own configuration
```

Edit `.env.local` with your settings:

```env
# For development (SQLite is default)
DATABASE_URL=sqlite:///./event_manager.db
SECRET_KEY=your-secret-key-here

# For production (PostgreSQL)
# DATABASE_URL=postgresql://user:password@localhost:5432/event_db
# SECRET_KEY=use-a-strong-random-key-here
```

### 5. Run Application

```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API Documentation**: http://localhost:8000/api/docs
- **ReDoc Documentation**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Authentication (`/api/v1/auth`)

```
POST   /admin/signup          - Register new admin
POST   /admin/login           - Admin login
POST   /user/signup           - Register new user
POST   /user/login            - User login
POST   /vendor/login          - Vendor login
```

### Admin Management (`/api/v1/admin`)

```
GET    /dashboard             - Admin dashboard statistics
GET    /users                 - List all users
GET    /users/{user_id}       - Get user details
PUT    /users/{user_id}/deactivate  - Deactivate user
GET    /vendors               - List all vendors
GET    /vendors/{vendor_id}   - Get vendor details
GET    /orders                - List all orders
GET    /item-requests         - List all item requests
```

### Vendor Management (`/api/v1/vendor`)

```
GET    /dashboard             - Vendor dashboard
POST   /products              - Create product
GET    /products              - List vendor's products
GET    /products/{product_id} - Get product details
PUT    /products/{product_id} - Update product
DELETE /products/{product_id} - Delete product
GET    /item-requests         - List assigned item requests
```

### User Management (`/api/v1/user`)

```
GET    /profile               - Get user profile
PUT    /profile               - Update user profile
```

### Products (`/api/v1/products`)

```
GET    /                      - List all products (with filtering)
GET    /{product_id}          - Get product details
GET    /categories            - Get product categories
GET    /search/?query=text    - Search products
```

### Shopping Cart (`/api/v1/cart`)

```
GET    /                      - Get user's cart
GET    /summary               - Get cart summary with totals
POST   /add                   - Add item to cart
PUT    /items/{product_id}    - Update item quantity
DELETE /items/{product_id}    - Remove item from cart
DELETE /                      - Clear entire cart
```

### Checkout (`/api/v1/checkout`)

```
POST   /place-order           - Create order from cart
GET    /success/{order_id}    - Order success confirmation
```

### Orders (`/api/v1/orders`)

```
GET    /my-orders             - Get user's orders
GET    /{order_id}            - Get order details
GET    /by-number/{order_number}  - Get order by number
PUT    /{order_id}/status     - Update order status (Admin/Vendor)
POST   /{order_id}/cancel     - Cancel order (User)
```

### Item Requests (`/api/v1/item-requests`)

```
POST   /                      - Create new item request
GET    /my-requests           - Get user's requests
GET    /{request_id}          - Get request details
GET    /pending               - List pending requests (Admin/Vendor)
PUT    /{request_id}/status   - Update request status
PUT    /{request_id}/assign-vendor/{vendor_id}  - Assign to vendor (Admin)
PUT    /{request_id}/fulfill  - Mark as fulfilled (Vendor)
```

## Authentication Flow

### 1. User Registration and Login

```bash
# Admin Signup
curl -X POST http://localhost:8000/api/v1/auth/admin/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin User",
    "email": "admin@example.com",
    "password": "secure_password_123"
  }'

# User Signup
curl -X POST http://localhost:8000/api/v1/auth/user/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "user@example.com",
    "password": "secure_password_123",
    "phone": "1234567890"
  }'

# User Login
curl -X POST http://localhost:8000/api/v1/auth/user/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password_123"
  }'
```

### 2. Using JWT Token

All authenticated endpoints require the Bearer token in the Authorization header:

```bash
curl -X GET http://localhost:8000/api/v1/user/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Usage Workflows

### Workflow 1: User Places Order

1. **User Signup/Login** → Get access token
2. **Browse Products** → GET `/api/v1/products`
3. **Add to Cart** → POST `/api/v1/cart/add`
4. **View Cart** → GET `/api/v1/cart`
5. **Checkout** → POST `/api/v1/checkout/place-order`
6. **Track Order** → GET `/api/v1/orders/my-orders`

### Workflow 2: Request Unavailable Item

1. **Create Request** → POST `/api/v1/item-requests`
2. **Track Status** → GET `/api/v1/item-requests/my-requests`
3. **Admin Reviews** → GET `/api/v1/admin/item-requests`
4. **Admin Assigns to Vendor** → PUT `/api/v1/item-requests/{id}/assign-vendor/{vendor_id}`
5. **Vendor Fulfills** → PUT `/api/v1/item-requests/{id}/fulfill`

### Workflow 3: Vendor Manages Products

1. **Vendor Login** → Get vendor token
2. **Create Product** → POST `/api/v1/vendor/products`
3. **Update Product** → PUT `/api/v1/vendor/products/{id}`
4. **View Orders** → GET `/api/v1/admin/orders`
5. **Update Order Status** → PUT `/api/v1/orders/{id}/status`

## Testing

### Run Tests

```bash
pytest
```

### Generate Sample Data

Create a script `seed_data.py`:

```python
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Admin, User, Vendor, Product
from app.core import hash_password

db = SessionLocal()

# Create sample admin
admin = Admin(
    name="System Admin",
    email="admin@example.com",
    password_hash=hash_password("admin123")
)
db.add(admin)

# Create sample user
user = User(
    name="John Doe",
    email="user@example.com",
    password_hash=hash_password("user123"),
    phone="1234567890"
)
db.add(user)

# Create sample vendor
vendor = Vendor(
    name="Tech Supplies",
    email="vendor@example.com",
    password_hash=hash_password("vendor123"),
    company_name="TechSupplies Inc."
)
db.add(vendor)

db.commit()
print("Sample data created successfully!")
```

Run seed script:
```bash
python seed_data.py
```

## Security Features

1. **Password Security**: bcrypt hashing for all passwords
2. **JWT Authentication**: Secure token-based authentication
3. **Role-Based Access Control**: Three distinct roles with endpoint protection
4. **Input Validation**: Pydantic schemas validate all inputs
5. **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection
6. **CORS Configuration**: Configurable CORS for security

## Production Deployment

### 1. Environment Setup

```bash
# Use strong secret key
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')

# Use PostgreSQL for production
export DATABASE_URL=postgresql://user:password@db-server:5432/event_db
```

### 2. Run with Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

### 3. Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Database Connection Issues

```bash
# Check database URL in .env
DATABASE_URL=sqlite:///./event_manager.db  # SQLite (local)
DATABASE_URL=postgresql://user:pass@localhost/db  # PostgreSQL
```

### Import Errors

```bash
# Ensure you're in virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Token Errors

- Ensure token is passed in `Authorization: Bearer <token>` header
- Check token expiration (default: 60 minutes)
- Regenerate token by logging in again

## Future Enhancements

- [ ] Product search and filtering improvements
- [ ] Order pagination and advanced filtering
- [ ] Email notifications for orders and requests
- [ ] Payment gateway integration
- [ ] Vendor performance analytics
- [ ] Admin dashboard analytics
- [ ] Soft delete for data retention
- [ ] Audit logging for compliance
- [ ] WebSocket for real-time order updates
- [ ] File uploads for product images

## API Documentation

Complete API documentation is auto-generated and available at:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Support

For issues, questions, or contributions, please check the documentation or reach out to the development team.

## License

This project is licensed under the MIT License.
