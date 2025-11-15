# 🧪 How to Test Your Deployed API

Quick guide to verify your API is working after deployment.

---

## ✅ Method 1: Health Check (Easiest)

### In Browser
1. Open your backend URL in browser:
   ```
   https://your-backend.onrender.com/api/health/
   ```
   Or if using Railway:
   ```
   https://your-backend.railway.app/api/health/
   ```

2. **Expected Response:**
   ```json
   {
     "status": "healthy",
     "message": "Chemical Equipment Visualizer API is running",
     "version": "1.0.0"
   }
   ```

3. ✅ **If you see this JSON** → API is working!

---

## ✅ Method 2: Test Authentication Endpoints

### Test CSRF Token Endpoint
```
https://your-backend.onrender.com/api/auth/csrf/
```

**Expected Response:**
```json
{
  "csrfToken": "some-token-here"
}
```

### Test Login (Will fail without credentials, but should return 400, not 500)
```
POST https://your-backend.onrender.com/api/auth/login/
```

**Expected Response (without credentials):**
```json
{
  "error": "Username and password are required"
}
```

✅ **If you get a proper error message** → API is working!

---

## ✅ Method 3: Using Browser DevTools

1. **Open your frontend URL** (Vercel/Render)
2. **Open Browser DevTools** (F12)
3. **Go to "Network" tab**
4. **Try to register/login**
5. **Check the API calls:**
   - Look for requests to `/api/auth/login/` or `/api/auth/register/`
   - Status should be `200` (success) or `400` (bad request), NOT `500` (server error)
   - Click on the request to see the response

---

## ✅ Method 4: Using curl (Command Line)

### Health Check
```bash
curl https://your-backend.onrender.com/api/health/
```

### Test CSRF Token
```bash
curl https://your-backend.onrender.com/api/auth/csrf/
```

### Test Login (Should return error without credentials)
```bash
curl -X POST https://your-backend.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected:** Error message about missing username/password

---

## ✅ Method 5: Test from Frontend

1. **Visit your frontend URL**
2. **Try to register a new account:**
   - Fill in username, password
   - Click "Register"
   - Should either:
     - ✅ Success: Redirect to dashboard
     - ❌ Error: Show error message (but API is responding)

3. **If you see an error message** → API is working, just need to fix the issue
4. **If page hangs/doesn't respond** → API might not be working

---

## ✅ Method 6: Check API Documentation

Visit Swagger UI:
```
https://your-backend.onrender.com/swagger/
```

**Expected:**
- Should show API documentation
- Can see all endpoints
- Can test endpoints directly

---

## 🔍 Check Render Logs

1. **Go to Render Dashboard**
2. **Click on your backend service**
3. **Go to "Logs" tab**
4. **Look for:**
   - ✅ `Listening on 0.0.0.0:xxxx` → Server is running
   - ✅ `System check identified no issues` → Django is healthy
   - ✅ `Starting development server` or `Booting worker` → Gunicorn started
   - ❌ Any red errors → Something is wrong

---

## 🆘 Common Issues

### "Application Error" or "Service Unavailable"
- **Check logs** in Render dashboard
- **Verify environment variables** are set
- **Check database connection**

### "404 Not Found" on `/api/health/`
- **Check URL** - make sure it ends with `/api/health/`
- **Verify service is deployed** and running
- **Check logs** for routing errors

### "500 Internal Server Error"
- **Check logs** - this shows the actual error
- **Common causes:**
  - Database connection failed
  - Missing environment variables
  - Import errors

### CORS Errors in Browser
- **Update CORS settings** in backend
- **Add frontend URL** to `CORS_ALLOWED_ORIGINS`
- **Redeploy backend**

---

## ✅ Quick Test Checklist

- [ ] Health endpoint returns JSON
- [ ] CSRF endpoint returns token
- [ ] Frontend can connect to backend
- [ ] Can register new user
- [ ] Can login
- [ ] No 500 errors in logs
- [ ] Swagger UI loads

---

## 🎯 Expected Working State

When everything is working:
1. ✅ Health check returns `{"status": "healthy"}`
2. ✅ Frontend loads without errors
3. ✅ Can register/login
4. ✅ Can upload CSV files
5. ✅ Dashboard shows data
6. ✅ No CORS errors in browser console

---

**If health check works, your API is deployed correctly!** 🎉

