# Quick Reference Card - Event Management System

## 🚀 Start Development in 5 Minutes

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate (choose based on OS)
source venv/bin/activate          # macOS/Linux
venv\Scripts\activate              # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Seed database
python seed_data.py

# 5. Run server
uvicorn app.main:app --reload

# 6. Open browser
http://localhost:8000/api/docs
```

---

## 📝 Sample Credentials

```
ADMIN
  Email: admin@eventmgmt.com
  Password: Admin@123

USER
  Email: john@example.com
  Password: User@123

VENDOR
  Email: vendor1@eventmgmt.com
  Password: Vendor@123
```

---

## 🌐 API Endpoints Quick Map

### Auth (5 endpoints)
```
POST   /api/v1/auth/admin/signup        - Admin registration
POST   /api/v1/auth/admin/login         - Admin login
POST   /api/v1/auth/user/signup         - User registration
POST   /api/v1/auth/user/login          - User login
POST   /api/v1/auth/vendor/login        - Vendor login
```

### Products (4 endpoints)
```
GET    /api/v1/products                 - List all products
GET    /api/v1/products/{id}            - Get product details
GET    /api/v1/products/category/{cat}  - Filter by category
GET    /api/v1/products/search          - Search products
```

### Cart (6 endpoints)
```
GET    /api/v1/cart                     - View cart
POST   /api/v1/cart/add                 - Add to cart
PUT    /api/v1/cart/update/{item_id}    - Update quantity
DELETE /api/v1/cart/remove/{item_id}    - Remove from cart
GET    /api/v1/cart/summary             - Get summary
DELETE /api/v1/cart/clear               - Clear cart
```

### Orders (5 endpoints)
```
GET    /api/v1/orders/my-orders         - View my orders
GET    /api/v1/orders/{id}              - Get order details
PUT    /api/v1/orders/{id}/cancel       - Cancel order
GET    /api/v1/orders/track/{id}        - Track order
PUT    /api/v1/orders/{id}/status       - Update status
```

### Item Requests (7 endpoints)
```
POST   /api/v1/item-requests            - Create request
GET    /api/v1/item-requests/my-requests - View my requests
GET    /api/v1/item-requests/{id}       - Get request details
PUT    /api/v1/item-requests/{id}/status - Update status
PUT    /api/v1/item-requests/{id}/assign - Assign to vendor
PUT    /api/v1/item-requests/{id}/fulfill - Mark fulfilled
GET    /api/v1/item-requests/all        - View all (admin only)
```

### Admin (9 endpoints)
```
GET    /api/v1/admin/dashboard          - Dashboard stats
GET    /api/v1/admin/users              - List users
GET    /api/v1/admin/vendors            - List vendors
GET    /api/v1/admin/orders             - View all orders
GET    /api/v1/admin/requests           - View all requests
PUT    /api/v1/admin/users/{id}         - Update user
PUT    /api/v1/admin/vendors/{id}       - Update vendor
DELETE /api/v1/admin/users/{id}         - Deactivate user
DELETE /api/v1/admin/vendors/{id}       - Deactivate vendor
```

### Vendor (8 endpoints)
```
GET    /api/v1/vendor/dashboard         - Vendor dashboard
POST   /api/v1/vendor/products          - Create product
GET    /api/v1/vendor/products          - View my products
PUT    /api/v1/vendor/products/{id}     - Update product
DELETE /api/v1/vendor/products/{id}     - Delete product
GET    /api/v1/vendor/item-requests     - View requests
PUT    /api/v1/vendor/orders/{id}/status - Update order status
GET    /api/v1/vendor/analytics         - View analytics
```

### User (2 endpoints)
```
GET    /api/v1/users/profile            - Get profile
PUT    /api/v1/users/profile            - Update profile
```

### Checkout (2 endpoints)
```
POST   /api/v1/checkout/place-order     - Create order from cart
GET    /api/v1/checkout/success/{id}    - Order confirmation
```

---

## 📂 File Structure Reference

```
Root Files
  .env                  - Environment configuration
  .gitignore           - Git ignore rules
  requirements.txt     - Python dependencies
  seed_data.py         - Sample data generator

App Files (app/)
  main.py              - FastAPI entry point
  config.py            - Configuration
  
Authentication (app/core/)
  security.py          - JWT & password utilities
  roles.py             - Authorization checks
  
Database (app/db/)
  base.py              - SQLAlchemy base
  session.py           - Database session
  
Models (app/models/)
  enums.py             - Role & status enums
  admin.py             - Admin model
  user.py              - User model
  vendor.py            - Vendor model
  product.py           - Product model
  cart.py              - Cart models
  order.py             - Order models
  item_request.py      - Item request model
  
Schemas (app/schemas/)
  auth.py              - Auth schemas
  product.py           - Product schemas
  cart.py              - Cart schemas
  order.py             - Order schemas
  item_request.py      - Request schemas
  
Services (app/services/)
  auth_service.py      - Auth logic
  product_service.py   - Product logic
  cart_service.py      - Cart logic
  order_service.py     - Order logic
  item_request_service.py - Request logic
  
Routes (app/api/routes/)
  auth.py              - Auth endpoints
  admins.py            - Admin endpoints
  vendors.py           - Vendor endpoints
  users.py             - User endpoints
  products.py          - Product endpoints
  carts.py             - Cart endpoints
  checkout.py          - Checkout endpoints
  orders.py            - Order endpoints
  item_requests.py     - Request endpoints

Tests (tests/)
  test_api.py          - Test examples

Documentation
  README.md            - Full documentation
  QUICKSTART.md        - Fast setup
  INSTALLATION.md      - Installation guide
  SYSTEM_DESIGN.md     - Architecture
  PROJECT_SUMMARY.md   - File listing
  DELIVERY_COMPLETE.md - Delivery summary
  QUICK_REFERENCE.md   - This file
  Event_Management_API.postman_collection.json - Postman tests
```

---

## 🧪 Test API Quickly

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Signup
curl -X POST http://localhost:8000/api/v1/auth/user/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
    "email": "test@example.com",
    "password": "Test@12345",
    "phone": "1234567890"
  }'

# Get token from response, then:

# Get products
curl -X GET http://localhost:8000/api/v1/products \
  -H "Authorization: Bearer <token>"
```

### Using Postman

1. Import `Event_Management_API.postman_collection.json`
2. Set base_url to `http://localhost:8000`
3. Login endpoint will auto-set token
4. All other endpoints ready to use

### Using Swagger UI

1. Open http://localhost:8000/api/docs
2. Click "Authorize" button
3. Login with sample credentials
4. Try any endpoint

---

## 🔧 Common Commands

```bash
# Start server
uvicorn app.main:app --reload

# Start on different port
uvicorn app.main:app --reload --port 8001

# Run tests
pytest

# Seed database
python seed_data.py

# Reset database
rm event_manager.db && python seed_data.py

# Activate virtual environment
source venv/bin/activate          # macOS/Linux
venv\Scripts\activate              # Windows

# Deactivate
deactivate

# Install new package
pip install package_name

# View installed packages
pip list
```

---

## 📊 Database Commands

```bash
# Connect to SQLite
sqlite3 event_manager.db

# Inside sqlite3 shell:
.tables                           # View all tables
.schema users                     # View table structure
SELECT * FROM users;              # View all users
SELECT COUNT(*) FROM orders;      # Count orders
.quit                             # Exit

# Backup database
cp event_manager.db event_manager.db.backup

# Restore from backup
cp event_manager.db.backup event_manager.db
```

---

## 🔐 Authentication Flow

1. **User Signup**
   ```
   POST /auth/user/signup
   → Returns: { access_token, token_type, user_id, email, role }
   ```

2. **Use Token in Requests**
   ```
   Authorization: Bearer <access_token>
   ```

3. **Token Auto-validates**
   - JWT verified
   - Role checked
   - Permissions enforced

4. **Token Expires in 60 minutes**
   - Login again for new token

---

## 🗄️ Database Tables

```
admins          - Admin users (1 field + timestamps)
users           - Regular users (5 fields + timestamps)
vendors         - Vendor accounts (5 fields + timestamps)
products        - Product catalog (7 fields + timestamps)
carts           - Shopping carts (2 fields + timestamps)
cart_items      - Cart contents (3 fields)
orders          - Customer orders (5 fields + timestamps)
order_items     - Order contents (3 fields)
item_requests   - Special requests (7 fields + timestamps)
```

---

## 🎯 Role Permissions

### Admin Can:
- View all users
- Manage vendors
- View all orders
- Handle item requests
- Assign requests to vendors
- View system analytics

### Vendor Can:
- Create products
- Manage inventory
- View assigned requests
- Update order fulfillment status
- View vendor analytics

### User Can:
- Browse products
- Manage shopping cart
- Create orders
- Track orders
- Request special items
- Track request status

---

## 🚀 Environment Variables

```
DATABASE_URL=sqlite:///./event_manager.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=["http://localhost:3000"]
DB_ECHO=False
```

---

## 📈 Key API Status Codes

```
200 - Success
201 - Created
400 - Bad request
401 - Unauthorized
403 - Forbidden
404 - Not found
422 - Validation error
500 - Server error
```

---

## 💡 Pro Tips

1. **Always use Authorization header:**
   ```
   Authorization: Bearer <your_token>
   ```

2. **Check token expiry:**
   - Tokens expire after 60 minutes
   - Get new token by logging in again

3. **Use Swagger UI for testing:**
   - http://localhost:8000/api/docs
   - Click "Authorize" to auto-set token

4. **Check error messages:**
   - Response includes detailed error info
   - Use for debugging

5. **Pagination available:**
   - Add `?skip=0&limit=10` to endpoints
   - Default: 10 items per page

---

## 🐛 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Activate venv, reinstall requirements |
| `Address already in use` | Use different port: `--port 8001` |
| `Invalid token` | Login again to get new token |
| `database is locked` | Delete db, run `python seed_data.py` |
| `Unauthorized (401)` | Check Authorization header has token |
| `Forbidden (403)` | Check user role has permission |

---

## 📚 Documentation Files

| File | Use For |
|------|---------|
| README.md | Complete reference |
| QUICKSTART.md | Fast setup |
| INSTALLATION.md | Detailed setup |
| SYSTEM_DESIGN.md | Architecture |
| PROJECT_SUMMARY.md | File listing |
| DELIVERY_COMPLETE.md | What you got |
| QUICK_REFERENCE.md | This file |

---

## ✅ Before First Use

- [ ] Create virtual environment
- [ ] Activate virtual environment
- [ ] Install requirements
- [ ] Run seed_data.py
- [ ] Start server
- [ ] Access http://localhost:8000/api/docs
- [ ] Test login

**Time required: ~5 minutes**

---

**Quick Tip**: When stuck, check the comprehensive documentation files provided!

**Need Setup Help?** → Read INSTALLATION.md
**Need Architecture Details?** → Read SYSTEM_DESIGN.md
**Need Full API Reference?** → Visit http://localhost:8000/api/docs

---

**Happy Coding! 🚀**
