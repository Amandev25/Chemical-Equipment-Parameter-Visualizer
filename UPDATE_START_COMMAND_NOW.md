# 🚨 Update Start Command in Render NOW

## The Problem
Render is still using the old command with `cd backend &&`, which causes the error.

## ✅ Fix: Update Manually in Render Dashboard

### Step 1: Go to Render Dashboard
1. Open https://dashboard.render.com
2. Click your service: `chemical-equipment-parameter-visualizer-1`

### Step 2: Update Start Command
1. Click **Settings** tab
2. Scroll to **Build & Deploy** section
3. Find **Start Command** field
4. **Delete everything** in that field
5. **Paste this exactly:**
   ```bash
   python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
   ```
6. **IMPORTANT:** Make sure there's NO `cd backend &&` at the beginning!

### Step 3: Check Root Directory
While you're in Settings → Build & Deploy:
1. Look for **Root Directory** field
2. It should say: `backend`
3. If it's empty, set it to: `backend`

### Step 4: Save and Redeploy
1. Scroll down and click **Save Changes**
2. Go to **Manual Deploy** tab
3. Click **"Clear build cache & deploy"**
4. Wait 3-5 minutes for deployment

---

## ✅ Correct Configuration

**Root Directory:** `backend`

**Start Command:**
```bash
python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

**Build Command:**
```bash
cd backend && pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py collectstatic --noinput
```

---

## Why This Works

- **Root Directory = `backend`** means Render starts in the `backend` folder
- So you DON'T need `cd backend` in Start Command
- But Build Command still needs `cd backend` because it runs from repo root

---

**Do this now and redeploy!** 🚀

