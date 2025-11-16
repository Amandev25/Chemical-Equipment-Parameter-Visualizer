# 🔧 Fix CORS Error: "Origin should not have path"

## The Problem
```
SystemCheckError: Origin 'https://chemical-equipment-parameter-visual-mu.vercel.app/' in CORS_ALLOWED_ORIGINS should not have path
```

**The issue:** Your CORS URL has a **trailing slash** (`/`) which is not allowed.

---

## ✅ Quick Fix (1 minute)

### Step 1: Go to Render Dashboard
1. Open https://dashboard.render.com
2. Click on your backend service: `chemical-equipment-parameter-visualizer-1`

### Step 2: Fix Environment Variables
1. Go to **"Environment"** tab
2. Find `CORS_ALLOWED_ORIGINS`
3. **Remove the trailing slash** from the value

**❌ Wrong:**
```
https://chemical-equipment-parameter-visual-mu.vercel.app/
```

**✅ Correct:**
```
https://chemical-equipment-parameter-visual-mu.vercel.app
```

4. Also check `CSRF_TRUSTED_ORIGINS` - remove trailing slash if present

**❌ Wrong:**
```
https://chemical-equipment-parameter-visual-mu.vercel.app/
```

**✅ Correct:**
```
https://chemical-equipment-parameter-visual-mu.vercel.app
```

5. Click **"Save Changes"**
6. Render will automatically redeploy

---

## 📋 Correct Format

CORS URLs should be:
- ✅ `https://your-app.vercel.app` (no trailing slash)
- ✅ `http://localhost:3000` (no trailing slash)
- ❌ `https://your-app.vercel.app/` (has trailing slash - WRONG!)

---

## 🔍 Verify After Fix

1. Wait for deployment to complete (2-3 minutes)
2. Check **Logs** tab - should see "Starting gunicorn" without errors
3. Test your API: `https://chemical-equipment-parameter-visualizer-1.onrender.com/api/health/`

---

**That's it! Just remove the trailing slash and redeploy.** 🚀

