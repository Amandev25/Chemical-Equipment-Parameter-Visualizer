# 🔧 Fix 403 Error on CSV Upload

## The Problem
```
Request failed with status code 403
```

This happens when uploading CSV files because:
1. **CSRF token not available** - The upload request needs a CSRF token
2. **Content-Type header conflict** - FormData needs browser to set Content-Type with boundary

---

## ✅ What I Fixed

### 1. **Fetch CSRF Token Before Upload**
Updated `UploadPage.jsx` to fetch CSRF token before uploading:
```javascript
// Ensure CSRF token is available before upload
await api.getCsrfToken();
```

### 2. **Handle FormData Content-Type**
Updated `api/client.js` interceptor to automatically remove `Content-Type` header for FormData:
```javascript
// For FormData, remove Content-Type to let browser set it with boundary
if (config.data instanceof FormData) {
  delete config.headers['Content-Type'];
}
```

### 3. **Simplified Upload Function**
Removed unnecessary headers from `uploadCSV` - the interceptor handles everything now.

---

## 🧪 Test After Deployment

1. **Make sure you're logged in:**
   - Go to your frontend
   - Log in with your credentials
   - You should see the dashboard

2. **Try uploading a CSV:**
   - Go to Upload page
   - Select a CSV file
   - Click "Upload File"
   - Should upload successfully (no 403 error)

3. **Check Network Tab (F12):**
   - Look for `POST /api/uploads/`
   - Status should be `201 Created` (not 403)
   - Check Request Headers:
     - `X-CSRFToken` should be present
     - `Cookie` should include `sessionid` and `csrftoken`

---

## 🔍 If Still Getting 403

### Check 1: Are you logged in?
- Try logging out and logging back in
- Check if `sessionid` cookie exists (F12 → Application → Cookies)

### Check 2: CSRF Token
- Check if `csrftoken` cookie exists
- Check if `X-CSRFToken` header is in the request

### Check 3: Backend Session Settings
- Make sure backend has `SESSION_COOKIE_SAMESITE = 'None'` and `SESSION_COOKIE_SECURE = True`
- (Already fixed in previous commit)

---

**The changes are pushed to GitHub. Vercel should auto-deploy the frontend. Try uploading again after deployment!** 🚀

