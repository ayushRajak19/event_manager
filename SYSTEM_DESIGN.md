# Technical Event Management System - System Design Document

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Database Design](#database-design)
4. [API Endpoints](#api-endpoints)
5. [Authentication & Authorization](#authentication--authorization)
6. [Business Logic](#business-logic)
7. [Deployment](#deployment)

---

## System Overview

The **Technical Event Management System** is a comprehensive web platform for managing event item procurement, vendor management, and order fulfillment. It enables three distinct user roles to interact with the system:

### Key Features

#### For Users
- Browse and search event items/products
- Add items to shopping cart
- Place orders and track status
- Request unavailable items
- View order history
- Manage personal profile

#### For Vendors
- Manage product inventory
- Update product availability
- Fulfill item requests from users
- Update order status
- View assigned work and requests

#### For Admins
- Oversee entire platform
- Manage users and vendors
- Monitor all orders
- Handle item request approvals
- View platform analytics/statistics

---

## Architecture

### Technology Stack

```
Frontend/Client Layer
        ↓
API Gateway (FastAPI)
        ↓
Authentication Layer (JWT)
        ↓
Business Logic Layer (Services)
        ↓
Data Access Layer (SQLAlchemy ORM)
        ↓
Database (SQLite/PostgreSQL/MySQL)
```

### Architectural Layers

#### 1. **Presentation Layer** (API Routes)
- RESTful FastAPI endpoints
- Input validation using Pydantic
- Response serialization
- Error handling with appropriate HTTP status codes

Files:
```
app/api/routes/
├── auth.py           # Authentication endpoints
├── admins.py         # Admin endpoints
├── vendors.py        # Vendor endpoints
├── users.py          # User endpoints
├── products.py       # Product endpoints
├── carts.py          # Cart endpoints
├── checkout.py       # Checkout endpoints
├── orders.py         # Order endpoints
└── item_requests.py  # Item request endpoints
```

#### 2. **Business Logic Layer** (Services)
- Implements core business rules
- Handles complex operations
- Manages data consistency
- Transaction management

Files:
```
app/services/
├── auth_service.py           # User registration & authentication
├── product_service.py        # Product CRUD & management
├── cart_service.py           # Shopping cart operations
├── order_service.py          # Order processing & tracking
└── item_request_service.py   # Item request handling
```

#### 3. **Data Access Layer** (Models & Database)
- SQLAlchemy ORM models
- Database schema definition
- Relationship management

Files:
```
app/models/
├── enums.py       # Enum definitions for statuses/roles
├── admin.py       # Admin model
├── user.py        # User model
├── vendor.py      # Vendor model
├── product.py     # Product model
├── cart.py        # Cart & CartItem models
├── order.py       # Order & OrderItem models
└── item_request.py  # ItemRequest model
```

#### 4. **Security Layer** (Authentication & Authorization)
- JWT token generation and validation
- Password hashing with bcrypt
- Role-based access control
- Request authorization

Files:
```
app/core/
├── security.py   # JWT & password utilities
└── roles.py      # Authorization & role checks
```

---

## Database Design

### Entity Relationship Diagram (Conceptual)

```
┌────────────┐         ┌──────────┐
│   Admin    │         │  Vendor  │
└────────────┘         └────┬─────┘
                            │ (1)
                            │ (creates)
                            ↓ (M)
        ┌───────────────┌────────────┐
        │               │  Product   │
        │ (M)           │            │
        ↓ (1)      ┌────┤ ├──────────┘
    ┌────────┐     │    │
    │  User  │     │    │ (M) (1)
    └───┬────┘     │    │
        │ (1)      │    ↓
        ├─────────→┤  ┌──────────┐
        │ (M)      │  │CartItem  │
        ├──────────┤  └──────────┘
        │          │
        │ (1)      │
        ├─────────→┤
        │ (M)      │
        ├──────────┤
        │          │
        │ (1)      │
        ├─────────→┤
        │ (M)      │
        ↓          │
    ┌────────┐     │
    │  Cart  │     │
    └────────┘     │
        │          │
        │ (1)      │
        ├─────────→┤
        │ (M)      │
        ↓          │
    ┌────────┐     │
    │ Order  │←────┘
    └───┬────┘
        │ (1)
        ├──────────→┤
        │ (M)       │
        ↓           │
   ┌──────────┐     │
   │OrderItem │←────┘
   └──────────┘

    ┌─────────────┐
    │ItemRequest  │ (user_id, vendor_id)
    └─────────────┘
```

### Database Tables

#### 1. **admins**
```sql
CREATE TABLE admins (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. **users**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER DEFAULT 1  -- Boolean as 0/1
);
```

#### 3. **vendors**
```sql
CREATE TABLE vendors (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    status VARCHAR(50) DEFAULT 'active',  -- active/inactive/suspended
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 4. **products**
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(1000),
    category VARCHAR(100),
    quantity INTEGER DEFAULT 0,
    price FLOAT NOT NULL,
    status VARCHAR(50) DEFAULT 'available',  -- available/out_of_stock/discontinued
    vendor_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vendor_id) REFERENCES vendors(id)
);
```

#### 5. **carts**
```sql
CREATE TABLE carts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### 6. **cart_items**
```sql
CREATE TABLE cart_items (
    id INTEGER PRIMARY KEY,
    cart_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES carts(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

#### 7. **orders**
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    total_amount FLOAT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'pending',  -- pending/approved/packed/dispatched/delivered/cancelled
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### 8. **order_items**
```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

#### 9. **item_requests**
```sql
CREATE TABLE item_requests (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    description VARCHAR(1000),
    category VARCHAR(100),
    status VARCHAR(50) DEFAULT 'pending',  -- pending/approved/fulfilled/rejected
    vendor_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(id)
);
```

---

## API Endpoints

### Complete Endpoint Reference

#### Authentication Endpoints
```
POST   /api/v1/auth/admin/signup      - Admin registration
POST   /api/v1/auth/admin/login       - Admin login
POST   /api/v1/auth/user/signup       - User registration
POST   /api/v1/auth/user/login        - User login
POST   /api/v1/auth/vendor/login      - Vendor login
```

#### Admin Endpoints (Admin Only)
```
GET    /api/v1/admin/dashboard        - Dashboard statistics
GET    /api/v1/admin/users            - List all users
GET    /api/v1/admin/users/{id}       - User details
PUT    /api/v1/admin/users/{id}/deactivate - Deactivate user
GET    /api/v1/admin/vendors          - List all vendors
GET    /api/v1/admin/vendors/{id}     - Vendor details
GET    /api/v1/admin/orders           - List all orders
GET    /api/v1/admin/item-requests    - List all item requests
```

#### User Endpoints (User Only)
```
GET    /api/v1/user/profile           - Get user profile
PUT    /api/v1/user/profile           - Update user profile
```

#### Vendor Endpoints (Vendor Only)
```
GET    /api/v1/vendor/dashboard       - Vendor dashboard
POST   /api/v1/vendor/products        - Create product
GET    /api/v1/vendor/products        - List vendor's products
GET    /api/v1/vendor/products/{id}   - Product details
PUT    /api/v1/vendor/products/{id}   - Update product
DELETE /api/v1/vendor/products/{id}   - Delete product
GET    /api/v1/vendor/item-requests   - List assigned requests
```

#### Product Endpoints (All Authenticated Users)
```
GET    /api/v1/products               - List all products
GET    /api/v1/products/{id}          - Product details
GET    /api/v1/products/categories    - Get categories
GET    /api/v1/products/search/?query - Search products
```

#### Cart Endpoints (Users Only)
```
GET    /api/v1/cart                   - Get cart
GET    /api/v1/cart/summary           - Cart summary
POST   /api/v1/cart/add               - Add to cart
PUT    /api/v1/cart/items/{id}        - Update quantity
DELETE /api/v1/cart/items/{id}        - Remove from cart
DELETE /api/v1/cart                   - Clear cart
```

#### Checkout Endpoints (Users Only)
```
POST   /api/v1/checkout/place-order   - Create order
GET    /api/v1/checkout/success/{id}  - Order success confirmation
```

#### Order Endpoints
```
GET    /api/v1/orders/my-orders       - User's orders
GET    /api/v1/orders/{id}            - Order details
GET    /api/v1/orders/by-number/{num} - Get by order number
PUT    /api/v1/orders/{id}/status     - Update status (Admin/Vendor)
POST   /api/v1/orders/{id}/cancel     - Cancel order (User)
```

#### Item Request Endpoints
```
POST   /api/v1/item-requests          - Create request
GET    /api/v1/item-requests/my-requests   - User's requests
GET    /api/v1/item-requests/{id}     - Request details
GET    /api/v1/item-requests/pending  - Pending requests (Admin/Vendor)
PUT    /api/v1/item-requests/{id}/status   - Update status
PUT    /api/v1/item-requests/{id}/assign-vendor/{vid} - Assign vendor (Admin)
PUT    /api/v1/item-requests/{id}/fulfill  - Fulfill request (Vendor)
```

---

## Authentication & Authorization

### Authentication Flow

```
1. User sends credentials
        ↓
2. Server validates credentials
        ↓
3. Password verified using bcrypt
        ↓
4. JWT token generated with claims:
   - sub: user_id
   - role: user/admin/vendor
   - email: user_email
   - exp: expiration_time
        ↓
5. Token returned to client
        ↓
6. Client stores token (localStorage/sessionStorage)
        ↓
7. Client sends token in Authorization header for subsequent requests:
   Authorization: Bearer <token>
```

### Authorization

Role-based access control implemented using dependency injection:

```python
# Example: Only admin can access endpoint
@app.get("/admin/users")
async def get_users(current_user: dict = Depends(require_admin)):
    # Only executed if user has admin role
    pass

# Example: Check specific role
if current_user["role"] != "vendor":
    raise HTTPException(status_code=403, detail="Vendor role required")
```

### JWT Token Structure

```json
{
  "sub": "1",           // User ID
  "role": "user",       // User role
  "email": "user@example.com",
  "exp": 1704067200    // Expiration timestamp
}
```

### Password Security

- Passwords hashed using bcrypt with salt
- Stored as `password_hash` in database
- Never stored in plain text
- Verified using `verify_password()` function

```python
from app.core.security import hash_password, verify_password

# Hashing
hashed = hash_password("plaintext_password")

# Verification
is_valid = verify_password("plaintext_password", hashed)
```

---

## Business Logic

### Key Workflows

#### Workflow 1: User Orders Flow

```
1. User Signup/Login
   └─→ Receive JWT token

2. Browse Products
   └─→ GET /products (public, paginated)

3. Add to Cart
   └─→ POST /cart/add
   └─→ Check product availability
   └─→ Create/update CartItem

4. View Cart
   └─→ GET /cart
   └─→ Show items and total

5. Checkout
   └─→ POST /checkout/place-order
   └─→ Validate cart not empty
   └─→ Create Order with status=pending
   └─→ Create OrderItems from CartItems
   └─→ Reduce product quantities
   └─→ Clear cart

6. Track Order
   └─→ GET /orders/{id}
   └─→ Monitor status: pending → approved → packed → dispatched → delivered
```

#### Workflow 2: Item Request Flow

```
1. User Creates Request
   └─→ POST /item-requests
   └─→ Set status=pending

2. Admin Reviews
   └─→ GET /admin/item-requests (all pending)

3. Admin Assigns to Vendor
   └─→ PUT /item-requests/{id}/assign-vendor/{vendor_id}
   └─→ Set vendor_id and status=approved

4. Vendor Fulfills
   └─→ GET /vendor/item-requests (assigned to vendor)
   └─→ PUT /item-requests/{id}/fulfill
   └─→ Set status=fulfilled

5. User Tracks
   └─→ GET /item-requests/my-requests
   └─→ See status progression
```

#### Workflow 3: Order Status Update

```
Pending (initial)
   ↓ (Admin/Vendor updates)
Approved
   ↓ (Vendor packing)
Packed
   ↓ (Shipping)
Dispatched
   ↓ (Delivery)
Delivered (final)

Or: Cancelled (anytime before dispatch)
```

### Service Layer Methods

#### ProductService
```python
create_product(db, product_data, vendor_id)
get_product(db, product_id)
get_all_products(db, skip, limit, category, status)
get_vendor_products(db, vendor_id, skip, limit)
update_product(db, product_id, data, vendor_id)
delete_product(db, product_id, vendor_id)
update_quantity(db, product_id, quantity_change)
```

#### CartService
```python
get_or_create_cart(db, user_id)
add_to_cart(db, user_id, cart_item_data)
remove_from_cart(db, user_id, product_id)
update_cart_item(db, user_id, product_id, data)
get_cart(db, user_id)
clear_cart(db, user_id)
get_cart_summary(db, user_id)  # Returns total items & price
```

#### OrderService
```python
create_order_from_cart(db, user_id)
get_order(db, order_id)
get_order_by_number(db, order_number)
get_user_orders(db, user_id, skip, limit, status)
get_all_orders(db, skip, limit, status)  # Admin view
update_order_status(db, order_id, status)
cancel_order(db, order_id)  # Restores inventory
```

#### ItemRequestService
```python
create_request(db, user_id, request_data)
get_request(db, request_id)
get_user_requests(db, user_id, skip, limit, status)
get_pending_requests(db, skip, limit)
get_vendor_requests(db, vendor_id, skip, limit, status)
update_request_status(db, request_id, status_update)
assign_to_vendor(db, request_id, vendor_id)
fulfill_request(db, request_id)
```

---

## Deployment

### Development Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload --port 8000

# Access API
http://localhost:8000/api/docs
```

### Production Deployment

#### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

#### Using Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Environment Configuration
```env
# Production settings
DEBUG=False
SECRET_KEY=<use-strong-random-key>
DATABASE_URL=postgresql://user:pass@db.example.com/event_db
CORS_ORIGINS=["https://example.com"]
```

---

## Error Handling

### HTTP Status Codes
- **200**: Success
- **201**: Created
- **400**: Bad Request (validation error)
- **401**: Unauthorized (invalid token)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found (resource doesn't exist)
- **500**: Internal Server Error

### Example Error Response
```json
{
  "detail": "Invalid email or password"
}
```

---

## Future Enhancements

1. **Payment Integration**: Stripe/PayPal integration
2. **Email Notifications**: Order confirmations, status updates
3. **Analytics Dashboard**: Sales reports, vendor metrics
4. **Advanced Search**: Filters, faceted search
5. **Soft Delete**: Data retention for auditing
6. **Audit Logs**: Track all operations
7. **Webhooks**: Real-time event notifications
8. **GraphQL**: Alternative API layer
9. **Mobile App**: iOS/Android apps
10. **Real-time Updates**: WebSocket support

---

**Document Version**: 1.0
**Last Updated**: 2024
**Status**: Complete Production-Ready System
