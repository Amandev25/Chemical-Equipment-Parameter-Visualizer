# 🔧 Fix: "Origin should not have path" Error

## The Problem
```
Origin 'https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app/login' 
in CORS_ALLOWED_ORIGINS should not have path
```

**The issue:** Your CORS URL has a path (`/login`) which is not allowed. CORS origins must be just the domain, no paths!

---

## ✅ Fix: Remove Path from CORS URL

### Step 1: Go to Render Dashboard
1. Open https://dashboard.render.com
2. Click your backend service: `chemical-equipment-parameter-visualizer-1`

### Step 2: Update CORS_ALLOWED_ORIGINS
1. Go to **"Environment"** tab
2. Find `CORS_ALLOWED_ORIGINS`
3. **Remove any path** - it should be just the domain

**❌ Wrong (has path):**
```
https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app/login
```

**✅ Correct (no path):**
```
https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app
```

4. Click **"Save"**

### Step 3: Update CSRF_TRUSTED_ORIGINS
1. Find `CSRF_TRUSTED_ORIGINS`
2. Make sure it also has **NO path**:

**✅ Correct:**
```
https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app
```

3. Click **"Save"**

### Step 4: Wait for Redeploy
1. Render will automatically redeploy (2-3 minutes)
2. Check **"Logs"** tab - should see deployment complete
3. Look for: `Your service is live 🎉`

### Step 5: Test Again
1. Go to your Vercel frontend
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

**Rules:**
- ✅ Include `https://`
- ✅ Just the domain (no path like `/login`, `/dashboard`, etc.)
- ✅ NO trailing slash `/`
- ✅ Exact match with your Vercel URL

---

**Update the CORS variables to remove the path and redeploy!** 🚀

