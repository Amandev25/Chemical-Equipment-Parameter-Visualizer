# 🚀 Deploy Web UI - Step by Step Guide

**Backend URL:** `https://chemical-equipment-parameter-visualizer-1.onrender.com`

---

## 📋 Step-by-Step Instructions

### **Step 1: Go to Vercel** (30 seconds)
1. Open https://vercel.com in your browser
2. Click **"Sign Up"** or **"Log In"**
3. Sign in with **GitHub** (recommended - use the same account as your repo)

---

### **Step 2: Import Your Project** (1 minute)
1. Click **"Add New"** button (top right)
2. Click **"Project"**
3. Find your repository: `Chemical-Equipment-Parameter-Visualizer`
4. Click **"Import"** button

---

### **Step 3: Configure Project Settings** (2 minutes)

#### 3.1 Framework Settings
- **Framework Preset**: Should auto-detect as **"Vite"** ✅
- If not, select **"Vite"** from dropdown

#### 3.2 Root Directory
1. Click **"Edit"** next to "Root Directory"
2. Change from `./` to: **`web-frontend`**
3. Click **"Continue"**

#### 3.3 Build Settings (Should auto-fill, verify these)
- **Build Command**: `npm run build` ✅
- **Output Directory**: `dist` ✅
- **Install Command**: `npm install` ✅

---

### **Step 4: Add Environment Variable** (1 minute)
1. Scroll down to **"Environment Variables"** section
2. Click **"Add"** button
3. Enter:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://chemical-equipment-parameter-visualizer-1.onrender.com/api`
4. Click **"Save"**

---

### **Step 5: Deploy** (2 minutes)
1. Scroll to bottom
2. Click **"Deploy"** button
3. Wait for build to complete (1-2 minutes)
4. **Copy your frontend URL** when it appears
   - Example: `https://chemical-equipment-parameter-visualizer-1.vercel.app`

---

### **Step 6: Update Backend CORS** (2 minutes)

#### 6.1 Go to Render Dashboard
1. Open https://dashboard.render.com
2. Click on your backend service: `chemical-equipment-parameter-visualizer-1`

#### 6.2 Add CORS Environment Variables
1. Go to **"Environment"** tab
2. Click **"Add Environment Variable"**

**Variable 1:**
- **Key**: `CORS_ALLOWED_ORIGINS`
- **Value**: `https://your-vercel-url.vercel.app`
  - Replace `your-vercel-url` with your actual Vercel URL from Step 5
  - Example: `https://chemical-equipment-parameter-visualizer-1.vercel.app`
  - ⚠️ **IMPORTANT: NO trailing slash!** (Don't add `/` at the end)
- Click **"Save"**

**Variable 2:**
- **Key**: `CSRF_TRUSTED_ORIGINS`
- **Value**: `https://your-vercel-url.vercel.app`
  - Same URL as above
  - ⚠️ **IMPORTANT: NO trailing slash!** (Don't add `/` at the end)
- Click **"Save"**

3. Render will automatically redeploy (wait 2-3 minutes)

---

### **Step 7: Test Your Deployment** (3 minutes)

#### 7.1 Test Frontend
1. Visit your Vercel URL
2. You should see the **Login Page**

#### 7.2 Test Registration
1. Click **"Don't have an account? Register"**
2. Fill in:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `testpass123`
   - Confirm Password: `testpass123`
3. Click **"Register"**
4. Should redirect to **Dashboard**

#### 7.3 Test CSV Upload
1. Click **"Upload"** in navigation
2. Drag and drop or click to upload `sample_equipment_data.csv`
3. Wait for "Upload successful" message

#### 7.4 Test Dashboard
1. Click **"Dashboard"** in navigation
2. Check if statistics show (Total Equipment, etc.)
3. Check if charts are displaying

#### 7.5 Test Visualization
1. Click **"Data Visualization"** in navigation
2. Check if equipment data table is showing
3. Test search and filters

---

## ✅ Deployment Complete!

Your full-stack application is now live! 🎉

### Your Live URLs:
- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://chemical-equipment-parameter-visualizer-1.onrender.com`
- **API Docs**: `https://chemical-equipment-parameter-visualizer-1.onrender.com/swagger/`

---

## 🆘 Troubleshooting

### ❌ Build Fails in Vercel
- Check build logs in Vercel dashboard
- Verify `VITE_API_URL` environment variable is set
- Make sure Root Directory is `web-frontend`

### ❌ CORS Errors
- Verify `CORS_ALLOWED_ORIGINS` in Render matches your Vercel URL exactly
- Include `https://` prefix
- Wait for Render to finish redeploying after adding CORS variables

### ❌ "Cannot connect to API"
- Check `VITE_API_URL` in Vercel environment variables
- Make sure it ends with `/api`
- Verify backend is running (check Render dashboard)

### ❌ Login/Register Not Working
- Check browser console for errors (F12)
- Verify backend CORS settings
- Make sure CSRF token is being sent (check Network tab)

---

## 📝 Quick Reference

**Vercel Configuration:**
- Root Directory: `web-frontend`
- Build Command: `npm run build`
- Output Directory: `dist`
- Environment Variable: `VITE_API_URL=https://chemical-equipment-parameter-visualizer-1.onrender.com/api`

**Render CORS Variables:**
- `CORS_ALLOWED_ORIGINS` = Your Vercel URL
- `CSRF_TRUSTED_ORIGINS` = Your Vercel URL

---

**Ready? Start with Step 1!** 🚀

