# 🔍 Debug Login Issue

## Common Issues & Solutions

### 1. Check Browser Console
1. Open your frontend URL
2. Press **F12** (or right-click → Inspect)
3. Go to **Console** tab
4. Try to login
5. Look for **red error messages**
6. **Copy any errors** you see

### 2. Check Network Tab
1. Press **F12** → **Network** tab
2. Try to login
3. Look for requests to `/api/auth/login/`
4. Click on the request
5. Check:
   - **Status Code** (should be 200, not 403, 401, or 500)
   - **Response** tab - what error message?
   - **Request Headers** - is `X-CSRFToken` present?

### 3. Common Errors

#### Error: "Network Error" or "Failed to fetch"
**Problem:** Frontend can't reach backend
**Solution:**
- Check `VITE_API_URL` in Vercel environment variables
- Should be: `https://chemical-equipment-parameter-visualizer-1.onrender.com/api`
- Make sure backend is running (check Render dashboard)

#### Error: 403 Forbidden
**Problem:** CSRF token issue
**Solution:**
- Check CORS settings in Render
- Make sure `CSRF_TRUSTED_ORIGINS` has your Vercel URL (no trailing slash)
- Check browser console for CSRF errors

#### Error: 401 Unauthorized
**Problem:** Wrong username/password or user doesn't exist
**Solution:**
- Try registering a new account first
- Make sure password is at least 6 characters
- Check if user exists in backend

#### Error: CORS error
**Problem:** Backend not allowing frontend origin
**Solution:**
- Check `CORS_ALLOWED_ORIGINS` in Render
- Should be: `https://your-vercel-url.vercel.app` (no trailing slash)
- Redeploy backend after updating

---

## Quick Test Steps

1. **Test Backend API directly:**
   ```
   https://chemical-equipment-parameter-visualizer-1.onrender.com/api/health/
   ```
   Should return: `{"status": "healthy", ...}`

2. **Check Vercel Environment Variable:**
   - Go to Vercel Dashboard → Your project → Settings → Environment Variables
   - Verify `VITE_API_URL` is set correctly

3. **Check Render CORS:**
   - Go to Render Dashboard → Your service → Environment
   - Verify `CORS_ALLOWED_ORIGINS` = your Vercel URL (no `/` at end)
   - Verify `CSRF_TRUSTED_ORIGINS` = your Vercel URL (no `/` at end)

4. **Try Register First:**
   - Click "Register" on login page
   - Create a new account
   - Then try logging in with that account

---

## What to Share

If still not working, share:
1. **Browser Console errors** (F12 → Console)
2. **Network tab** - screenshot of the `/api/auth/login/` request
3. **Your Vercel URL**
4. **Any error message** shown on the login page

