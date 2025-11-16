# 🔧 Fix "No open ports detected" on Render

## The Problem
```
No open ports detected, continuing to scan...
```

This means Render can't detect which port your app is listening on.

---

## ✅ Solution: Update Start Command in Render Dashboard

### Option 1: Update via Render Dashboard (Recommended)

1. **Go to Render Dashboard:**
   - https://dashboard.render.com
   - Click your service: `chemical-equipment-parameter-visualizer-1`

2. **Go to Settings:**
   - Click **"Settings"** tab (left sidebar)

3. **Update Start Command:**
   - Find **"Start Command"** field
   - Set it to:
     ```
     cd backend && python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
     ```
   - **Important:** Make sure `$PORT` is included (Render sets this automatically)

4. **Check Root Directory:**
   - Make sure **"Root Directory"** is set to: (empty or project root)
   - If it's set to `backend`, remove `cd backend` from the start command

5. **Save Changes:**
   - Click **"Save Changes"**
   - Render will redeploy automatically

---

### Option 2: Check Environment Variables

1. **Go to Environment tab:**
   - Click **"Environment"** tab

2. **Verify PORT is set:**
   - Render automatically sets `PORT` environment variable
   - You don't need to set it manually
   - If you see `PORT` in the list, that's fine (Render sets it)

---

## ✅ Verify It's Working

After redeploy, check **"Logs"** tab:

**✅ Good signs:**
```
[INFO] Starting gunicorn...
[INFO] Listening at: http://0.0.0.0:10000
Your service is live 🎉
```

**❌ Bad signs:**
```
No open ports detected
Application exited early
```

---

## 🔍 Debug Steps

### Step 1: Check Logs
1. Go to **"Logs"** tab in Render
2. Look for:
   - `Listening at: http://0.0.0.0:XXXXX` (should see a port number)
   - Any error messages

### Step 2: Check Start Command
1. Go to **"Settings"** tab
2. Verify **Start Command** is:
   ```
   cd backend && python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
   ```

### Step 3: Check Root Directory
1. In **"Settings"** tab
2. Check **"Root Directory"**:
   - If empty or project root → Use `cd backend` in start command
   - If set to `backend` → Remove `cd backend` from start command

---

## ✅ Correct Start Command Format

**If Root Directory is empty (project root):**
```
cd backend && python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

**If Root Directory is set to `backend`:**
```
python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

---

**Update the Start Command in Render Dashboard and redeploy!** 🚀

