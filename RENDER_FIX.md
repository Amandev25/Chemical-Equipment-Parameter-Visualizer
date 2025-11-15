# 🔧 Fix Render Build Error - Python Version Issue

## The Problem
Render is using Python 3.13 which has compatibility issues. We need to force Python 3.11.

## ✅ Solution: Update Your Render Service

### Option 1: Update Existing Service (Easiest)

1. **Go to your Render Dashboard**
2. **Click on your `chemviz-backend` service**
3. **Go to "Settings" tab**
4. **Scroll down to find "Python Version" or "Environment"**
5. **Change it to `3.11`** (if it shows 3.13 or any other version)
6. **Save changes**
7. **Go to "Manual Deploy" tab**
8. **Click "Clear build cache & deploy"**
9. **Wait for deployment**

### Option 2: Delete and Recreate (If Option 1 doesn't work)

1. **Delete your current service** (don't delete the database!)
2. **Create new Web Service**
3. **When configuring, BEFORE clicking "Create":**
   - Look for **"Python Version"** dropdown
   - **Select `3.11`** explicitly
   - Don't leave it on default!
4. **Set Build Command**: `pip install --upgrade pip setuptools wheel && pip install -r requirements.txt`
5. **Set Start Command**: `python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`
6. **Add all environment variables** (same as before)
7. **Create service**

## 📝 Updated Build Command

Make sure your Build Command is:
```bash
pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
```

## ✅ Verify Python Version

After deployment, check the logs. You should see:
- Python 3.11.x (NOT 3.13!)
- Successful package installation
- No `KeyError: '__version__'` errors

## 🆘 Still Getting Errors?

If you still see Python 3.13 in the error:
1. **Check Render Settings** - Make sure Python 3.11 is selected
2. **Clear Build Cache** - In Manual Deploy, click "Clear build cache"
3. **Check runtime.txt** - Should contain `python-3.11.9`
4. **Try deleting and recreating** the service with Python 3.11 explicitly selected

---

**The key is: Render MUST use Python 3.11, not 3.13!**

