# Free Cloud Deployment Guide - Render.com

## 🆓 Deploy Your Housing Data Tool for FREE on Render.com

### Why Render.com?
- ✅ **Completely FREE** for 750 hours/month
- ✅ **Automatic HTTPS** included
- ✅ **Easy deployment** from GitHub
- ✅ **Supports Python/FastAPI** out of the box
- ✅ **Custom domain** support (free)

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your GitHub Repository
1. Create a new repository on GitHub
2. Upload these files from your project:
   ```
   main.py
   requirements.txt
   render.yaml
   index-production.html
   .env (without sensitive data - see step 3)
   ```

### Step 2: Sign Up for Render.com
1. Go to https://render.com
2. Sign up with your GitHub account (free)
3. Authorize Render to access your repositories

### Step 3: Deploy the API Backend
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `hometag-housing-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variable:
   - **Key**: `CENSUS_API_KEY`
   - **Value**: `7cc4d53e64e1ed3e009bd07ecd4838b5c542978a`
5. Click "Create Web Service"

### Step 4: Get Your API URL
After deployment (5-10 minutes), you'll get a URL like:
```
https://hometag-housing-api.onrender.com
```

### Step 5: Update Frontend
1. Edit `index-production.html`
2. Replace line 17:
   ```javascript
   const API_ENDPOINT = "https://hometag-housing-api.onrender.com/api/housing-data/";
   ```
3. Upload the updated file

### Step 6: Deploy Frontend (Optional)
You can also host the frontend on Render:
1. Create another service → "Static Site"
2. Upload your HTML file
3. Get frontend URL like: `https://hometag-frontend.onrender.com`

---

## 🧪 **Test Your Deployment**

### API Health Check:
```
https://your-api-name.onrender.com/
```

### Test with ZIP codes:
```
https://your-api-name.onrender.com/api/housing-data/?zip_codes=33065,33063
```

### Frontend Access:
```
https://your-frontend-name.onrender.com
```

---

## ⚡ **Quick Alternative: Static Frontend**

If you just want to test the frontend, use any of these FREE options:

### Netlify Drop (Instant):
1. Go to https://app.netlify.com/drop
2. Drag and drop your `index-production.html` file
3. Get instant URL: `https://random-name.netlify.app`

### Vercel:
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel --prod`
3. Deploy in seconds

### GitHub Pages:
1. Create GitHub repo
2. Upload `index-production.html` as `index.html`
3. Enable Pages in repo settings
4. Access at: `https://username.github.io/repo-name`

---

## 💡 **Pro Tips for Free Hosting**

### Render.com:
- ⚠️ **Sleep after 15min**: Free services sleep when idle
- 🔄 **First request slow**: Takes ~30 seconds to wake up
- 📊 **750 hours/month**: About 24/7 for 31 days
- 🆙 **Upgrade**: $7/month for always-on

### Performance Tips:
- Use a service like **UptimeRobot** (free) to ping your API every 5 minutes
- This keeps it awake during business hours
- Perfect for testing and demos

---

## 🎯 **Recommended Testing Flow**

1. **Start with Render.com** - Deploy both API and frontend
2. **Test thoroughly** - Make sure everything works
3. **Share with users** - Get feedback using the free URLs
4. **Upgrade when ready** - Move to paid hosting for production

Your app will be live and accessible worldwide in about 15 minutes! 🌍
