# Render.com Deployment Configuration

## Backend Deployment Steps

1. **Prepare Repository:**
   - Push all files to GitHub repository
   - Ensure requirements.txt is in root directory

2. **Create Render Service:**
   - Go to https://render.com
   - Connect your GitHub account
   - Create new "Web Service"
   - Select your repository

3. **Configure Service:**
   ```
   Name: hometag-housing-api
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port 10000
   ```

4. **Environment Variables:**
   ```
   CENSUS_API_KEY = your_actual_census_api_key_here
   ```

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Note the service URL (e.g., https://hometag-housing-api.onrender.com)

## Frontend Deployment Steps

1. **Update API Endpoint:**
   - Edit HousingDataTool.jsx
   - Change API_ENDPOINT to your Render service URL
   ```javascript
   const API_ENDPOINT = "https://hometag-housing-api.onrender.com/api/housing-data/";
   ```

2. **Build React App:**
   ```bash
   npm run build
   ```

3. **Upload to Web Server:**
   - Upload contents of `build/` folder to `www.hometagdirect.com/results`
   - Ensure index.html is accessible at `/results`

## Health Check

After deployment, test these URLs:
- Backend health: https://your-service.onrender.com/
- API test: https://your-service.onrender.com/api/housing-data/?zip_codes=33065
- Frontend: https://www.hometagdirect.com/results

## Production Environment Variables

```bash
CENSUS_API_KEY=your_actual_key_here
PORT=10000
```

## Monitoring

- Render provides logs and metrics dashboard
- Monitor API usage to stay within Census API limits
- Set up alerts for service downtime
