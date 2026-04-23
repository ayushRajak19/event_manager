# Frontend API Integration Guide

## 🔌 API Connection Status

The frontend is now **fully integrated** with the FastAPI backend. All functions use actual API endpoints instead of mock data.

## 📡 API Base URL
```javascript
const API_BASE = 'http://localhost:8000/api/v1';
```

---

## 🔑 Authentication

### Login Endpoint
**Frontend Function:** `doLogin()`

**Endpoint:** 
- Admin: `POST /auth/admin/login`
- User: `POST /auth/user/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "user"
  }
}
```

**Token Storage:** Stored in `state.token` and used in all subsequent requests via Bearer token header.

---

## 👥 User Management (Admin Only)

### Get All Users
**Frontend Function:** `loadAdminData()`

**Endpoint:** `GET /users`

**Response:** Array of user objects
```json
[
  {
    "id": 1,
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone_number": "9876543210",
    "is_active": true,
    "role": "user"
  }
]
```

**Display:** Admin Dashboard → Members page

### Add New Member
**Frontend Function:** `saveMember()`

**Endpoint:** `POST /users`

**Request Body:**
```json
{
  "full_name": "Jane Smith",
  "email": "jane@example.com",
  "phone_number": "8765432109",
  "password": "TempPass@123",
  "role": "user"
}
```

**Response:** Created user object with ID

---

## 🎫 Membership Management

### Add Membership
**Frontend Function:** `submitAddMembership()`

**Endpoint:** `POST /memberships`

**Request Body:**
```json
{
  "user_id": 1,
  "full_name": "Jane Smith",
  "email": "jane@example.com",
  "phone_number": "8765432109",
  "duration_months": 6,
  "start_date": "2024-01-15T00:00:00",
  "status": "active"
}
```

**Response:** Membership object with `expiry_date`

### Extend Membership
**Frontend Function:** `submitUpdateMembership()` (when action = "extend")

**Endpoint:** `PUT /memberships/{membership_id}/extend`

**Request Body:**
```json
{
  "additional_months": 12
}
```

**Response:** Updated membership with new `expiry_date`

### Cancel Membership
**Frontend Function:** `submitUpdateMembership()` (when action = "cancel")

**Endpoint:** `DELETE /memberships/{membership_id}`

**Response:** Confirmation message

---

## 🔧 Maintenance Tasks (Admin Only)

### Get All Maintenance Tasks
**Frontend Function:** `loadAdminData()` (loads into `state.maintenance`)

**Endpoint:** `GET /maintenance` (if available)

**Response:** Array of maintenance tasks

### Add Maintenance Task
**Frontend Function:** `saveMaintenance()`

**Endpoint:** `POST /maintenance`

**Request Body:**
```json
{
  "title": "Facility Inspection",
  "scheduled_date": "2024-02-01",
  "status": "Scheduled"
}
```

**Response:** Created maintenance task object

---

## 💰 Orders & Transactions

### Get Admin Orders
**Frontend Function:** `loadAdminData()`

**Endpoint:** `GET /orders`

**Response:** Array of all orders

**Display:** Admin Dashboard → Transactions page

### Get User Orders
**Frontend Function:** `loadUserData()`

**Endpoint:** `GET /orders/my-orders`

**Response:** Array of user's orders

**Display:** User Dashboard → Transactions page

---

## 📊 Reports

### Member Report
**Frontend Function:** `generateReport('members')`

**Endpoint:** `GET /reports/members` (to be implemented)

### Transaction Report
**Frontend Function:** `generateReport('transactions')`

**Endpoint:** `GET /reports/transactions` (to be implemented)

---

## 🔄 Flow Diagrams

### Login Flow
```
User enters credentials
    ↓
doLogin() called
    ↓
POST /auth/{role}/login
    ↓
Receive access_token
    ↓
Store token in state.token
    ↓
Load role-specific data (loadAdminData / loadUserData)
    ↓
Navigate to dashboard
```

### Admin Member Management Flow
```
Admin clicks "Add Member"
    ↓
openAddMember() modal
    ↓
Admin fills form (name, email, phone)
    ↓
saveMember() called
    ↓
POST /users with form data
    ↓
New user added to state.members
    ↓
showAdminPage('members') refreshes table
```

### User Membership Flow
```
User clicks "Add Membership"
    ↓
showAddMembership() modal
    ↓
Select duration (6m, 1y, 2y) - Default: 6 months
    ↓
submitAddMembership() called
    ↓
POST /memberships with details
    ↓
Membership created
    ↓
Update state.user.membership_expiry
    ↓
Show success message
```

---

## 🛡️ Error Handling

All API calls are wrapped in `apiCall()` helper function which:
1. Adds Authorization header with Bearer token
2. Checks response status
3. Parses errors and shows toast notification
4. Throws error for catch blocks

```javascript
async function apiCall(endpoint, options = {}) {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${state.token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(error.detail || `API Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    toast(`Error: ${error.message}`, 'error');
    throw error;
  }
}
```

---

## 📋 Data Synchronization

### Initial Load
When user logs in:
1. **Admin:** `loadAdminData()` fetches users and orders
2. **User:** `loadUserData()` fetches their orders

### Real-time Updates
- Adding member → `state.members` updated
- Adding maintenance → `state.maintenance` updated
- Creating membership → `state.user.membership_expiry` updated

---

## ✅ Feature Checklist

- [x] Login with JWT tokens
- [x] Admin dashboard with real data
- [x] Member management (CRUD)
- [x] Membership add functionality
- [x] Membership update/extend functionality
- [x] Membership cancel functionality
- [x] Maintenance task creation
- [x] Transaction/Order viewing
- [x] Error handling & logging
- [x] Toast notifications for feedback
- [ ] Reports generation (pending backend)
- [ ] Real-time data refresh
- [ ] Pagination for large datasets

---

## 🚀 Testing the Integration

### 1. Start Backend Server
```bash
cd event_manager
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### 2. Open Frontend
```
file:///C:/Users/Administrator/OneDrive/Desktop/event_manager/frontend/index.html
```
Or with Python server:
```bash
cd frontend
python -m http.server 8001
# Visit: http://localhost:8001
```

### 3. Test Login
- Select Admin role
- Email: `admin@eventmgmt.com`
- Password: `Admin@123`
- Check browser console for API calls (F12 → Network tab)

### 4. Monitor API Calls
- Open DevTools (F12)
- Go to Network tab
- Perform actions (login, add member, create task)
- See API calls and responses

---

## 🔗 Related Files

- **Backend:** `/app/api/routes/` (all endpoint implementations)
- **Database Models:** `/app/models/`
- **Frontend:** `/frontend/index.html`

---

## 📞 Support

For API issues:
1. Check backend console for errors
2. Verify token is being sent in headers
3. Check response status codes (401 = auth error, 404 = not found, 500 = server error)
4. Enable browser DevTools Network tab to debug
