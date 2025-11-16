# 🔧 Fix: "can't open file manage.py" Error

## The Problem
```
python: can't open file '/opt/render/project/src/backend/backend/manage.py': [Errno 2] No such file or directory
```

The path shows `backend/backend/manage.py` - this means **Root Directory is set to `backend`** in Render, so you don't need `cd backend` in the start command.

---

## ✅ Fix: Update Start Command in Render

### Step 1: Go to Render Dashboard
1. Open https://dashboard.render.com
2. Click your service: `chemical-equipment-parameter-visualizer-1`

### Step 2: Update Start Command
1. Go to **Settings** tab
2. Scroll to **Build & Deploy** section
3. Find **Start Command**
4. **Remove `cd backend &&`** from the beginning

**Current (Wrong):**
```bash
cd backend && python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

**Should be (Correct):**
```bash
python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

### Step 3: Update Build Command (if needed)
If Build Command also has `cd backend &&`, check if Root Directory is set:

**If Root Directory = `backend`:**
```bash
pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py collectstatic --noinput
```

**If Root Directory = empty (root of repo):**
```bash
cd backend && pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py collectstatic --noinput
```

### Step 4: Save and Redeploy
1. Click **Save Changes**
2. Go to **Manual Deploy** tab
3. Click **"Clear build cache & deploy"**
4. Wait for deployment (3-5 minutes)

---

## 🔍 How to Check Root Directory

1. Go to **Settings** → **Build & Deploy**
2. Look for **"Root Directory"** field
3. If it says `backend` → Don't use `cd backend` in commands
4. If it's empty → Use `cd backend` in commands

---

## ✅ After Fixing

The deployment should work! The start command will:
1. Run migrations: `python manage.py migrate`
2. Start Gunicorn: `gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`

---

**Quick Fix: Just remove `cd backend &&` from Start Command!** 🚀

