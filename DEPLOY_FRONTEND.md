# 🚀 Deploy Frontend to Vercel

Your Backend URL: `https://chemical-equipment-parameter-visualizer-1.onrender.com`

---

## Step 1: Deploy to Vercel (3 minutes)

### 1.1 Go to Vercel
1. Open https://vercel.com
2. Sign in with GitHub (if not already)

### 1.2 Import Project
1. Click **"Add New"** → **"Project"**
2. Find your repository: `Chemical-Equipment-Parameter-Visualizer`
3. Click **"Import"**

### 1.3 Configure Frontend
1. **Framework Preset**: Select **"Vite"** (or it will auto-detect)
2. **Root Directory**: Click **"Edit"** and set to `web-frontend`
3. **Build Command**: `npm run build` (should be auto-filled)
4. **Output Directory**: `dist` (should be auto-filled)
5. **Install Command**: `npm install` (should be auto-filled)

### 1.4 Set Environment Variable
1. Scroll to **"Environment Variables"** section
2. Click **"Add"**
3. Add this variable:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://chemical-equipment-parameter-visualizer-1.onrender.com/api`
4. Click **"Save"**

### 1.5 Deploy
1. Click **"Deploy"** button
2. Wait for build to complete (1-2 minutes)
3. Vercel will show you the deployment URL
4. **Copy your frontend URL** (e.g., `https://your-app.vercel.app`)

---

## Step 2: Update CORS in Backend

### 2.1 Go Back to Render
1. Open https://dashboard.render.com
2. Click on your backend service: `chemical-equipment-parameter-visualizer-1`

### 2.2 Update CORS Variables
1. Go to **"Environment"** tab
2. Find or add these variables:

**Variable 1:**
- Key: `CORS_ALLOWED_ORIGINS`
- Value: `https://your-frontend-url.vercel.app`
  (Use your actual Vercel URL from Step 1.5)

**Variable 2:**
- Key: `CSRF_TRUSTED_ORIGINS`
- Value: `https://your-frontend-url.vercel.app`
  (Use your actual Vercel URL from Step 1.5)

3. Click **"Save Changes"**
4. Render will automatically redeploy

---

## Step 3: Test Your Deployment

### 3.1 Test Frontend
1. Visit your Vercel URL
2. You should see the login page

### 3.2 Test Registration
1. Click "Don't have an account? Register"
2. Create a test account
3. Should redirect to dashboard

### 3.3 Test CSV Upload
1. Go to "Upload" page
2. Upload `sample_equipment_data.csv`
3. Wait for processing
4. Check if success message appears

### 3.4 Test Dashboard
1. Go to "Dashboard" page
2. Check if statistics are showing
3. Check if charts are displaying

### 3.5 Test Visualization
1. Go to "Data Visualization" page
2. Check if equipment data is showing
3. Test filters and search

---

## ✅ Deployment Complete!

If everything works, your full-stack app is live! 🎉

### Your Live URLs:
- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://chemical-equipment-parameter-visualizer-1.onrender.com`
- **API Docs**: `https://chemical-equipment-parameter-visualizer-1.onrender.com/swagger/`

---

## 🆘 Troubleshooting

### CORS Errors
- Make sure you updated `CORS_ALLOWED_ORIGINS` with exact Vercel URL
- Include `https://` prefix
- Redeploy backend after updating

### "Cannot connect to API"
- Check `VITE_API_URL` in Vercel environment variables
- Make sure it ends with `/api`
- Verify backend URL is correct
- Check backend is running

### Frontend Build Fails
- Check build logs in Vercel
- Verify all dependencies are in package.json
- Make sure `VITE_API_URL` is set

---

**Start with Step 1 - Deploy to Vercel!** 🚀

