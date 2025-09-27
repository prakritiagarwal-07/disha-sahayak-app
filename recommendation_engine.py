import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# --- Helper Functions ---
def preprocess_text(text):
    """Cleans and standardizes text data."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s,]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculates the distance between two points on Earth."""
    R = 6371  # Radius of Earth in kilometers
    lat1_rad, lon1_rad = np.radians(lat1), np.radians(lon1)
    lat2_rad, lon2_rad = np.radians(lat2), np.radians(lon2)
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def calculate_location_score(distance, max_distance=100):
    """Converts distance to a score from 0 to 1."""
    if distance > max_distance:
        return 0
    return 1 - (distance / max_distance)

# --- Main Recommendation Engine Class ---
class RecommendationEngine:
    """The main class for generating internship recommendations."""

    WEIGHTS = {
        'skills': 0.25,
        'location': 0.25,
        'education': 0.25,
        'stipend': 0.25
    }

    def __init__(self, internships_filepath):
        self.internships_df = self._load_and_preprocess_data(internships_filepath)
        self.tfidf_vectorizer, self.internship_skill_matrix = self._build_skill_matrix()

    def _load_and_preprocess_data(self, filepath):
        df = pd.read_csv(filepath)
        # Create a combined text field for TF-IDF analysis
        df['combined_text'] = df['title'] + ' ' + df['description'] + ' ' + df['skills_required'] + ' ' + df['education_required']
        df['processed_text'] = df['combined_text'].apply(preprocess_text)
        # Create a separate processed field for education matching
        df['education_processed'] = df['education_required'].apply(preprocess_text)
        return df

    def _build_skill_matrix(self):
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        internship_skill_matrix = tfidf_vectorizer.fit_transform(self.internships_df['processed_text'])
        return tfidf_vectorizer, internship_skill_matrix

    # --- NEW METHOD TO FIX THE ERROR ---
    def get_city_coords(self, city_name):
        """
        Finds the latitude and longitude for a given city name from the dataset.
        This is the missing function that the API needs.
        """
        # Clean the input city name for a reliable match
        city_name_processed = preprocess_text(city_name)
        
        # Search for the city in the dataframe (case-insensitive)
        city_match = self.internships_df[self.internships_df['location_city'].str.lower() == city_name_processed]
        
        if not city_match.empty:
            # Return the coordinates of the first match
            return {
                'latitude': city_match.iloc[0]['latitude'],
                'longitude': city_match.iloc[0]['longitude']
            }
        return None # Return None if the city is not found

    def get_recommendations(self, user_profile, priority='skills', top_n=4):
        # 1. Hard Filter: Remove internships below the user's minimum stipend
        min_stipend_requested = user_profile.get('min_stipend', 0)
        eligible_internships = self.internships_df[self.internships_df['stipend'] >= min_stipend_requested].copy()

        if eligible_internships.empty:
            return pd.DataFrame() # Return empty if no internships meet stipend criteria

        # 2. Calculate Skill Score
        user_input_text = f"{user_profile['skills']} {user_profile['education']}"
        user_skills_processed = preprocess_text(user_input_text)
        user_vector = self.tfidf_vectorizer.transform([user_skills_processed])
        skill_scores = cosine_similarity(user_vector, self.internship_skill_matrix).flatten()
        eligible_internships['skill_score'] = skill_scores[eligible_internships.index]

        # 3. Calculate Location Score
        user_lat, user_lon = user_profile['latitude'], user_profile['longitude']
        eligible_internships['distance_km'] = eligible_internships.apply(
            lambda row: haversine_distance(user_lat, user_lon, row['latitude'], row['longitude']), axis=1
        )
        eligible_internships['location_score'] = eligible_internships['distance_km'].apply(calculate_location_score)

        # 4. Calculate Education Score
        user_education_processed = preprocess_text(user_profile['education'])
        eligible_internships['education_score'] = (eligible_internships['education_processed'] == user_education_processed).astype(float)

        # 5. Calculate Stipend Score
        max_stipend = eligible_internships['stipend'].max()
        min_stipend = eligible_internships['stipend'].min()
        if max_stipend > min_stipend:
            eligible_internships['stipend_score'] = (eligible_internships['stipend'] - min_stipend) / (max_stipend - min_stipend)
        else:
            eligible_internships['stipend_score'] = 1.0

        # 6. Dynamically Adjust Weights based on Priority
        current_weights = self.WEIGHTS.copy()
        if priority in current_weights:
            current_weights[priority] = 0.60
            other_weight = (1.0 - 0.60) / (len(current_weights) - 1)
            for key in current_weights:
                if key != priority:
                    current_weights[key] = other_weight
        
        # 7. Calculate Final Match Score
        eligible_internships['match_score'] = (
            current_weights['skills'] * eligible_internships['skill_score'] +
            current_weights['location'] * eligible_internships['location_score'] +
            current_weights['education'] * eligible_internships['education_score'] +
            current_weights['stipend'] * eligible_internships['stipend_score']
        )
        
        # 8. Normalize and Sort
        max_score = eligible_internships['match_score'].max()
        if max_score > 0:
            eligible_internships['match_score_percent'] = (eligible_internships['match_score'] / max_score * 100).round(0).astype(int)
        else:
            eligible_internships['match_score_percent'] = 0
            
        recommendations = eligible_internships.sort_values(by='match_score', ascending=False).head(top_n)
        
        return recommendations[['internship_id', 'title', 'location_city', 'stipend', 'education_required', 'skills_required', 'match_score_percent']]

