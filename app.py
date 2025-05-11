import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(
    page_title="GreenLife AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title(" GreenLife AI 🌱- Your Sustainability Planner")

# User input form
with st.form("lifestyle_form"):
    st.write("### Enter your lifestyle details:")
    commute_km = st.number_input("Daily commute (in km):", 0, 100, value=10) 
    electricity_kwh = st.number_input("Monthly electricity usage (kWh):", 0, 2000, value=300) 
    diet_type = st.selectbox("Diet type:", ["Vegetarian", "Mixed", "Non-Vegetarian"])
    location = st.text_input("City/Location:", value="San Francisco") 
    submitted = st.form_submit_button("Submit")

def calculate_footprint(commute_km, electricity_kwh, diet_type):
    # Basic carbon factors (simplified)
    commute_emission = commute_km * 0.271 * 30  # per month (assuming average car emissions)
    electricity_emission = electricity_kwh * 0.92 # average US grid intensity, can vary widely
    diet_emission = {
        "Vegetarian": 1.5 * 30,  # kg CO2e per day, very rough estimate
        "Mixed": 2.0 * 30,
        "Non-Vegetarian": 2.5 * 30
    }[diet_type]

    total_emission = commute_emission + electricity_emission + diet_emission
    return round(total_emission, 2)

if submitted:
    if not location:
        st.error("Please enter your City/Location.")
    else:
        total_emission = calculate_footprint(commute_km, electricity_kwh, diet_type)
        st.success(f"🌍 Your estimated monthly carbon footprint is: **{total_emission} kg CO₂**")

def get_ai_suggestions(commute_km, electricity_kwh, diet_type, location):
    prompt = f"""
    I'm a person living in {location} who commutes {commute_km} km daily, uses {electricity_kwh} kWh of electricity monthly,
    and follows a {diet_type} diet.

    My estimated monthly carbon footprint is approximately {calculate_footprint(commute_km, electricity_kwh, diet_type)} kg CO₂.

    Suggest 5 simple, highly actionable, and realistic ways I can reduce my carbon footprint.
    For each suggestion, provide a brief explanation of why it helps and an estimated potential CO₂ reduction per month if applicable (can be a rough estimate or qualitative).
    Focus on advice tailored to my specific inputs (commute, electricity, diet, location if relevant for local context like public transport or renewable energy options).
    Present the suggestions as a numbered list.
    """

    # --- Model ---
    model = genai.GenerativeModel("gemini-2.0-flash") # 
    # --- End Model ---

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating AI suggestions: {e}")
        return "Could not retrieve suggestions at this time. Please ensure your API key is valid and has access to the selected model."


if submitted and location: 
    with st.spinner("Generating AI suggestions..."):
        suggestions = get_ai_suggestions(commute_km, electricity_kwh, diet_type, location)
        st.write("### ♻️ AI-Powered Sustainability Suggestions:")
        st.markdown(suggestions)


def find_green_places(location, keyword="organic store"):
    endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    if not maps_api_key:
        st.warning("Google Maps API key not configured. Cannot fetch nearby places.")
        return []

    params = {
        "query": f"{keyword} near {location}",
        "key": maps_api_key
    }
    try:
        res = requests.get(endpoint, params=params)
        res.raise_for_status() 
        data = res.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching places from Google Maps API: {e}")
        return []
    except ValueError: 
        st.error("Error decoding response from Google Maps API.")
        return []


    results = []
    if "results" in data:
        for place in data["results"][:5]:  # top 5 places
            results.append({
                "name": place.get("name", "N/A"),
                "address": place.get("formatted_address", "Address not available"),
                "rating": place.get("rating", "N/A")
            })
    elif "error_message" in data:
        st.error(f"Google Maps API Error: {data['error_message']}")
    return results

if submitted and location:
    st.write("### 🌿 Nearby Eco-Friendly Places:")
    with st.expander("Find Local Green Spots (e.g., organic store, repair cafe, farmers market)", expanded=False):
        keyword_options = ["organic store", "farmers market", "repair cafe", "bike shop", "bulk food store", "community garden"]
        selected_keyword = st.selectbox("What are you looking for?", keyword_options)

        if selected_keyword:
            with st.spinner(f"Searching for '{selected_keyword}' near {location}..."):
                places = find_green_places(location, keyword=selected_keyword)
                if places:
                    for p in places:
                        st.markdown(f"**{p['name']}**\n\n📍 {p['address']}\n\n⭐ Rating: {p['rating']}\n\n---")
                elif os.getenv("GOOGLE_MAPS_API_KEY"): # Only show no results if API key was present
                    st.info(f"No '{selected_keyword}' found nearby, or an error occurred.")