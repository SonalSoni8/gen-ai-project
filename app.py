import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests

# --- Initialize session state for theme choice ---
# This MUST be one of the very first Streamlit related lines, before st.set_page_config
if 'app_theme_choice' not in st.session_state:
    st.session_state.app_theme_choice = "Light" # Default to Light theme

# --- Page Configuration ---
# Must be the first Streamlit command (after imports and session_state init)
st.set_page_config(
    page_title="GreenLife AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed" # Sidebar is collapsed by default
)

# --- Define CSS for Light and Dark Themes ---
LIGHT_THEME_CSS = """
<style>
    body, .stApp {
        background-color: #FFFFFF;
        color: #262730;
    }
    /* General text elements */
    h1, h2, h3, h4, h5, h6, p, div[data-testid="stMarkdownContainer"] {
        color: #262730 !important;
    }
.st-ci {
    border: 1px solid rgb(19, 23, 32);
    background-color: white;
}
    /* --- Form Input Fields & Labels --- */
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stTextArea label,
    div[data-testid="stForm"] label { /* More general form label targeting */
        color: #262730 !important;
    }
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        color: #262730 !important; /* Text color inside input */
        background-color: #F9F9F9 !important; /* Slightly off-white background for input */
        border: 1px solid #D0D0D0 !important; /* Border for inputs */
        border-radius: 0.25rem !important;
    }
    .stTextInput input::placeholder,
    .stNumberInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #A0A0A0 !important;
    }
    .stSelectbox > div[data-baseweb="select"] > div:first-child { /* Main visible part of selectbox */
        color: #262730 !important;
        background-color: #F9F9F9 !important;
        border: 1px solid #D0D0D0 !important;
        border-radius: 0.25rem !important;
    }
    .stSelectbox > div[data-baseweb="select"] svg { /* Arrow icon */
        fill: #262730 !important;
    }

    /* Radio button labels (for theme toggle and any other radio buttons) */
    .stRadio > label { /* Main label of the radio group */
        color: #262730 !important;
        font-size: 0.9rem !important; /* Adjust size if needed */
        padding-bottom: 0px !important; /* Adjust spacing if needed */
    }
    .stRadio div[role="radiogroup"] label span { /* Individual radio option text */
        color: #262730 !important;
        font-size: 0.9rem !important; /* Adjust size if needed */
    }

    /* Buttons */
button {
    background-color: #1976D2 !important; /* Material Design Blue 700 */
    color: #fffff !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.4em 0.8em !important; /* Adjusted padding */
}
button p {
    color:#f4f5f9 !important;
}
 button:hover {
    background-color: #1565C0 !important; /* Blue 800 */
}
 button:active {
    background-color: #0D47A1 !important; /* Blue 900 */
}
 button:focus { /* Optional: for better accessibility */
    box-shadow: 0 0 0 0.2rem rgba(25, 118, 210, 0.5) !important;
}

    /* Expander styling */
    .stExpander > div:first-child {
        background-color: #F0F2F6; /* Light gray for expander header */
        color: #262730 !important;
    }
    .stExpander > div:first-child svg { /* Icon color in expander header */
        fill: #262730 !important;
    }

.st-er {
    background-color: rgb(244 246 248);
}
.st-cc {
    color: rgb(25 24 24);
}
    .st-emotion-cache-13na8ym, .st-emotion-cache-seewz2 hr {
    border-color: #22212133;
}
</style>
"""

DARK_THEME_CSS = """
<style>
    body, .stApp {
        background-color: #0E1117; /* Dark background */
        color: #FAFAFA; /* Light default text color */
    }
    h1, h2, h3, h4, h5, h6, p, div[data-testid="stMarkdownContainer"] {
        color: #FAFAFA !important;
    }

    /* --- Form Input Fields & Labels --- */
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stTextArea label,
    div[data-testid="stForm"] label {
        color: #FAFAFA !important;
    }
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        color: #FAFAFA !important;
        background-color: #262730 !important;
        border: 1px solid #4A4A4A !important;
        border-radius: 0.25rem !important;
    }
    .stTextInput input::placeholder,
    .stNumberInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #A0A0A0 !important;
    }
    .stSelectbox > div[data-baseweb="select"] > div:first-child {
        color: #FAFAFA !important;
        background-color: #262730 !important;
        border: 1px solid #4A4A4A !important;
        border-radius: 0.25rem !important;
    }
    .stSelectbox > div[data-baseweb="select"] svg {
        fill: #FAFAFA !important;
    }

    /* Radio button labels (for theme toggle and any other radio buttons) */
    .stRadio > label { /* Main label of the radio group */
        color: #FAFAFA !important;
        font-size: 0.9rem !important; /* Adjust size if needed */
        padding-bottom: 0px !important; /* Adjust spacing if needed */
    }
    .stRadio div[role="radiogroup"] label span { /* Individual radio option text */
        color: #FAFAFA !important;
        font-size: 0.9rem !important; /* Adjust size if needed */
    }

    /* Buttons */
 button {
    background-color: #2196F3 !important; /* Material Design Blue 500 (brighter for dark theme) */
    color: #fffff !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.4em 0.8em !important; /* Adjusted padding */
}
 button:hover {
    background-color: #1976D2 !important; /* Blue 700 */
}
 button:active {
    background-color: #0D47A1 !important; /* Blue 900 */
}
 button:focus { /* Optional: for better accessibility */
    box-shadow: 0 0 0 0.2rem rgba(33, 150, 243, 0.5) !important;
}

    /* Expander styling */
    .stExpander > div:first-child {
        background-color: #161B22; /* Darker gray for expander header */
        color: #FAFAFA !important;
    }
    .stExpander > div:first-child svg {
        fill: #FAFAFA !important;
    }
</style>
"""

# --- Apply selected theme's CSS ---
if st.session_state.app_theme_choice == "Dark":
    st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)
else:
    st.markdown(LIGHT_THEME_CSS, unsafe_allow_html=True)


# --- Environment and API Configuration ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Main App Content ---

# --- Title and Theme Toggle ---
col_title, col_toggle = st.columns([0.8, 0.2])

with col_title:
    st.title(" GreenLife AI 🌱- Your Sustainability Planner")

with col_toggle:
    # Callback function to update theme choice in session state
    def theme_changed_callback_main():
        st.session_state.app_theme_choice = st.session_state.theme_radio_main_page

    st.radio(
        label="App Theme:",
        options=("Light", "Dark"),
        index=("Light", "Dark").index(st.session_state.app_theme_choice),
        key="theme_radio_main_page", 
        on_change=theme_changed_callback_main,
        horizontal=True, 
    )
st.markdown("---") 

# User input form
with st.form("lifestyle_form"):
    st.write("### Enter your lifestyle details:")
    commute_km = st.number_input("Daily commute (in km):", 0, 100, value=10)
    electricity_kwh = st.number_input("Monthly electricity usage (kWh):", 0, 2000, value=300)
    diet_type = st.selectbox("Diet type:", ["Vegetarian", "Mixed", "Non-Vegetarian"])
    location = st.text_input("City/Location:", value="Gujarat")
    submitted = st.form_submit_button("Submit")

def calculate_footprint(commute_km, electricity_kwh, diet_type):
    commute_emission = commute_km * 0.271 * 30
    electricity_emission = electricity_kwh * 0.92
    diet_emission = {
        "Vegetarian": 1.5 * 30,
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

def get_ai_suggestions(commute_km, electricity_kwh, diet_type, location, current_footprint):
    prompt = f"""
    I'm a person living in {location} who commutes {commute_km} km daily, uses {electricity_kwh} kWh of electricity monthly,
    and follows a {diet_type} diet.
    My estimated monthly carbon footprint is approximately {current_footprint} kg CO₂.
    Suggest 5 simple, highly actionable, and realistic ways I can reduce my carbon footprint.
    For each suggestion, provide a brief explanation of why it helps and an estimated potential CO₂ reduction per month if applicable (can be a rough estimate or qualitative).
    Focus on advice tailored to my specific inputs (commute, electricity, diet, location if relevant for local context like public transport or renewable energy options).
    Present the suggestions as a numbered list.
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating AI suggestions: {e}")
        return "Could not retrieve suggestions. Check API key and model access."

if submitted and location:
    calculated_footprint = calculate_footprint(commute_km, electricity_kwh, diet_type)
    with st.spinner("Generating AI suggestions..."):
        suggestions = get_ai_suggestions(commute_km, electricity_kwh, diet_type, location, calculated_footprint)
        st.write("### ♻️ AI-Powered Sustainability Suggestions:")
        st.markdown(suggestions)

def find_green_places(location, keyword="organic store"):
    endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not maps_api_key:
        st.warning("Google Maps API key not configured. Cannot fetch nearby places.")
        return []
    params = {"query": f"{keyword} near {location}", "key": maps_api_key}
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
        for place in data["results"][:5]:
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
        keyword_options = ["organic store", "farmers market", "repair cafe", "bike shop", "bulk food store", "community garden", "EV charging station"]
        selected_keyword = st.selectbox("What are you looking for?", keyword_options, key="green_spot_keyword_main_page") 

        if selected_keyword:
            with st.spinner(f"Searching for '{selected_keyword}' near {location}..."):
                places = find_green_places(location, keyword=selected_keyword)
                if places:
                    for p in places:
                        st.markdown(f"**{p['name']}**\n\n📍 {p['address']}\n\n⭐ Rating: {p['rating']}\n\n---")
                elif os.getenv("GOOGLE_MAPS_API_KEY"):
                    st.info(f"No '{selected_keyword}' found nearby for '{location}', or an error occurred.")
else:
    if not submitted:
        st.info("👋 Welcome! Fill in your details above and click 'Submit' to get started.")
        st.markdown("""
            #### How GreenLife AI helps you:
            1.  **Estimate your carbon footprint.**
            2.  **Get AI-powered tips** for a greener lifestyle.
            3.  **Find eco-friendly places** in your area.
        """)

# --- Footer ---
st.markdown("---")
footer_style = "text-align: center; font-size: 0.8rem; color: #808080 !important;"
st.markdown(f"<div style='{footer_style}'>© 2025 GreenLife AI - Your Partner in Sustainability.</div>", unsafe_allow_html=True)
st.markdown(f"<div style='{footer_style}'>Estimates are for informational purposes only.</div>", unsafe_allow_html=True)
st.markdown(f"<div style='{footer_style}'>Powered by Google Gemini & Google Maps.</div>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #808080 !important; font-size: 0.8rem;'>Created by SONAL SONI</p>", unsafe_allow_html=True)