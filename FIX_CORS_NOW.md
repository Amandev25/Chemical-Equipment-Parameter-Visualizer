# 🚨 Fix CORS Error - Update Render Environment Variables

## The Problem
```
Access to XMLHttpRequest at 'https://chemical-equipment-parameter-visualizer-1.onrender.com/api/auth/csrf/' 
from origin 'https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app' 
has been blocked by CORS policy
```

**Your Vercel URL:** `https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app`

---

## ✅ Fix: Update CORS in Render (2 minutes)

### Step 1: Go to Render Dashboard
1. Open https://dashboard.render.com
2. Click your backend service: `chemical-equipment-parameter-visualizer-1`

### Step 2: Update Environment Variables
1. Go to **"Environment"** tab
2. Find or add these variables:

**Variable 1: CORS_ALLOWED_ORIGINS**
- **Key**: `CORS_ALLOWED_ORIGINS`
- **Value**: `https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app`
  - ⚠️ **NO trailing slash!** (Don't add `/` at the end)
- Click **"Save"**

**Variable 2: CSRF_TRUSTED_ORIGINS**
- **Key**: `CSRF_TRUSTED_ORIGINS`
- **Value**: `https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app`
  - ⚠️ **NO trailing slash!** (Don't add `/` at the end)
- Click **"Save"**

### Step 3: Wait for Redeploy
1. Render will automatically redeploy (2-3 minutes)
2. Check **"Logs"** tab to see when it's done
3. Look for: `Your service is live 🎉`

### Step 4: Test Again
1. Go back to your Vercel frontend
2. Try registering again
3. Should work now!

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

**⚠️ Important:**
- Include `https://`
- NO trailing slash `/`
- Exact match with your Vercel URL

---

## 🔍 How to Check Your Vercel URL

1. Go to https://vercel.com
2. Click your project
3. Copy the URL from the top (e.g., `https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app`)

---

**Update these variables in Render and wait for redeploy!** 🚀

