# 🔧 Fix Swagger UI Blank Page

## The Problem
Swagger UI shows a blank white page because static files aren't being collected/served.

## ✅ Solution: Update Build Command in Render

### Step 1: Go to Render Dashboard
1. Open https://dashboard.render.com
2. Click on your backend service: `chemical-equipment-parameter-visualizer-1`

### Step 2: Update Build Command
1. Go to **"Settings"** tab
2. Find **"Build Command"**
3. Update it to:
   ```
   pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```
4. Click **"Save Changes"**

### Step 3: Redeploy
1. Go to **"Manual Deploy"** tab
2. Click **"Clear build cache & deploy"**
3. Wait for deployment (3-5 minutes)

### Step 4: Test
After deployment, visit:
```
https://chemical-equipment-parameter-visualizer-1.onrender.com/swagger/
```

**Expected:** Swagger UI should now load with all API endpoints visible!

---

## 🔍 What Changed

1. **Added `collectstatic`** to build command - collects all static files (including Swagger UI assets)
2. **WhiteNoise middleware** - Serves static files in production
3. **Static files storage** - Configured for production

---

## ✅ Alternative: Use ReDoc

If Swagger still doesn't work, try ReDoc:
```
https://chemical-equipment-parameter-visualizer-1.onrender.com/redoc/
```

ReDoc is simpler and might work better.

---

**After updating the build command and redeploying, Swagger should work!** 🚀

