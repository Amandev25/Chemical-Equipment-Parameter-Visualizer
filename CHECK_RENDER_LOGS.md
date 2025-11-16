# 🔍 Check Render Logs for 500 Error

## The Problem
You're getting a **500 Internal Server Error** when trying to register. This means the backend is crashing.

## ✅ How to Check Render Logs

### Step 1: Go to Render Dashboard
1. Open https://dashboard.render.com
2. Click on your backend service: `chemical-equipment-parameter-visualizer-1`

### Step 2: View Logs
1. Click on **"Logs"** tab (at the top)
2. Scroll down to see the most recent logs
3. Look for **red error messages** or **traceback**
4. **Copy the error message** - this will tell us what's wrong

### Step 3: Try Registering Again
1. Go back to your frontend
2. Try to register again
3. Immediately go back to Render Logs
4. You should see a new error appear

---

## Common 500 Errors & Fixes

### Error: "relation does not exist" or "table does not exist"
**Problem:** Database migrations not run
**Fix:**
1. Go to Render → Your service → **Shell** tab (or use Manual Deploy)
2. Run: `python manage.py migrate`
3. Or update Start Command to include: `python manage.py migrate`

### Error: "IntegrityError" or "duplicate key"
**Problem:** User already exists
**Fix:** Try a different username

### Error: "ImportError" or "ModuleNotFoundError"
**Problem:** Missing dependency
**Fix:** Check `requirements.txt` is complete

### Error: "OperationalError" or "connection refused"
**Problem:** Database connection issue
**Fix:** Check `DATABASE_URL` in Render environment variables

---

## What to Share

After checking logs, share:
1. **The exact error message** from Render logs
2. **The traceback** (if shown)
3. **Any red error lines** you see

This will help me fix the exact issue!

---

## Quick Fix to Try First

1. **Check if migrations are running:**
   - Go to Render → Your service → **Settings** → **Build & Deploy**
   - Check **Start Command** includes: `python manage.py migrate`
   - Should be: `cd backend && python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`

2. **Redeploy:**
   - Go to **Manual Deploy** tab
   - Click **"Clear build cache & deploy"**
   - Wait for deployment

3. **Try registering again**

