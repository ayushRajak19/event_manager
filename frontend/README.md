# Frontend - TechEvent Hub

Modern, responsive web interface for the Technical Event Management System.

## 📁 Files

- **index.html** - Complete single-page application with:
  - Admin Dashboard
  - User Portal  
  - Vendor Management
  - Product Catalog
  - Shopping Cart
  - Order Tracking
  - Item Requests

## 🚀 Getting Started

### Option 1: Direct File Access
Simply open the file in your browser:
```
file:///C:/Users/Administrator/OneDrive/Desktop/event_manager/frontend/index.html
```

### Option 2: Local Web Server (Recommended)

**Using Python:**
```bash
cd frontend
python -m http.server 8001
```

**Using Node.js:**
```bash
cd frontend
npx http-server
```

Then visit: **http://localhost:8001** (or your server port)

## 🔌 API Integration

The frontend is configured to communicate with your FastAPI backend:

```javascript
const API_BASE = 'http://localhost:8000/api/v1';
```

Make sure your backend is running:
```bash
# In another terminal
uvicorn app.main:app --reload --port 8000
```

## 👤 Sample Login Credentials

### Admin
- Email: `admin@eventmgmt.com`
- Password: `Admin@123`

### User
- Email: `john@example.com`
- Password: `User@123`

### Vendor
- Email: `vendor1@eventmgmt.com`
- Password: `Vendor@123`

## 🎨 Features

### Authentication
- ✅ Role-based login (Admin, User, Vendor)
- ✅ User signup support
- ✅ JWT token management (ready for API integration)

### Admin Dashboard
- Dashboard with statistics
- Product inventory management
- User and vendor management
- Order tracking
- Item request handling

### User Portal
- Browse products with filtering/search
- Shopping cart with quantity management
- Order summary with GST calculation
- Order tracking (ready for API)
- Item request submission
- My orders view

### Vendor Portal
- Vendor dashboard
- Product management
- Order management
- Item request handling

## 🔄 API Integration Status

The frontend is **ready for full API integration**. Currently it uses local state management, but the following endpoints are mapped:

### Ready to Connect:
- `POST /auth/user/signup` - User registration
- `POST /auth/user/login` - User login
- `POST /auth/admin/login` - Admin login
- `POST /auth/vendor/login` - Vendor login
- `GET /products` - Get all products
- `GET /products/{id}` - Get product details
- `POST /cart/add` - Add to cart
- `GET /cart` - View cart
- `POST /checkout/place-order` - Create order
- `GET /orders/my-orders` - Get user orders
- `POST /item-requests` - Create item request
- And more...

## 📱 Responsive Design

The interface is fully responsive:
- Desktop: Full layout with all features
- Tablet: Optimized grid layouts
- Mobile: Touch-friendly navigation

## 🎯 Customization

### Change Backend URL
Edit the API_BASE in the script:
```javascript
const API_BASE = 'http://your-api-url:8000/api/v1';
```

### Update Sample Data
Modify the `state.products` array to change displayed products.

### Styling
All styles use CSS variables defined in `:root`. Modify them to match your brand:
```css
--accent: #6c63ff;
--bg: #0a0a0f;
/* ... etc */
```

## 🔐 Security Notes

- Current implementation uses local state management for demo
- For production:
  - Implement proper JWT token storage (HttpOnly cookies)
  - Add HTTPS enforcement
  - Implement CORS with backend
  - Add input validation
  - Secure API communication

## 📋 Checklist

- [x] Complete UI/UX design
- [x] All 3 role-based dashboards
- [x] Shopping cart with calculations
- [x] Product filtering and search
- [x] Responsive design
- [x] Toast notifications
- [x] Modal windows
- [x] Form validation setup
- [ ] Full API integration
- [ ] Token management
- [ ] Error handling
- [ ] Loading states

## 🚀 Next Steps

1. **Backend Connection**: Update API_BASE and implement actual API calls
2. **Token Management**: Implement JWT storage and refresh logic
3. **Error Handling**: Add try-catch blocks for all API calls
4. **Loading States**: Add spinners during API requests
5. **Deployment**: Set up frontend hosting (Vercel, Netlify, GitHub Pages, etc.)

## 📞 Support

For API documentation, see the backend README.md or visit:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 📄 License

Part of TechEvent Hub - Technical Event Management System
