# 🔍 Debug 403 Error on Upload

## Step-by-Step Debugging

### Step 1: Check Network Tab (F12)
1. Press **F12** → **Network** tab
2. Try uploading a file
3. Click on the `POST /api/uploads/` request
4. Check these:

#### Request Headers:
- ✅ `X-CSRFToken` - Should be present (the CSRF token value)
- ✅ `Cookie` - Should include:
  - `sessionid=...` (your session)
  - `csrftoken=...` (CSRF token)
- ✅ `Origin` - Should be your Vercel URL

#### Response:
- Status: `403 Forbidden`
- Response body: Check what it says (might have error details)

---

### Step 2: Check Browser Console (F12)
1. Press **F12** → **Console** tab
2. Look for:
   - "User is authenticated" - Should appear before upload
   - "CSRF token obtained" - Should appear before upload
   - Any error messages

---

### Step 3: Verify Render Environment Variables

Go to Render Dashboard → Your Service → Environment:

**CORS_ALLOWED_ORIGINS:**
- Should be: `https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app`
- NO trailing slash, NO path

**CSRF_TRUSTED_ORIGINS:**
- Should be: `https://chemical-equipment-parameter-visualizer-c1jvwy54a.vercel.app`
- NO trailing slash, NO path

**ALLOWED_HOSTS:**
- Should include: `chemical-equipment-parameter-visualizer-1.onrender.com`

---

### Step 4: Clear Cookies and Re-login

1. Press **F12** → **Application** → **Cookies**
2. Delete all cookies for your Vercel site
3. Refresh page (Ctrl+F5)
4. **Log in again** (this sets new session and CSRF cookies)
5. Try uploading

---

### Step 5: Check if You're Actually Logged In

1. Go to your frontend
2. Check if you see the dashboard (not login page)
3. Try accessing other pages - do they work?
4. If you're redirected to login, you're not authenticated

---

## Common Causes

### Cause 1: Not Logged In
- **Symptom:** Redirected to login page
- **Fix:** Log in first, then try uploading

### Cause 2: CSRF Token Missing
- **Symptom:** 403 error, no `X-CSRFToken` in request headers
- **Fix:** Make sure `CSRF_TRUSTED_ORIGINS` is set correctly in Render

### Cause 3: Session Expired
- **Symptom:** 403 error, `sessionid` cookie missing
- **Fix:** Clear cookies, log in again

### Cause 4: Wrong Origin
- **Symptom:** 403 error, CORS errors in console
- **Fix:** Make sure `CORS_ALLOWED_ORIGINS` matches your Vercel URL exactly

---

## Quick Test

1. **Open browser console (F12)**
2. **Type:** `document.cookie`
3. **Check if you see:**
   - `sessionid=...`
   - `csrftoken=...`
4. **If missing:** You're not logged in or cookies aren't being set

---

**Follow these steps and let me know what you find!** 🔍

