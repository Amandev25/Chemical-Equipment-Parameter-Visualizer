# ⚡ Quick Deploy - 5 Minutes

The absolute fastest way to get your app online!

## 🎯 Railway + Vercel (Recommended)

### Backend (Railway) - 3 minutes

1. Go to https://railway.app → Sign up (GitHub login)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Click on the service → Settings:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`
5. Click "New" → "Database" → "PostgreSQL" (free)
6. Go to "Variables" tab, add:
   ```
   DEBUG=True
   SECRET_KEY=your-random-50-char-string-here
   ALLOWED_HOSTS=*.railway.app
   ```
7. Copy your backend URL (e.g., `https://xxx.up.railway.app`)

### Frontend (Vercel) - 2 minutes

1. Go to https://vercel.com → Sign up (GitHub login)
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Settings:
   - Framework: Vite
   - Root Directory: `web-frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. Environment Variables:
   - `VITE_API_URL` = `https://xxx.up.railway.app/api` (your Railway URL)
6. Click "Deploy"
7. Copy your frontend URL (e.g., `https://xxx.vercel.app`)

### Final Step - Update CORS

1. Go back to Railway
2. Add to Variables:
   ```
   CORS_ALLOWED_ORIGINS=https://xxx.vercel.app
   CSRF_TRUSTED_ORIGINS=https://xxx.vercel.app
   ```
3. Railway will auto-redeploy

**Done!** Visit your Vercel URL and test! 🚀

---

## 🔑 Generate Secret Key

Run this in Python:
```python
import secrets
print(secrets.token_urlsafe(50))
```

Or use: https://djecrety.ir/

---

## ✅ Test Your Deployment

1. Visit frontend URL
2. Register a new account
3. Upload `sample_equipment_data.csv`
4. Check dashboard

If it works, you're live! 🎉

---

## 🆘 Quick Fixes

**Backend not starting?**
- Check Railway logs
- Make sure `gunicorn` is in requirements.txt ✅

**CORS errors?**
- Add frontend URL to `CORS_ALLOWED_ORIGINS`
- Include `https://` prefix

**Can't connect to API?**
- Check `VITE_API_URL` ends with `/api`
- Verify backend URL is correct

---

That's it! Simple and fast! 🚀

