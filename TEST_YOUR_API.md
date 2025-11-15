# 🧪 Test Your API - Quick Guide

Your Backend URL: `https://chemical-equipment-parameter-visualizer-1.onrender.com`

---

## ✅ Quick Tests (Copy & Paste in Browser)

### 1. Health Check (Should work immediately)
```
https://chemical-equipment-parameter-visualizer-1.onrender.com/api/health/
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "Chemical Equipment Visualizer API is running",
  "version": "1.0.0"
}
```

### 2. API Documentation (Swagger)
```
https://chemical-equipment-parameter-visualizer-1.onrender.com/swagger/
```

**Expected:** Interactive API documentation page

### 3. CSRF Token Endpoint
```
https://chemical-equipment-parameter-visualizer-1.onrender.com/api/auth/csrf/
```

**Expected Response:**
```json
{
  "csrfToken": "some-token-string"
}
```

---

## 🔍 What to Check

### ✅ If Health Check Works:
- Your API is deployed and running! ✅
- Server is responding
- Django is working

### ❌ If You Get Errors:

**"Application Error" or "Service Unavailable":**
- Service might be spinning up (free tier takes ~30 seconds on first request)
- Check Render logs for errors
- Verify environment variables are set

**"404 Not Found":**
- Check the URL - should end with `/api/health/`
- Verify the service is deployed

**"500 Internal Server Error":**
- Check Render logs
- Common issues:
  - Database connection failed
  - Missing environment variables
  - Import errors

---

## 🎯 Next Steps After Health Check Works

1. **Test Frontend Connection:**
   - Make sure frontend URL is in `CORS_ALLOWED_ORIGINS`
   - Visit frontend and try to register/login

2. **Test Authentication:**
   - Try registering a new user
   - Try logging in

3. **Test CSV Upload:**
   - Upload a CSV file
   - Check if it processes correctly

---

## 📝 Your API Endpoints

Base URL: `https://chemical-equipment-parameter-visualizer-1.onrender.com/api`

- Health: `/api/health/`
- Register: `/api/auth/register/`
- Login: `/api/auth/login/`
- Current User: `/api/auth/me/`
- Logout: `/api/auth/logout/`
- Equipment List: `/api/equipment/`
- Upload CSV: `/api/uploads/`
- Dashboard Summary: `/api/dashboard/summary/`
- Swagger Docs: `/swagger/`

---

**Start with the health check URL above!** 🚀

