# ✅ Frontend Deployment Checklist

## Quick Steps (5 minutes)

### 1️⃣ Deploy to Vercel
- [ ] Go to https://vercel.com
- [ ] Import GitHub repo: `Chemical-Equipment-Parameter-Visualizer`
- [ ] Set **Root Directory**: `web-frontend`
- [ ] Add **Environment Variable**:
  - Key: `VITE_API_URL`
  - Value: `https://chemical-equipment-parameter-visualizer-1.onrender.com/api`
- [ ] Click **Deploy**
- [ ] **Copy your Vercel URL** (e.g., `https://your-app.vercel.app`)

### 2️⃣ Update Backend CORS
- [ ] Go to https://dashboard.render.com
- [ ] Open your backend service
- [ ] Go to **Environment** tab
- [ ] Add/Update these variables:

**CORS_ALLOWED_ORIGINS:**
```
https://your-vercel-url.vercel.app
```

**CSRF_TRUSTED_ORIGINS:**
```
https://your-vercel-url.vercel.app
```

- [ ] Click **Save Changes** (auto-redeploys)

### 3️⃣ Test Everything
- [ ] Visit your Vercel URL
- [ ] Register a new account
- [ ] Login
- [ ] Upload CSV file
- [ ] Check Dashboard
- [ ] Check Visualization page

---

## 🎉 Done!

Your full-stack app is live!

**Frontend**: `https://your-app.vercel.app`  
**Backend**: `https://chemical-equipment-parameter-visualizer-1.onrender.com`

