# 🚀 Simple Deployment Guide

Quick and easy deployment guide for getting your app online fast!

---

## 📦 Option 1: Railway (Easiest - Recommended)

### Backend Deployment (Railway)

1. **Go to [railway.app](https://railway.app)** and sign up/login

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select your repository

3. **Configure Backend**
   - Railway will auto-detect Django
   - Set root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`
   - Or Railway will use `railway.json` automatically if present

4. **Add PostgreSQL Database**
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway will automatically set `DATABASE_URL`

5. **Set Environment Variables**
   - Click on your service → "Variables"
   - Add these:
     ```
     DEBUG=True
     SECRET_KEY=your-random-secret-key-here-min-50-chars
     ALLOWED_HOSTS=*.railway.app
     CORS_ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
     CSRF_TRUSTED_ORIGINS=https://your-frontend-url.vercel.app
     ```

6. **Deploy!**
   - Railway will automatically deploy
   - Get your backend URL (e.g., `https://your-app.railway.app`)

### Frontend Deployment (Vercel)

1. **Go to [vercel.com](https://vercel.com)** and sign up/login

2. **Import Project**
   - Click "Add New" → "Project"
   - Import from GitHub
   - Select your repository

3. **Configure Frontend**
   - Framework Preset: Vite
   - Root Directory: `web-frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **Set Environment Variable**
   - Add: `VITE_API_URL` = `https://your-backend.railway.app/api`
   - (Use the URL from Railway backend)

5. **Deploy!**
   - Click "Deploy"
   - Get your frontend URL (e.g., `https://your-app.vercel.app`)

6. **Update Backend CORS**
   - Go back to Railway
   - Update `CORS_ALLOWED_ORIGINS` with your Vercel URL
   - Redeploy backend

**Done!** 🎉 Your app is live!

---

## 📦 Option 2: Render (Free Tier)

### Backend Deployment (Render)

1. **Go to [render.com](https://render.com)** and sign up

2. **Create New Web Service**
   - Click "New" → "Web Service"
   - Connect GitHub repository

3. **Configure**
   - Name: `chemviz-backend`
   - Environment: Python 3
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`

4. **Add PostgreSQL**
   - Click "New" → "PostgreSQL"
   - Render will set `DATABASE_URL` automatically

5. **Environment Variables**
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=your-app.onrender.com
   CORS_ALLOWED_ORIGINS=https://your-frontend.onrender.com
   ```

6. **Deploy!**

### Frontend Deployment (Render)

1. **Create New Static Site**
   - Click "New" → "Static Site"
   - Connect GitHub repository

2. **Configure**
   - Build Command: `cd web-frontend && npm install && npm run build`
   - Publish Directory: `web-frontend/dist`

3. **Environment Variable**
   - `VITE_API_URL` = `https://your-backend.onrender.com/api`

4. **Deploy!**

---

## 📦 Option 3: Heroku (Simple but Limited Free Tier)

### Backend (Heroku)

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login**
   ```bash
   heroku login
   ```

3. **Create App**
   ```bash
   cd backend
   heroku create your-app-name-backend
   ```

4. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set DEBUG=True
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set ALLOWED_HOSTS=your-app-name-backend.herokuapp.com
   ```

6. **Deploy**
   ```bash
   git push heroku main
   ```

### Frontend (Vercel - Same as Option 1)

Use Vercel for frontend (it's easier than Heroku for static sites).

---

## ⚙️ Quick Configuration

### Minimal Environment Variables Needed

**Backend:**
```env
DEBUG=True
SECRET_KEY=any-random-string-at-least-50-characters-long
ALLOWED_HOSTS=your-backend-url.com
CORS_ALLOWED_ORIGINS=https://your-frontend-url.com
CSRF_TRUSTED_ORIGINS=https://your-frontend-url.com
```

**Frontend:**
```env
VITE_API_URL=https://your-backend-url.com/api
```

### Generate Secret Key

```python
# Run this in Python
import secrets
print(secrets.token_urlsafe(50))
```

Or use this online: https://djecrety.ir/

---

## 🔧 Quick Fixes

### If Backend Won't Start

1. **Check logs** in Railway/Render dashboard
2. **Common issues:**
   - Missing `gunicorn` in requirements.txt ✅ (already added)
   - Wrong start command
   - Database connection error

### If Frontend Can't Connect to Backend

1. **Check CORS settings** - Make sure frontend URL is in `CORS_ALLOWED_ORIGINS`
2. **Check API URL** - Verify `VITE_API_URL` is correct
3. **Check backend is running** - Visit backend URL in browser

### Database Migration

If you need to run migrations manually:

**Railway:**
- Go to your service → "Deployments" → Click on deployment → "View Logs"
- Or use Railway CLI: `railway run python manage.py migrate`

**Render:**
- Add this to build command: `cd backend && python manage.py migrate && ...`

---

## 📝 Step-by-Step: Railway + Vercel (Recommended)

### Step 1: Deploy Backend (Railway)

1. Sign up at railway.app
2. New Project → Deploy from GitHub
3. Select repo
4. Add PostgreSQL database
5. Set variables:
   - `DEBUG=True`
   - `SECRET_KEY=generate-one`
   - `ALLOWED_HOSTS=*.railway.app`
6. Copy backend URL (e.g., `https://xxx.railway.app`)

### Step 2: Deploy Frontend (Vercel)

1. Sign up at vercel.com
2. Import from GitHub
3. Set root: `web-frontend`
4. Add env var: `VITE_API_URL=https://xxx.railway.app/api`
5. Deploy
6. Copy frontend URL (e.g., `https://xxx.vercel.app`)

### Step 3: Update CORS

1. Go back to Railway
2. Update `CORS_ALLOWED_ORIGINS` with Vercel URL
3. Update `CSRF_TRUSTED_ORIGINS` with Vercel URL
4. Redeploy

### Step 4: Test

1. Visit your Vercel URL
2. Register/Login
3. Upload CSV
4. Check dashboard

**That's it!** 🎉

---

## 💡 Tips

- **Railway** gives you $5 free credit monthly
- **Vercel** has generous free tier
- **Render** has free tier but slower cold starts
- Always check logs if something doesn't work
- Test locally first before deploying

---

## 🆘 Troubleshooting

### "Application Error" on Railway/Render
- Check logs in dashboard
- Verify all environment variables are set
- Make sure database is connected

### "CORS Error" in Browser
- Add frontend URL to `CORS_ALLOWED_ORIGINS`
- Include `https://` in URL
- Redeploy backend

### "404 Not Found" on API calls
- Check `VITE_API_URL` ends with `/api`
- Verify backend is running
- Check API routes in backend logs

### Database Connection Error
- Verify database is created
- Check `DATABASE_URL` is set (auto-set by Railway/Render)
- Run migrations: `python manage.py migrate`

---

## ✅ Deployment Checklist

- [ ] Backend deployed and running
- [ ] Frontend deployed and running
- [ ] Database connected
- [ ] Environment variables set
- [ ] CORS configured
- [ ] Can access frontend URL
- [ ] Can register/login
- [ ] Can upload CSV
- [ ] Can view dashboard

---

**Need help?** Check the logs in your deployment platform's dashboard!

