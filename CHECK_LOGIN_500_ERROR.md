# 🔍 Debug 500 Error on Login

## The Problem
You're getting a **500 Internal Server Error** when trying to log in. This means the backend is crashing.

---

## ✅ Step 1: Check Network Tab Response

1. Open your frontend
2. Press **F12** → **Network** tab
3. Try to log in again
4. Find the request: `POST /api/auth/login/` (status 500)
5. Click on it → **Response** tab
6. **Copy the response** - it should show:
   ```json
   {
     "error": "Login failed",
     "detail": "actual error message here"
   }
   ```

---

## ✅ Step 2: Check Render Logs

1. Go to https://dashboard.render.com
2. Click your backend service
3. Go to **"Logs"** tab
4. Scroll to the **bottom** (most recent logs)
5. Try logging in again from frontend
6. **Immediately** check Render logs
7. Look for:
   - `Login error: ...`
   - Python traceback
   - Any ERROR or Exception lines

---

## Common 500 Errors & Fixes

### Error: "relation does not exist" or "table does not exist"
**Problem:** Database migrations not run
**Fix:** Check if migrations ran in logs. Should see "No migrations to apply" or "Operations to perform"

### Error: "OperationalError" or "connection refused"
**Problem:** Database connection issue
**Fix:** Check `DATABASE_URL` in Render environment variables

### Error: "IntegrityError"
**Problem:** Database constraint violation
**Fix:** Check if user already exists or database issue

---

## What to Share

After checking, share:
1. **The Response body** from Network tab (the `detail` field)
2. **The error from Render logs** (especially `Login error:` or traceback)

This will show the exact issue!

---

**Check the Network tab Response first - it should now show the actual error!** 🔍

