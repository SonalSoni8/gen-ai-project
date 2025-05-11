# GreenLife AI - Your Personal Sustainability Planner 🌱

GreenLife AI is a Streamlit web application designed to help you understand and reduce your personal carbon footprint. It provides an estimated monthly carbon footprint based on your lifestyle inputs, offers AI-powered suggestions for sustainable living, and helps you find local eco-friendly places.

## ✨ Features

*   **Carbon Footprint Estimation:** Calculates an approximate monthly CO₂ footprint based on:
    *   Daily commute distance
    *   Monthly electricity usage
    *   Dietary choices
*   **AI-Powered Suggestions:** Leverages Google's Gemini AI model to provide personalized, actionable tips to reduce your environmental impact, tailored to your inputs and location.
*   **Local Green Spots Finder:** Uses the Google Maps Places API to help you discover nearby:
    *   Organic stores
    *   Farmers markets
    *   Repair cafes/shops
    *   Bike shops
    *   Bulk food stores
    *   Community gardens
    *   And more!
*   **User-Friendly Interface:** Built with Streamlit for an interactive and easy-to-use experience.

## 🛠️ Tech Stack

*   **Frontend:** Streamlit
*   **AI Model:** Google Gemini API (e.g., `gemini-1.5-pro-latest`, `gemini-1.5-flash-latest`, `gemini-2.0-flash`, any of your choice)
*   **Mapping/Places:** Google Maps Places API
*   **Language:** Python
*   **Environment Management:** `python-dotenv`

## 🚀 Setup and Installation

Follow these steps to get GreenLife AI running on your local machine.

### 1. Prerequisites

*   Python 3.8 or higher
*   `pip` (Python package installer)
*   Git (for cloning the repository)

### 2. Clone the Repository

######################################################## 

# Create a Virtual Environment (Recommended)
python -m venv venv


## Activate the virtual environment:
* Windows:
.\venv\Scripts\activate


* macOS/Linux:
source venv/bin/activate


######################################################## 

# Install Dependencies
Create a requirements.txt file with the following content:
* streamlit
* google-generativeai
* python-dotenv
* requests

Then install the packages:
* pip install -r requirements.txt


######################################################## 

# API Key Configuration
You'll need API keys for Google Generative AI and Google Maps Places API.
1. Google Generative AI API Key:
Go to Google AI Studio or the Google Cloud Console to create an API key for the Gemini models.
Ensure the API key has permissions to use the desired Gemini model (e.g., gemini-1.5-pro-latest, gemini-2.0-flash). You might need to enable the "Vertex AI API" in your Google Cloud project.

2. Google Maps Places API Key:
Go to the Google Cloud Console.
Create a new project or select an existing one.
Enable the "Places API" for your project.
Create an API key and ensure it's restricted appropriately (e.g., to the Places API and your IP address for development).
Create a .env file in the root directory of the project and add your API keys:
GOOGLE_API_KEY="YOUR_GOOGLE_GENERATIVE_AI_API_KEY"
GOOGLE_MAPS_API_KEY="YOUR_GOOGLE_MAPS_PLACES_API_KEY"

Env
* Important: Replace "YOUR_..._API_KEY" with your actual keys. Do not commit your .env file to Git. (It should be covered by the .gitignore file).


######################################################## 

# Run the Application
Once the dependencies are installed and API keys are configured, run the Streamlit app:
streamlit run your_script_name.py

* (Replace your_script_name.py with the actual name of your Python script, e.g., app.py or greenlife_ai.py).


The application should open in your default web browser.


######################################################## 

# 📖 How to Use
1. Open the App: Navigate to the local URL provided by Streamlit (usually http://localhost:8501).
2. Enter Lifestyle Details:
Input your daily commute distance (in km).
Enter your estimated monthly electricity usage (in kWh).
Select your primary diet type.
Provide your city/location (this helps tailor AI suggestions and find local places).
3. Submit: Click the "Submit" button.
4. View Results:
Your estimated monthly carbon footprint will be displayed.
Personalized AI-powered suggestions to reduce your footprint will be generated.
You can explore nearby eco-friendly places by selecting a category and letting the app search.


######################################################## 

# 💡 Future Enhancements (Ideas)
More detailed footprint calculation (e.g., travel modes, waste, water usage).
User accounts to track progress over time.
Gamification or challenges.
Integration with renewable energy providers or carbon offset programs.