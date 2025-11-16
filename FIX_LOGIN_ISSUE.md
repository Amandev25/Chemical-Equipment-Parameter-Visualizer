# 🔧 Fix Login Not Working

## Quick Diagnostic Steps

### Step 1: Check Browser Console (Most Important!)
1. Open your Vercel frontend URL
2. Press **F12** (or right-click → Inspect)
3. Go to **Console** tab
4. Try to login
5. **Look for red error messages** - what do you see?

### Step 2: Check Network Requests
1. Press **F12** → **Network** tab
2. Try to login
3. Find the request to `/api/auth/login/` or `/auth/login/`
4. Click on it
5. Check:
   - **Status Code**: What number? (200 = success, 403/401/500 = error)
   - **Response** tab: What error message?
   - **Request Headers**: Is `X-CSRFToken` present?

---

## Common Issues & Fixes

### Issue 1: "Network Error" or "Failed to fetch"
**Problem:** Frontend can't reach backend

**Fix:**
1. Go to **Vercel Dashboard** → Your project → **Settings** → **Environment Variables**
2. Check `VITE_API_URL`:
   - Should be: `https://chemical-equipment-parameter-visualizer-1.onrender.com/api`
   - Make sure it ends with `/api`
3. **Redeploy** frontend after updating

### Issue 2: 403 Forbidden
**Problem:** CSRF or CORS issue

**Fix:**
1. Go to **Render Dashboard** → Your service → **Environment** tab
2. Check these variables:
   - `CORS_ALLOWED_ORIGINS` = `https://your-vercel-url.vercel.app` (NO trailing slash!)
   - `CSRF_TRUSTED_ORIGINS` = `https://your-vercel-url.vercel.app` (NO trailing slash!)
3. **Save** and wait for redeploy

### Issue 3: 401 Unauthorized
**Problem:** Wrong credentials or user doesn't exist

**Fix:**
1. **Try registering first:**
   - Click "Don't have an account? Register"
   - Create a new account
   - Then login with that account
2. Make sure password is at least 6 characters

### Issue 4: CORS Error in Console
**Problem:** Backend blocking frontend requests

**Fix:**
1. Check `CORS_ALLOWED_ORIGINS` in Render
2. Make sure it matches your **exact** Vercel URL
3. No trailing slash!
4. Redeploy backend

### Issue 5: No Error Message Shown
**Problem:** Error might be silent

**Fix:**
1. Check browser console (F12)
2. Check Network tab for failed requests
3. Try registering a new account first

---

## Quick Test Checklist

✅ **Backend is running?**
- Visit: `https://chemical-equipment-parameter-visualizer-1.onrender.com/api/health/`
- Should return: `{"status": "healthy"}`

✅ **Vercel Environment Variable set?**
- `VITE_API_URL` = `https://chemical-equipment-parameter-visualizer-1.onrender.com/api`

✅ **Render CORS configured?**
- `CORS_ALLOWED_ORIGINS` = Your Vercel URL (no trailing slash)
- `CSRF_TRUSTED_ORIGINS` = Your Vercel URL (no trailing slash)

✅ **User exists?**
- Try registering a new account first
- Then login with that account

---

## What to Share

If still not working, please share:
1. **Browser Console errors** (F12 → Console → screenshot or copy text)
2. **Network tab** - screenshot of the login request
3. **Your Vercel URL**
4. **Any error message** shown on the login page

---

## Try This First

1. **Register a new account:**
   - Click "Register" on login page
   - Username: `testuser`
   - Password: `test123456` (at least 6 chars)
   - Email: `test@example.com`
   - Click "Register"
   - Then try logging in with those credentials

2. **Check browser console** (F12) for any errors

3. **Check Network tab** (F12 → Network) when clicking Sign In

