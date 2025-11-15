# 🚀 Deploy to Render (Free Tier Available)

Since Railway trial ended, let's use Render which has a free tier!

---

## Step 1: Deploy Backend to Render

### 1.1 Sign Up
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended)

### 1.2 Create PostgreSQL Database
1. Click **"New +"** → **"PostgreSQL"**
2. Name: `chemviz-db`
3. Database: `chemviz_db`
4. User: `chemviz_user`
5. Region: Choose closest to you
6. Plan: **Free** (or Starter if you want)
7. Click **"Create Database"**
8. **Save these credentials** - you'll need them:
   - Internal Database URL (for Render services)
   - External Connection String (if needed)

### 1.3 Create Web Service (Backend)
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `Chemical-Equipment-Parameter-Visualizer`
3. Configure:
   - **Name**: `chemviz-backend`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Environment**: **Python 3**
   - **Python Version**: **MUST BE 3.11** - Look for a dropdown or field that says "Python Version" and select `3.11` (NOT 3.13!)
   - **Build Command**: `pip install --upgrade pip setuptools wheel && pip install -r requirements.txt`
   - **Start Command**: `python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`
   - **Plan**: **Free** (or Starter)

### 1.4 Get Database Connection String First
**IMPORTANT: Do this BEFORE setting environment variables!**

1. Go back to your PostgreSQL database (created in Step 1.2)
2. Click on the database name to open it
3. Look for **"Internal Database URL"** or **"Connection String"** 
4. It will look like: `postgresql://chemviz_user:password@dpg-xxxxx-a.oregon-postgres.render.com/chemviz_db`
5. **Copy this entire URL** - you'll paste it in the next step
6. Keep this tab open or save the URL somewhere

### 1.5 Set Environment Variables
Now go back to your Web Service configuration and scroll to **"Environment Variables"** section.

Add these variables one by one (click "Add Environment Variable" for each):

**Variable 1:**
- Key: `DEBUG`
- Value: `True`

**Variable 2:**
- Key: `SECRET_KEY`
- Value: `oOAo472iuU2-5FhqQVm8a_UfuJPXN4VtIGh1IQWvtbXd1QiniotCcwaKxjP6Ku5aFYw`

**Variable 3:**
- Key: `ALLOWED_HOSTS`
- Value: `chemical-equipment-parameter-visualizer-1.onrender.com`
  - **IMPORTANT:** Use your actual Render service URL (the one you see in Render dashboard)

**Variable 4:**
- Key: `DATABASE_URL`
- Value: `postgresql://user:password@host:port/dbname`
  - **Paste the Internal Database URL you copied in Step 1.4 here!**

**Variable 5:**
- Key: `CORS_ALLOWED_ORIGINS`
- Value: `https://your-frontend-url.onrender.com`
  - (We'll update this after frontend deployment - use placeholder for now)

**Variable 6:**
- Key: `CSRF_TRUSTED_ORIGINS`
- Value: `https://your-frontend-url.onrender.com`
  - (We'll update this after frontend deployment - use placeholder for now)

### 1.6 Deploy
1. Click **"Create Web Service"**
2. Render will start building (takes 3-5 minutes)
3. Wait for deployment to complete
4. Copy your backend URL: `https://chemviz-backend.onrender.com`

---

## Step 2: Deploy Frontend to Render

### 2.1 Create Static Site
1. Click **"New +"** → **"Static Site"**
2. Connect your GitHub repository: `Chemical-Equipment-Parameter-Visualizer`
3. Configure:
   - **Name**: `chemviz-frontend`
   - **Branch**: `main`
   - **Root Directory**: `web-frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
   - **Plan**: **Free**

### 2.2 Set Environment Variable
1. Scroll to **"Environment Variables"**
2. Add:
   ```
   VITE_API_URL=https://chemviz-backend.onrender.com/api
   ```
   (Use your actual backend URL from Step 1.6)

### 2.3 Deploy
1. Click **"Create Static Site"**
2. Render will build and deploy (takes 2-3 minutes)
3. Copy your frontend URL: `https://chemviz-frontend.onrender.com`

---

## Step 3: Update CORS Settings

### 3.1 Go Back to Backend Service
1. Click on your `chemviz-backend` service
2. Go to **"Environment"** tab
3. Click **"Add Environment Variable"**

### 3.2 Update CORS Variables
Update these two variables with your frontend URL:

```
CORS_ALLOWED_ORIGINS=https://chemviz-frontend.onrender.com
```

```
CSRF_TRUSTED_ORIGINS=https://chemviz-frontend.onrender.com
```

### 3.3 Save and Redeploy
1. Click **"Save Changes"**
2. Render will automatically redeploy
3. Wait for deployment to complete

---

## Step 4: Test Your Deployment

1. Visit your frontend URL: `https://chemviz-frontend.onrender.com`
2. Register a new account
3. Upload `sample_equipment_data.csv`
4. Check dashboard and visualization

**Done!** 🎉

---

## ⚠️ Important Notes about Render Free Tier

### Free Tier Limitations:
- **Spins down after 15 minutes of inactivity**
- First request after spin-down takes ~30 seconds (cold start)
- **512 MB RAM**
- **0.1 CPU share**

### To Keep Service Active:
- Use a service like UptimeRobot (free) to ping your backend every 5 minutes
- Or upgrade to Starter plan ($7/month) for always-on

### Setting Up UptimeRobot (Free):
1. Go to https://uptimerobot.com
2. Sign up (free)
3. Add Monitor:
   - Type: HTTP(s)
   - URL: `https://chemviz-backend.onrender.com/api/health/`
   - Interval: 5 minutes
4. This will keep your service awake!

---

## 🆘 Troubleshooting

### Backend Issues

**"Build failed":**
- Check build logs in Render dashboard
- Make sure `gunicorn` is in requirements.txt ✅
- Verify Python version (should be 3.8+)

**"Database connection error":**
- Verify database is linked in "Environment" tab
- Check `DATABASE_URL` is set correctly
- Make sure database is running

**"Application error":**
- Check logs in Render dashboard
- Verify all environment variables are set
- Check start command is correct

### Frontend Issues

**"Build failed":**
- Check build logs
- Verify `VITE_API_URL` is set
- Make sure all dependencies are in package.json

**"CORS error":**
- Update `CORS_ALLOWED_ORIGINS` with exact frontend URL
- Include `https://` prefix
- Redeploy backend

---

## ✅ Alternative: Vercel for Frontend (Recommended)

If Render frontend is slow, use **Vercel** for frontend (it's faster and always free):

1. Go to https://vercel.com
2. Import your GitHub repo
3. Root Directory: `web-frontend`
4. Environment Variable: `VITE_API_URL=https://chemviz-backend.onrender.com/api`
5. Deploy!

Then update CORS in Render backend to point to Vercel URL.

---

**Your app is now live on Render!** 🚀

