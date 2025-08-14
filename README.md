# HomeTag Housing Data Tool

A web application for analyzing housing and business data using the U.S. Census API. Perfect for real estate professionals, marketing campaigns, and demographic research.

## 🚀 Live Demo

- **Frontend**: [https://super-phoenix-108888134.netlify.app/](https://super-phoenix-108888134.netlify.app/)
- **API**: Deploy to Render.com for global access

## ✨ Features

- 📊 Real-time housing data from U.S. Census API
- 🏠 Owner-occupied vs renter-occupied statistics
- 🏘️ Single-family vs apartment breakdowns
- 🏢 Business establishment counts
- 🎯 Filtering by minimum owner-occupancy percentage
- 📱 Responsive design for mobile and desktop

## 🛠️ Tech Stack

- **Frontend**: React (via CDN), HTML5, CSS3
- **Backend**: FastAPI, Python
- **Data Source**: U.S. Census API (ACS 5-year & Business Patterns)
- **Deployment**: Netlify (frontend) + Render.com (backend)

## 🚀 Quick Deploy to Render.com

### Automatic Deployment:
1. Fork this repository
2. Sign up at [render.com](https://render.com)
3. Create a new "Web Service"
4. Connect your GitHub repository
5. Add environment variable: `CENSUS_API_KEY=your_key_here`
6. Deploy!

## Project Structure

```
├── main.py                 # FastAPI backend application
├── requirements.txt        # Python dependencies
├── HousingDataTool.jsx    # React frontend component
├── README.md              # This file
├── .env.example           # Environment variables template
└── deployment/            # Deployment configurations
```

## Prerequisites

- Python 3.8+
- Node.js 16+ (for React frontend)
- U.S. Census API Key (free from https://api.census.gov/data/key_signup.html)

## Setup Instructions

### 1. Get Census API Key

1. Visit https://api.census.gov/data/key_signup.html
2. Request a free API key
3. Save the key for environment configuration

### 2. Backend Setup (FastAPI)

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variable:
```bash
# Windows
set CENSUS_API_KEY=your_actual_api_key_here

# Mac/Linux  
export CENSUS_API_KEY=your_actual_api_key_here
```

3. Run the development server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. Test the API:
   - Open http://localhost:8000 in your browser
   - API docs available at http://localhost:8000/docs
   - Test endpoint: http://localhost:8000/api/housing-data/?zip_codes=33065

### 3. Frontend Setup (React)

1. Update the `API_ENDPOINT` constant in `HousingDataTool.jsx`:
```javascript
const API_ENDPOINT = "http://localhost:8000/api/housing-data/"; // For development
// const API_ENDPOINT = "https://your-deployed-api.onrender.com/api/housing-data/"; // For production
```

2. Integrate into your existing React app or create a new one:
```bash
npx create-react-app housing-data-app
cd housing-data-app
# Copy HousingDataTool.jsx to src/
# Import and use in App.js
```

## API Usage

### Endpoint: GET /api/housing-data/

**Parameters:**
- `zip_codes` (required): List of ZIP codes to query
- `min_owner_occupied` (optional): Minimum percentage of owner-occupied units filter

**Example Request:**
```
GET /api/housing-data/?zip_codes=33065&zip_codes=33063&min_owner_occupied=50
```

**Response:**
```json
{
  "results": [
    {
      "zip_code": "33065",
      "total_units": 25847,
      "owner_occupied_units": 18234,
      "renter_occupied_units": 6543,
      "single_family_detached_units": 19876,
      "apartments_units": 3421,
      "business_establishments": 1247,
      "percent_owner_occupied": 70.54
    }
  ]
}
```

## Deployment

### Backend Deployment (Render.com)

1. Push code to GitHub repository
2. Connect repository to Render.com
3. Configure service:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`
   - **Environment Variable:** `CENSUS_API_KEY=your_actual_key`

### Frontend Deployment

1. Update API endpoint in `HousingDataTool.jsx` to production URL
2. Build the React app: `npm run build`
3. Upload build files to `www.hometagdirect.com/results`
4. Ensure web server serves files correctly

## Data Sources

- **Housing Data:** U.S. Census American Community Survey (ACS) 5-Year Data
- **Business Data:** U.S. Census ZIP Code Business Patterns

## Features

- **ZIP Code Analysis:** Enter multiple ZIP codes for batch processing
- **Filtering:** Filter results by minimum owner-occupied percentage
- **Responsive Design:** Works on desktop and mobile devices
- **Error Handling:** Graceful handling of API errors and missing data
- **Real-time Data:** Fetches latest available Census data

## Troubleshooting

### Common Issues

1. **"No data found" errors:**
   - Verify ZIP codes are valid 5-digit codes
   - Some ZIP codes may not have complete data

2. **API key errors:**
   - Ensure Census API key is valid and set in environment
   - Check API key hasn't exceeded rate limits

3. **CORS errors:**
   - Backend includes CORS middleware for development
   - For production, update allowed origins

### Development Notes

- API responses include error handling for missing or invalid data
- Frontend includes loading states and user feedback
- All numeric values are formatted for better readability
- Percentage calculations handle division by zero

## License

Internal tool for HomeTag Direct marketing purposes.

## Support

For technical issues or feature requests, contact the development team.
