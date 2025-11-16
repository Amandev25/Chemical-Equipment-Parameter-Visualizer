# 🔧 Fix: "No module named 'django'" Error

## The Problem
The error shows Render is using the **Start Command as Build Command**. The Build Command needs to **install dependencies first** before running migrations.

The log shows:
```
Running build command 'python manage.py migrate && gunicorn...'
```

This is wrong! The Build Command should install packages first.

---

## ✅ Fix: Update Build Command in Render

### Step 1: Go to Render Dashboard
1. Open https://dashboard.render.com
2. Click your service: `chemical-equipment-parameter-visualizer-1`

### Step 2: Update Build Command
1. Go to **Settings** tab
2. Scroll to **Build & Deploy** section
3. Find **Build Command** field
4. **Delete everything** in that field
5. **Paste this exactly:**
   ```bash
   cd backend && pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```

### Step 3: Verify Start Command
Make sure **Start Command** is:
```bash
python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

### Step 4: Verify Root Directory
- **Root Directory** should be: `backend`

### Step 5: Save and Redeploy
1. Click **Save Changes**
2. Go to **Manual Deploy** tab
3. Click **"Clear build cache & deploy"**
4. Wait 5-7 minutes for deployment

---

## ✅ Correct Configuration

**Root Directory:** `backend`

**Build Command:**
```bash
cd backend && pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py collectstatic --noinput
```

**Start Command:**
```bash
python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

---

## Why This Works

1. **Build Command** runs first:
   - Installs Python packages (Django, etc.)
   - Collects static files
   - Runs from repo root, so needs `cd backend`

2. **Start Command** runs after build:
   - Runs migrations
   - Starts Gunicorn server
   - Runs from `backend` directory (Root Directory), so NO `cd backend`

---

**Update the Build Command now and redeploy!** 🚀

