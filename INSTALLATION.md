# Installation & Startup Guide - Event Management System

## 🎯 Complete Setup Instructions

Follow these step-by-step instructions to get the Event Management System running on your machine.

---

## Prerequisites

### System Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **Disk Space**: ~500MB
- **RAM**: 2GB minimum

### Check Python Installation

```bash
# Check Python version
python --version

# Check pip installation
pip --version

# Should show Python 3.8+ and pip version
```

---

## Step 1: Environment Setup

### 1.1 Navigate to Project Directory

```bash
cd event_manager
```

### 1.2 Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
```

**On macOS/Linux:**
```bash
python3 -m venv venv
```

### 1.3 Activate Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

After activation, your terminal prompt should show `(venv)` at the beginning.

---

## Step 2: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Verify installation
pip list

# Should show: fastapi, sqlalchemy, python-jose, passlib, pydantic, etc.
```

**Installation Time**: 2-5 minutes (depending on internet speed)

### Troubleshooting Installation Issues

#### Issue: "ModuleNotFoundError" or "No module named"
```bash
# Ensure virtual environment is activated
# Then reinstall
pip install -r requirements.txt --force-reinstall
```

#### Issue: Permission denied on macOS/Linux
```bash
# Use --user flag
pip install --user -r requirements.txt
```

#### Issue: Slow installation
```bash
# Use a different PyPI index
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

---

## Step 3: Initialize Database

### 3.1 Seed Database with Sample Data

```bash
python seed_data.py
```

**Expected Output:**
```
🌱 Seeding database with sample data...
  ✓ Creating admin...
  ✓ Creating users...
  ✓ Creating vendors...
  ✓ Creating products...
  ✓ Creating orders...
  ✓ Creating item requests...

✅ Database seeding completed successfully!

Sample Credentials:
  Admin:
    Email: admin@eventmgmt.com
    Password: Admin@123

  User Examples:
    Email: john@example.com
    Password: User@123

  Vendor Examples:
    Email: vendor1@eventmgmt.com
    Password: Vendor@123

📊 Data Created:
  - Admins: 1
  - Users: 3
  - Vendors: 3
  - Products: 9
  - Orders: 2
  - Item Requests: 3
```

### 3.2 Verify Database Creation

**On Windows (PowerShell):**
```powershell
Get-Item -Path "event_manager.db"
```

**On macOS/Linux:**
```bash
ls -lh event_manager.db
```

Should show a file ~50-100KB in size.

---

## Step 4: Run the Application

### 4.1 Start Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
✓ Technical Event Management System started successfully
✓ Database initialized
✓ API Documentation available at http://localhost:8000/api/docs
INFO:     Application startup complete [0.45s]
```

### 4.2 Verify Server is Running

Open in browser or terminal:

```bash
# Check health endpoint
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","app_name":"Technical Event Management System","version":"1.0.0"}
```

---

## Step 5: Access API Documentation

### Interactive API Documentation (Swagger UI)

Open in browser:
```
http://localhost:8000/api/docs
```

**Features:**
- Try API endpoints
- See request/response schemas
- View parameter descriptions
- Test with real data

### Alternative Documentation (ReDoc)

Open in browser:
```
http://localhost:8000/api/redoc
```

**Features:**
- Beautiful documentation
- Full endpoint reference
- Search functionality
- Mobile-friendly

---

## 🧪 First API Test

### Test 1: Health Check

**Using cURL:**
```bash
curl http://localhost:8000/health
```

### Test 2: User Signup

**Using cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/user/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "testuser@example.com",
    "password": "Test@12345",
    "phone": "9876543210"
  }'
```

**Expected Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 4,
  "email": "testuser@example.com",
  "role": "user"
}
```

### Test 3: Get Products (Requires Authentication)

```bash
# Replace TOKEN with actual token from signup
curl -X GET http://localhost:8000/api/v1/products \
  -H "Authorization: Bearer TOKEN"
```

---

## 📊 Database Management

### View SQLite Database

**Using Python:**
```bash
python -c "
import sqlite3
conn = sqlite3.connect('event_manager.db')
cursor = conn.cursor()

# List all tables
cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")
tables = cursor.fetchall()
print('Tables:', [t[0] for t in tables])

# Count records in users table
cursor.execute('SELECT COUNT(*) FROM users')
print('Total users:', cursor.fetchone()[0])
"
```

**Using sqlite3 CLI:**
```bash
sqlite3 event_manager.db

# Inside sqlite3:
.tables              # List all tables
SELECT * FROM users; # View users
.schema users        # View table structure
.quit                # Exit
```

### Backup Database

```bash
# Create backup
cp event_manager.db event_manager.db.backup

# Restore from backup
cp event_manager.db.backup event_manager.db
```

### Reset Database

```bash
# Delete current database
rm event_manager.db

# Recreate with fresh data
python seed_data.py
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app tests/
```

### Using Postman for Testing

1. **Import Postman Collection**
   - Open Postman
   - Click "Import"
   - Select `Event_Management_API.postman_collection.json`

2. **Set Variables**
   - Go to "Environments"
   - Create new environment
   - Add variables:
     - `base_url`: `http://localhost:8000`
     - `access_token`: (leave empty, will auto-fill)
     - `admin_token`: (leave empty, will auto-fill)

3. **Test Endpoints**
   - Click "Send" on any endpoint
   - Responses appear in "Response" tab

---

## 🚨 Troubleshooting

### Server Won't Start

**Error**: `Address already in use`
```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```

**Error**: `ModuleNotFoundError: No module named 'app'`
```bash
# Ensure you're in project root directory
cd event_manager

# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows
```

**Error**: `CORS policy error`
- Ensure CORS is configured in `.env`
- Check `CORS_ORIGINS` setting

### Database Issues

**Error**: `database is locked`
```bash
# Delete database and reinitialize
rm event_manager.db
python seed_data.py
```

**Error**: `table already exists`
```bash
# Tables auto-create, just reset database
rm event_manager.db
python seed_data.py
```

### Authentication Issues

**Error**: `Invalid token`
```
Cause: Token expired or corrupted
Solution: Login again to get new token
```

**Error**: `Unauthorized (401)`
```
Cause: No token in Authorization header
Solution: Add header: Authorization: Bearer <token>
```

**Error**: `Forbidden (403)`
```
Cause: User doesn't have permission for endpoint
Solution: Check user role and endpoint requirements
```

### Import Errors

**Error**: `No module named 'sqlalchemy'`
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Error**: `No module named 'fastapi'`
```bash
# Make sure virtual environment is activated
# Reinstall
pip install fastapi uvicorn
```

---

## 🔍 Verify Installation

Run this checklist to confirm everything works:

```bash
# 1. Check Python version
python --version
# Output: Python 3.8.0 or higher ✓

# 2. Check virtual environment activated
pip list | grep fastapi
# Output: fastapi        0.104.1 ✓

# 3. Check database exists
ls -l event_manager.db
# Output: file size > 0 ✓

# 4. Check server starts
uvicorn app.main:app --reload &
# Wait 2 seconds, then:

# 5. Check health endpoint
curl http://localhost:8000/health
# Output: {"status":"healthy",...} ✓

# 6. Kill server
pkill -f uvicorn
```

---

## 📝 Common Commands Reference

```bash
# Activate virtual environment
source venv/bin/activate         # macOS/Linux
venv\Scripts\activate            # Windows

# Install dependencies
pip install -r requirements.txt

# Seed database
python seed_data.py

# Run development server
uvicorn app.main:app --reload --port 8000

# Run production server
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app

# Run tests
pytest
pytest --cov=app tests/

# Check for linting issues
flake8 app/

# Format code
black app/

# Deactivate virtual environment
deactivate
```

---

## 📚 Documentation Quick Links

```
README.md              - Full project documentation
QUICKSTART.md          - 5-minute setup guide
SYSTEM_DESIGN.md       - System architecture & design
PROJECT_SUMMARY.md     - Complete file listing
API Docs (Swagger)     - http://localhost:8000/api/docs
```

---

## 🆘 Getting Help

### If Server Won't Start
1. Check Python version: `python --version`
2. Check virtual environment: Should show `(venv)` in prompt
3. Check dependencies: `pip list | grep fastapi`
4. Read error message carefully
5. Try resetting: Delete `event_manager.db` and `python seed_data.py`

### If Tests Fail
1. Ensure dependencies installed: `pip install -r requirements.txt`
2. Check database exists: `ls event_manager.db`
3. Run with verbose: `pytest -v`

### If API Returns Errors
1. Check Authorization header: `Authorization: Bearer <token>`
2. Verify token not expired (expires in 60 min)
3. Check user role has permission
4. Check request body format (JSON)

---

## ✅ Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database seeded (`python seed_data.py`)
- [ ] Server starts without errors (`uvicorn app.main:app --reload`)
- [ ] Health endpoint responds (`curl http://localhost:8000/health`)
- [ ] Can access API docs (http://localhost:8000/api/docs)
- [ ] Can login with sample credentials
- [ ] Can get products (requires token)

---

## 🎉 You're All Set!

If you've completed all steps above, your Event Management System is ready to use!

### Next Steps

1. **Explore API Docs**: Open http://localhost:8000/api/docs
2. **Test Endpoints**: Use Postman collection or Swagger UI
3. **Review Code**: Check out files in `app/` directory
4. **Customize**: Modify `.env` for your needs
5. **Deploy**: Follow production deployment in README.md

---

## 📞 Support Resources

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **Code Comments**: Comprehensive comments in all files
- **README.md**: Detailed documentation
- **SYSTEM_DESIGN.md**: Technical architecture details

---

**Happy Coding! 🚀**
