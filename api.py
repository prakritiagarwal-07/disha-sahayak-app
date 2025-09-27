from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse # NEW: Import this to serve HTML files
from pydantic import BaseModel
import pandas as pd
from recommendation_engine import RecommendationEngine

# --- 1. Application Setup ---
app = FastAPI(
    title="Disha Sahayak API",
    description="An AI-powered internship recommendation engine.",
    version="1.0.0"
)

# Allow all origins for simplicity during deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. Data Models for API ---
class UserProfile(BaseModel):
    education: str
    skills: str
    location_city: str
    min_stipend: int = 0

# --- 3. Load AI Model ---
try:
    engine = RecommendationEngine('internships.csv')
    print("--- Recommendation Engine and data loaded successfully. API is ready. ---")
except Exception as e:
    print(f"!!! CRITICAL ERROR: Could not load the recommendation engine. {e}")
    engine = None

# --- 4. API Endpoints ---

# NEW ENDPOINT: This serves your chatbot HTML file
@app.get("/", response_class=HTMLResponse)
async def serve_chatbot():
    """
    This is the main endpoint. It reads and returns the index.html file,
    so your chatbot is visible to users.
    """
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="index.html not found. Make sure the file is in the same directory as the API.")


@app.post("/recommendations/")
async def get_recommendations_endpoint(user_profile: UserProfile, priority: str = 'skills'):
    """
    The core API endpoint that takes a user's profile and priority,
    and returns personalized internship recommendations.
    """
    if not engine:
        raise HTTPException(status_code=503, detail="Recommendation engine is not available.")
    
    # Get location data (latitude/longitude) for the user's city
    city_data = engine.get_city_coords(user_profile.location_city)
    if city_data is None:
        raise HTTPException(status_code=404, detail=f"City '{user_profile.location_city}' not found in our database.")

    api_profile = {
        'education': user_profile.education,
        'skills': user_profile.skills,
        'latitude': city_data['latitude'],
        'longitude': city_data['longitude'],
        'min_stipend': user_profile.min_stipend
    }

    try:
        recommendations = engine.get_recommendations(api_profile, priority=priority, top_n=4)
        if recommendations.empty:
            return {"message": "No suitable internships found.", "recommendations": []}
        
        # Convert DataFrame to a list of dictionaries for JSON response
        results = recommendations.to_dict(orient='records')
        return {"recommendations": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while generating recommendations: {e}")

