# ⚡ Quick Deploy Web UI (5 Minutes)

## 🎯 Quick Steps

### 1️⃣ Vercel Setup
- Go to https://vercel.com
- Sign in with GitHub
- Click **"Add New"** → **"Project"**
- Import: `Chemical-Equipment-Parameter-Visualizer`

### 2️⃣ Configure
- **Root Directory**: `web-frontend`
- **Framework**: Vite (auto-detected)
- **Build Command**: `npm run build` (auto)
- **Output Directory**: `dist` (auto)

### 3️⃣ Environment Variable
- **Key**: `VITE_API_URL`
- **Value**: `https://chemical-equipment-parameter-visualizer-1.onrender.com/api`

### 4️⃣ Deploy
- Click **"Deploy"**
- Wait 1-2 minutes
- **Copy your Vercel URL**

### 5️⃣ Update Backend CORS
- Go to https://dashboard.render.com
- Your service → **Environment** tab
- Add (⚠️ NO trailing slash `/`):
  - `CORS_ALLOWED_ORIGINS` = `https://your-vercel-url.vercel.app`
  - `CSRF_TRUSTED_ORIGINS` = `https://your-vercel-url.vercel.app`
- Wait for auto-redeploy

### 6️⃣ Test
- Visit your Vercel URL
- Register → Login → Upload CSV → Check Dashboard

---

**Done!** 🎉

