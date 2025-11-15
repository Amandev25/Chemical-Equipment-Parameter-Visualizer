# 🧪 Test All API Endpoints

Your Backend URL: `https://chemical-equipment-parameter-visualizer-1.onrender.com`

---

## ✅ Quick Test - Run Python Script

### Option 1: Automated Test Script

1. **Install requests** (if not installed):
   ```bash
   pip install requests
   ```

2. **Run the test script**:
   ```bash
   python test_api_endpoints.py
   ```

This will test all endpoints automatically and show you which ones are working!

---

## ✅ Manual Testing (Browser/Postman)

### Public Endpoints (No Auth Required)

#### 1. Health Check ✅
```
GET https://chemical-equipment-parameter-visualizer-1.onrender.com/api/health/
```
**Expected:** `{"status": "healthy", ...}`

#### 2. CSRF Token ✅
```
GET https://chemical-equipment-parameter-visualizer-1.onrender.com/api/auth/csrf/
```
**Expected:** `{"csrfToken": "..."}`

#### 3. Swagger Documentation ✅
```
GET https://chemical-equipment-parameter-visualizer-1.onrender.com/swagger/
```
**Expected:** Swagger UI page

---

### Authentication Endpoints (No Auth Required)

#### 4. Register User
```
POST https://chemical-equipment-parameter-visualizer-1.onrender.com/api/auth/register/
Content-Type: application/json

{
  "username": "testuser123",
  "password": "testpass123",
  "password_confirm": "testpass123",
  "email": "test@example.com"
}
```

#### 5. Login
```
POST https://chemical-equipment-parameter-visualizer-1.onrender.com/api/auth/login/
Content-Type: application/json

{
  "username": "testuser123",
  "password": "testpass123"
}
```

**Note:** After login, you'll get a session cookie. Use it for authenticated requests.

---

### Protected Endpoints (Requires Authentication)

**Important:** These require you to be logged in. Test them from the frontend or use session cookies.

#### 6. Current User
```
GET https://chemical-equipment-parameter-visualizer-1.onrender.com/api/auth/me/
```
**Requires:** Session cookie from login

#### 7. Equipment List
```
GET https://chemical-equipment-parameter-visualizer-1.onrender.com/api/equipment/
```
**Requires:** Session cookie

#### 8. Equipment Types
```
GET https://chemical-equipment-parameter-visualizer-1.onrender.com/api/equipment/types/
```
**Requires:** Session cookie

#### 9. CSV Uploads List
```
GET https://chemical-equipment-parameter-visualizer-1.onrender.com/api/uploads/
```
**Requires:** Session cookie

#### 10. Dashboard Summary
```
GET https://chemical-equipment-parameter-visualizer-1.onrender.com/api/dashboard/summary/
```
**Requires:** Session cookie

#### 11. Flowrate Chart Data
```
GET https://chemical-equipment-parameter-visualizer-1.onrender.com/api/dashboard/flowrate-chart/
```
**Requires:** Session cookie

#### 12. Type Distribution Data
```
GET https://chemical-equipment-parameter-visualizer-1.onrender.com/api/dashboard/type-distribution/
```
**Requires:** Session cookie

---

## 🎯 Best Way to Test: Use Frontend

The easiest way to test all endpoints is through your frontend:

1. **Deploy frontend** (Vercel/Render)
2. **Visit frontend URL**
3. **Register/Login** → Tests auth endpoints
4. **Upload CSV** → Tests upload endpoint
5. **View Dashboard** → Tests dashboard endpoints
6. **View Visualization** → Tests equipment endpoints

---

## 🔍 Check Render Logs

1. Go to Render Dashboard
2. Click your backend service
3. Go to "Logs" tab
4. Look for:
   - ✅ `200` status codes → Endpoints working
   - ❌ `401` → Authentication needed (normal for protected endpoints)
   - ❌ `500` → Server error (check logs for details)
   - ❌ `404` → Endpoint not found

---

## ✅ Expected Results

### Public Endpoints (Should work immediately):
- ✅ `/api/health/` → 200 OK
- ✅ `/api/auth/csrf/` → 200 OK
- ✅ `/swagger/` → 200 OK

### Auth Endpoints (Should work):
- ✅ `/api/auth/register/` → 201 Created (or 400 if user exists)
- ✅ `/api/auth/login/` → 200 OK (with valid credentials)

### Protected Endpoints (Need authentication):
- ❌ `/api/auth/me/` → 401 Unauthorized (without login) ✅ 200 OK (with login)
- ❌ `/api/equipment/` → 401 Unauthorized (without login) ✅ 200 OK (with login)
- ❌ `/api/dashboard/summary/` → 401 Unauthorized (without login) ✅ 200 OK (with login)

**401 errors are NORMAL for protected endpoints when not logged in!**

---

## 🚀 Quick Test Commands

### Using curl (if you have it):

```bash
# Health check
curl https://chemical-equipment-parameter-visualizer-1.onrender.com/api/health/

# CSRF token
curl https://chemical-equipment-parameter-visualizer-1.onrender.com/api/auth/csrf/

# Register (will fail if user exists, but tests endpoint)
curl -X POST https://chemical-equipment-parameter-visualizer-1.onrender.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123","password_confirm":"test123"}'
```

---

**Run the Python test script for comprehensive testing!** 🧪

