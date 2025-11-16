# 🔧 Fix 403 Error on CSV Upload - Final Solution

## The Problem
```
POST /api/uploads/ 403 (Forbidden)
```

This happens because:
1. **CSRF token not being validated** - Backend isn't accepting the CSRF token
2. **Frontend domain not in CSRF_TRUSTED_ORIGINS** - Your Vercel URL needs to be in Render's environment variables

---

## ✅ Step 1: Check Your Vercel Frontend URL

1. Go to your Vercel dashboard
2. Find your deployed frontend URL
3. It should look like: `https://chemical-equipment-parameter-visual-mu.vercel.app`
4. **Copy the exact URL** (no trailing slash, no path)

---

## ✅ Step 2: Update Render Environment Variables

1. Go to **Render Dashboard**: https://dashboard.render.com
2. Click your backend service: `chemical-equipment-parameter-visualizer-1`
3. Go to **"Environment"** tab
4. Find these variables and update them:

### **CORS_ALLOWED_ORIGINS**
- **Current value:** Check what it is
- **Should be:** Your Vercel frontend URL (exact match)
- **Example:** `https://chemical-equipment-parameter-visual-mu.vercel.app`
- **Important:** NO trailing slash, NO path (just the domain)

### **CSRF_TRUSTED_ORIGINS**
- **Current value:** Check what it is
- **Should be:** Same as CORS_ALLOWED_ORIGINS
- **Example:** `https://chemical-equipment-parameter-visual-mu.vercel.app`
- **Important:** NO trailing slash, NO path

5. Click **"Save Changes"**
6. Render will automatically redeploy (wait 2-3 minutes)

---

## ✅ Step 3: Verify After Redeploy

1. **Clear browser cookies:**
   - Press F12 → Application → Cookies
   - Delete all cookies for your Vercel frontend

2. **Log in again:**
   - Go to your frontend
   - Log in with your credentials
   - This will set new session and CSRF cookies

3. **Try uploading:**
   - Go to Upload page
   - Select CSV file
   - Click "Upload File"
   - Should work now!

---

## 🔍 Debug: Check Network Tab

If still getting 403, check:

1. **Press F12 → Network tab**
2. **Try uploading a file**
3. **Click on the `POST /api/uploads/` request**
4. **Check Request Headers:**
   - `X-CSRFToken` should be present
   - `Cookie` should include `sessionid` and `csrftoken`
   - `Origin` should match your Vercel URL

5. **Check Response:**
   - Status: Should be 201 (not 403)
   - If 403, check the response body for error details

---

## ✅ Quick Checklist

- [ ] Vercel frontend URL is in `CORS_ALLOWED_ORIGINS` (no path, no trailing slash)
- [ ] Vercel frontend URL is in `CSRF_TRUSTED_ORIGINS` (no path, no trailing slash)
- [ ] Render has redeployed after changes
- [ ] Cleared browser cookies
- [ ] Logged in again
- [ ] Tried uploading

---

**Update the environment variables in Render and redeploy!** 🚀

