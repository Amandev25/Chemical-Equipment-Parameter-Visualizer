# 🔧 Fix Render Deployment Error: "Application exited early"

## The Problem
Render shows: "Application exited early while running your code"

This usually means the **Start Command** is failing.

---

## ✅ Solution: Fix Start Command

### Step 1: Check Your Render Configuration

1. Go to https://dashboard.render.com
2. Click on your `chemical-equipment-parameter-visualizer-1` service
3. Go to **"Settings"** tab
4. Scroll to **"Build & Deploy"** section

### Step 2: Update Start Command

**If your Root Directory is set to `backend`:**
```
python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

**If your Root Directory is NOT set (root of repo):**
```
cd backend && python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

### Step 3: Update Build Command

**If your Root Directory is set to `backend`:**
```
pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py collectstatic --noinput
```

**If your Root Directory is NOT set (root of repo):**
```
cd backend && pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py collectstatic --noinput
```

---

## 🔍 Check These Common Issues

### 1. Root Directory Setting
- Go to **Settings** → **Build & Deploy**
- Check **"Root Directory"** field
- Should be: `backend` (if you set it) OR empty (if using root)

### 2. Python Version
- Go to **Settings** → **Build & Deploy**
- **Python Version** should be: `3.11` (NOT 3.13!)
- If it's wrong, change it and redeploy

### 3. Environment Variables
Go to **Environment** tab and verify these exist:

✅ **Required Variables:**
- `DEBUG` = `True`
- `SECRET_KEY` = (any long random string)
- `ALLOWED_HOSTS` = `chemical-equipment-parameter-visualizer-1.onrender.com`
- `DATABASE_URL` = (your PostgreSQL connection string)

✅ **Optional (for CORS):**
- `CORS_ALLOWED_ORIGINS` = `http://localhost:3000` (or your frontend URL)
- `CSRF_TRUSTED_ORIGINS` = `http://localhost:3000` (or your frontend URL)

### 4. Database Connection
- Make sure PostgreSQL database exists
- Check `DATABASE_URL` is correct
- Format: `postgresql://user:password@host:port/dbname`

---

## 🚀 Quick Fix Steps

1. **Go to Render Dashboard** → Your service
2. **Settings** tab
3. **Update Start Command** (use correct one based on Root Directory)
4. **Update Build Command** (use correct one based on Root Directory)
5. **Verify Python Version** = `3.11`
6. **Check Environment Variables** (especially `DATABASE_URL`)
7. **Go to "Manual Deploy"** tab
8. **Click "Clear build cache & deploy"**
9. **Wait for deployment** (3-5 minutes)

---

## 📋 Recommended Configuration

**Root Directory:** `backend`

**Build Command:**
```bash
pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py collectstatic --noinput
```

**Start Command:**
```bash
python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

**Python Version:** `3.11`

---

## 🆘 Still Not Working?

### Check Logs
1. Go to **"Logs"** tab in Render
2. Look for error messages
3. Common errors:
   - `ModuleNotFoundError` → Dependencies not installed
   - `OperationalError` → Database connection failed
   - `Port already in use` → Port binding issue
   - `No such file or directory` → Wrong path in commands

### Try This Debug Start Command
Temporarily use this to see what's failing:
```bash
python manage.py migrate && echo "Migration done" && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --log-level debug
```

---

**After fixing, redeploy and check if it works!** 🎯

