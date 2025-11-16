# 🚨 URGENT: Fix CORS Error

## The Error
```
Access to XMLHttpRequest at 'https://chemical-equipment-parameter-visualizer-1.onrender.com/api/auth/csrf/' 
from origin 'https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
```

**Your frontend URL:** `https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app`

---

## ✅ Fix: Add Frontend URL to Render

### Step 1: Go to Render Dashboard
1. Open: https://dashboard.render.com
2. Click your backend service: **`chemical-equipment-parameter-visualizer-1`**

### Step 2: Go to Environment Tab
1. Click **"Environment"** tab (left sidebar)
2. You'll see all environment variables

### Step 3: Update CORS_ALLOWED_ORIGINS
1. Find **`CORS_ALLOWED_ORIGINS`** variable
2. **Current value:** Check what it says
3. **Set it to:** `https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app`
   - **IMPORTANT:** 
     - ✅ Include `https://`
     - ✅ NO trailing slash `/`
     - ✅ NO path (just the domain)
     - ✅ Exact match with your Vercel URL

4. Click **"Save Changes"**

### Step 4: Update CSRF_TRUSTED_ORIGINS
1. Find **`CSRF_TRUSTED_ORIGINS`** variable
2. **Set it to:** `https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app`
   - Same format as above

3. Click **"Save Changes"**

### Step 5: Wait for Redeploy
1. Render will automatically redeploy (2-3 minutes)
2. Go to **"Logs"** tab to watch deployment
3. Wait for: `Your service is live 🎉`

---

## ✅ Step 6: Test After Redeploy

1. **Clear browser cache:**
   - Press `Ctrl+Shift+Delete` (Windows) or `Cmd+Shift+Delete` (Mac)
   - Clear cookies and cache for your Vercel site

2. **Or manually clear cookies:**
   - Press F12 → **Application** tab → **Cookies**
   - Delete all cookies for `chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app`

3. **Refresh the page:**
   - Hard refresh: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)

4. **Try logging in:**
   - Should work now without CORS errors
   - Then try uploading a CSV file

---

## ✅ Correct Format

**CORS_ALLOWED_ORIGINS:**
```
https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app
```

**CSRF_TRUSTED_ORIGINS:**
```
https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app
```

**Rules:**
- ✅ Start with `https://`
- ✅ Just the domain (no `/login`, `/dashboard`, etc.)
- ✅ NO trailing slash
- ✅ Exact match with Vercel URL

---

## 🔍 Verify It's Fixed

After redeploy, check browser console (F12):
- ❌ Should NOT see: "blocked by CORS policy"
- ✅ Should see: Successful API requests

---

**Go to Render NOW and add your Vercel URL to CORS_ALLOWED_ORIGINS!** 🚀

