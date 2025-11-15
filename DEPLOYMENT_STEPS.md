# 🚀 Live Deployment Steps

Follow these steps to deploy your app right now!

---

## Step 1: Deploy Backend to Railway

### 1.1 Go to Railway
1. Open https://railway.app
2. Sign in with GitHub (if not already)

### 1.2 Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Select your repository from the list
4. Click **"Deploy Now"**

### 1.3 Configure Backend Service
1. Railway will create a service automatically
2. Click on the service to open settings
3. Go to **"Settings"** tab
4. Set these values:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`

### 1.4 Add PostgreSQL Database
1. Click **"New"** button (top right)
2. Select **"Database"**
3. Choose **"Add PostgreSQL"**
4. Railway will automatically create and connect it
5. The `DATABASE_URL` will be set automatically

### 1.5 Set Environment Variables
1. Go to **"Variables"** tab
2. Click **"New Variable"** and add these one by one:

```
DEBUG=True
```

```
SECRET_KEY=your-secret-key-here-min-50-characters-long
```

(Generate secret key: https://djecrety.ir/ or run: `python -c "import secrets; print(secrets.token_urlsafe(50))"`)

```
ALLOWED_HOSTS=*.railway.app
```

3. Save all variables

### 1.6 Get Your Backend URL
1. Go to **"Settings"** tab
2. Scroll to **"Domains"** section
3. Click **"Generate Domain"** if not already generated
4. Copy your backend URL (e.g., `https://your-app-production.up.railway.app`)
5. **Save this URL** - you'll need it for frontend!

### 1.7 Wait for Deployment
- Railway will automatically build and deploy
- Watch the logs to see progress
- Wait until you see "Listening on 0.0.0.0:$PORT"
- Status should show "Active" ✅

---

## Step 2: Deploy Frontend to Vercel

### 2.1 Go to Vercel
1. Open https://vercel.com
2. Sign in with GitHub (if not already)

### 2.2 Import Project
1. Click **"Add New"** → **"Project"**
2. Find your repository in the list
3. Click **"Import"**

### 2.3 Configure Frontend
1. **Framework Preset**: Select **"Vite"** (or leave auto-detected)
2. **Root Directory**: Click "Edit" and set to `web-frontend`
3. **Build Command**: `npm run build` (should be auto-filled)
4. **Output Directory**: `dist` (should be auto-filled)
5. **Install Command**: `npm install` (should be auto-filled)

### 2.4 Set Environment Variable
1. Scroll to **"Environment Variables"** section
2. Click **"Add"**
3. Add this variable:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-backend-url.railway.app/api`
     (Use the Railway URL you copied in Step 1.6)
4. Click **"Save"**

### 2.5 Deploy
1. Click **"Deploy"** button
2. Wait for build to complete (1-2 minutes)
3. Vercel will show you the deployment URL
4. Copy your frontend URL (e.g., `https://your-app.vercel.app`)
5. **Save this URL** - you'll need it next!

---

## Step 3: Update CORS Settings

### 3.1 Go Back to Railway
1. Open Railway dashboard
2. Click on your backend service

### 3.2 Add CORS Variables
1. Go to **"Variables"** tab
2. Add these two new variables:

```
CORS_ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
```

(Replace with your actual Vercel URL from Step 2.5)

```
CSRF_TRUSTED_ORIGINS=https://your-frontend-url.vercel.app
```

(Replace with your actual Vercel URL from Step 2.5)

3. Save both variables
4. Railway will automatically redeploy

### 3.3 Wait for Redeploy
- Watch the deployment logs
- Wait until status shows "Active" ✅

---

## Step 4: Test Your Deployment

### 4.1 Test Frontend
1. Open your Vercel URL in browser
2. You should see the login page

### 4.2 Test Registration
1. Click "Don't have an account? Register"
2. Create a test account
3. You should be logged in

### 4.3 Test CSV Upload
1. Go to "Upload" page
2. Upload `sample_equipment_data.csv`
3. Wait for processing
4. Check if it shows success message

### 4.4 Test Dashboard
1. Go to "Dashboard" page
2. Check if statistics are showing
3. Check if charts are displaying

### 4.5 Test Visualization
1. Go to "Data Visualization" page
2. Check if equipment data is showing
3. Test filters and search

---

## ✅ Deployment Complete!

If everything works, your app is live! 🎉

### Your Live URLs:
- **Frontend**: https://your-app.vercel.app
- **Backend API**: https://your-app.railway.app
- **API Docs**: https://your-app.railway.app/swagger/
- **Admin Panel**: https://your-app.railway.app/admin/

---

## 🆘 Troubleshooting

### Backend Issues

**"Application Error" on Railway:**
- Check deployment logs in Railway
- Look for error messages
- Common fixes:
  - Make sure `gunicorn` is in requirements.txt ✅
  - Check all environment variables are set
  - Verify database is connected

**"Database connection error":**
- Make sure PostgreSQL is added
- Check `DATABASE_URL` is set (auto-set by Railway)
- Try redeploying

### Frontend Issues

**"CORS Error" in browser console:**
- Go back to Railway
- Verify `CORS_ALLOWED_ORIGINS` has your Vercel URL
- Make sure URL starts with `https://`
- Redeploy backend

**"Cannot connect to API":**
- Check `VITE_API_URL` in Vercel environment variables
- Make sure it ends with `/api`
- Verify backend URL is correct
- Check backend is running (visit backend URL in browser)

**"404 Not Found" on API calls:**
- Verify backend URL is correct
- Check API routes: https://your-backend.railway.app/api/health/
- Should return: `{"status":"healthy",...}`

### Quick Fixes

1. **Check logs** in Railway and Vercel dashboards
2. **Verify environment variables** are set correctly
3. **Test backend directly**: Visit backend URL + `/api/health/`
4. **Clear browser cache** and try again
5. **Check network tab** in browser DevTools for API errors

---

## 📝 Next Steps

1. **Create superuser** for admin access:
   - Use Railway CLI or connect via SSH
   - Run: `python manage.py createsuperuser`

2. **Custom domain** (optional):
   - Railway: Add custom domain in Settings
   - Vercel: Add custom domain in Project Settings

3. **Monitor usage**:
   - Railway: Check usage in dashboard
   - Vercel: Check analytics in dashboard

---

**Need help?** Check the logs in Railway and Vercel dashboards!

