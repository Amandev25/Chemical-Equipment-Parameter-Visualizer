# 🔧 Fix ALLOWED_HOSTS Error

## The Error
```
Invalid HTTP_HOST header: 'chemical-equipment-parameter-visualizer-1.onrender.com'. 
You may need to add 'chemical-equipment-parameter-visualizer-1.onrender.com' to ALLOWED_HOSTS.
```

## ✅ Quick Fix (2 minutes)

### Step 1: Go to Render Dashboard
1. Open https://dashboard.render.com
2. Click on your backend service: `chemical-equipment-parameter-visualizer-1`

### Step 2: Update Environment Variable
1. Go to **"Environment"** tab
2. Find the `ALLOWED_HOSTS` variable
3. Click on it to edit
4. Change the value to:
   ```
   chemical-equipment-parameter-visualizer-1.onrender.com
   ```
5. Click **"Save Changes"**

### Step 3: Redeploy
1. Render will automatically redeploy
2. Wait 2-3 minutes for deployment
3. Test again: https://chemical-equipment-parameter-visualizer-1.onrender.com/api/health/

---

## ✅ Alternative: Add via Render Dashboard

If you can't find the variable:

1. Go to **"Environment"** tab
2. Click **"Add Environment Variable"**
3. Key: `ALLOWED_HOSTS`
4. Value: `chemical-equipment-parameter-visualizer-1.onrender.com`
5. Click **"Save Changes"**

---

## 🎯 After Fixing

Once you update `ALLOWED_HOSTS` and redeploy:
- Health check should work: `/api/health/`
- Swagger should load: `/swagger/`
- API endpoints should respond

---

**That's it! Just update the ALLOWED_HOSTS variable in Render!** 🚀

