from recommendation_engine import RecommendationEngine
import pandas as pd

def get_coords_for_city(city_name, df):
    """Finds the latitude and longitude for a city from the dataframe."""
    city_name = city_name.strip().lower()
    city_data = df[df['location_city'].str.lower() == city_name]
    if not city_data.empty:
        return city_data.iloc[0]['latitude'], city_data.iloc[0]['longitude']
    return None, None

def run_interactive_session():
    """Runs a full interactive session to get user input and provide recommendations."""
    
    print("--- Welcome to Disha Sahayak AI Assistant ---")
    
    # Load the engine and data
    try:
        engine = RecommendationEngine('internships.csv')
        internship_data = pd.read_csv('internships.csv')
    except FileNotFoundError:
        print("\n[ERROR] The 'internships.csv' file was not found.")
        print("Please run 'python generate_data.py' first to create the data file.")
        return
    
    # --- Get User Input ---
    user_education = input("1. Enter your highest education (e.g., 12th Pass, Graduate): ")
    
    lat, lon = None, None
    while not lat:
        user_location_city = input("2. Enter the city where you want your internship: ")
        lat, lon = get_coords_for_city(user_location_city, internship_data)
        if not lat:
            print(f"   Sorry, '{user_location_city}' was not found. Please try another city.")

    user_skills = input("3. Enter your skills (e.g., MS Excel, Communication): ")
    
    try:
        user_min_stipend = int(input("4. Enter your minimum desired monthly stipend (e.g., 8000): "))
    except ValueError:
        print("   Invalid number. Defaulting to a minimum stipend of 0.")
        user_min_stipend = 0

    priority = ""
    while priority not in ['skills', 'location', 'education', 'stipend']:
        priority = input("5. What is your TOP priority? (type 'skills', 'location', 'education', or 'stipend'): ").lower()
        if priority not in ['skills', 'location', 'education', 'stipend']:
            print("   Invalid choice. Please type one of the four options.")

    # --- Create the user's profile for the AI model ---
    user_profile = {
        'education': user_education,
        'skills': user_skills,
        'latitude': lat,
        'longitude': lon,
        'min_stipend': user_min_stipend
    }

    # --- Get and Print the Recommendations ---
    recommendations = engine.get_recommendations(user_profile, priority=priority, top_n=4)

    print("\n\n--- Here are your top 4 personalized internship recommendations ---")
    if recommendations.empty:
        print("Sorry, no matching internships were found based on your profile and criteria.")
    else:
        for index, row in recommendations.iterrows():
            print("\n" + "="*60)
            print(f"🌟 {row['title'].upper()} 🌟")
            print(f"   Match Score: {row['match_score_percent']}%")
            print("-"*60)
            print(f"📍 Location:         {row['location_city']}")
            print(f"💰 Stipend:          ₹{row['stipend']} / month")
            print(f"🎓 Education:        {row['education_required']}")
            print(f"🛠️ Skills Required:  {row['skills_required']}")
            print("="*60)

if __name__ == '__main__':
    run_interactive_session()

