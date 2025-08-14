from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="HomeTag Housing Data API", version="1.0.0")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get Census API key from environment variable
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY", "YOUR_CENSUS_API_KEY_HERE")

# Validate API key
if CENSUS_API_KEY == "YOUR_CENSUS_API_KEY_HERE" or CENSUS_API_KEY == "111111abc":
    print("⚠️  WARNING: Using invalid Census API key!")
    print("📝 Get a real API key from: https://api.census.gov/data/key_signup.html")
    print("🔧 Update your .env file with: CENSUS_API_KEY=your_real_key_here")

def get_business_count(zip_code: str) -> Optional[int]:
    """Fetch business establishment count for a ZIP code from Census Business Patterns API"""
    url = (
        f"https://api.census.gov/data/2022/cbp"
        f"?get=ESTAB"
        f"&for=zip%20code%20tabulation%20area:{zip_code}"
        f"&key={CENSUS_API_KEY}"
    )
    try:
        r = requests.get(url, timeout=10)
        print(f"Business API Status: {r.status_code}, Response: {r.text[:200]}")
        
        if r.status_code != 200:
            print(f"Business API Error: {r.status_code} - {r.text}")
            return None
            
        data = r.json()
        if len(data) > 1:
            return int(data[1][0])
    except requests.exceptions.RequestException as e:
        print(f"Business API Request Error: {e}")
    except ValueError as e:
        print(f"Business API JSON Error: {e}")
    except Exception as e:
        print(f"Business API Unexpected Error: {e}")
    return None

@app.get("/")
def read_root():
    api_key_status = "✅ Valid" if CENSUS_API_KEY not in ["YOUR_CENSUS_API_KEY_HERE", "111111abc"] else "❌ Invalid/Demo"
    return {
        "message": "HomeTag Housing Data API", 
        "status": "running",
        "api_key_status": api_key_status,
        "note": "Get a real Census API key from https://api.census.gov/data/key_signup.html"
    }

@app.get("/test-api-key/")
def test_api_key():
    """Test if the Census API key is working"""
    if CENSUS_API_KEY in ["YOUR_CENSUS_API_KEY_HERE", "111111abc"]:
        return {
            "status": "error",
            "message": "Invalid API key. Please get a real key from https://api.census.gov/data/key_signup.html"
        }
    
    # Test with a simple API call
    test_url = f"https://api.census.gov/data/2022/acs/acs5?get=NAME&for=state:*&key={CENSUS_API_KEY}"
    try:
        response = requests.get(test_url, timeout=10)
        if response.status_code == 200:
            return {"status": "success", "message": "API key is working correctly"}
        else:
            return {"status": "error", "message": f"API returned status {response.status_code}: {response.text}"}
    except Exception as e:
        return {"status": "error", "message": f"API test failed: {str(e)}"}

@app.get("/api/housing-data/")
def get_housing_data(
    zip_codes: List[str] = Query(..., description="List of ZIP codes"),
    min_owner_occupied: Optional[float] = Query(None, description="Min % owner-occupied filter")
):
    """
    Fetch housing and business data for specified ZIP codes from U.S. Census API
    
    Parameters:
    - zip_codes: List of ZIP codes to query
    - min_owner_occupied: Optional filter for minimum percentage of owner-occupied units
    
    Returns detailed housing statistics including:
    - Total housing units
    - Owner-occupied units
    - Renter-occupied units  
    - Single-family detached homes
    - Apartments (multi-unit structures)
    - Business establishment counts
    """
    results = []

    for zip_code in zip_codes:
        try:
            # Fetch housing data from Census ACS 5-year API
            url = (
                f"https://api.census.gov/data/2022/acs/acs5"
                f"?get=B25001_001E,B25003_002E,B25003_003E,B25024_002E,B25032_010E"
                f"&for=zip%20code%20tabulation%20area:{zip_code}"
                f"&key={CENSUS_API_KEY}"
            )
            print(f"Housing API URL: {url}")
            
            res = requests.get(url, timeout=10)
            print(f"Housing API Status: {res.status_code}, Response: {res.text[:200]}")
            
            if res.status_code != 200:
                error_msg = f"API Error {res.status_code}: {res.text}"
                print(error_msg)
                results.append({"zip_code": zip_code, "error": error_msg})
                continue
                
            data = res.json()

            if len(data) < 2:
                results.append({"zip_code": zip_code, "error": "No data found"})
                continue

            headers, values = data
            total_units = int(values[0]) if values[0] != '-' else 0
            owner_occupied = int(values[1]) if values[1] != '-' else 0
            renter_occupied = int(values[2]) if values[2] != '-' else 0
            single_family_detached = int(values[3]) if values[3] != '-' else 0
            apartments = int(values[4]) if values[4] != '-' else 0

            percent_owner_occupied = round(owner_occupied / total_units * 100, 2) if total_units else 0
            business_count = get_business_count(zip_code)

            # Apply owner-occupied filter if specified
            if min_owner_occupied is not None and percent_owner_occupied < min_owner_occupied:
                continue

            results.append({
                "zip_code": zip_code,
                "total_units": total_units,
                "owner_occupied_units": owner_occupied,
                "renter_occupied_units": renter_occupied,
                "single_family_detached_units": single_family_detached,
                "apartments_units": apartments,
                "business_establishments": business_count if business_count is not None else "data_unavailable",
                "percent_owner_occupied": percent_owner_occupied,
            })

        except Exception as e:
            results.append({"zip_code": zip_code, "error": str(e)})

    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
