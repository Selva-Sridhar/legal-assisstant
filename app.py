import streamlit as st
import json
import os
import speech_recognition as sr
from utils import search_cases

# Get absolute path of the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load legal case data with absolute paths
def load_cases():
    case_files = {
        "civil": os.path.join(BASE_DIR, "cases", "civil_cases.json"),
        "criminal": os.path.join(BASE_DIR, "cases", "criminal_cases.json"),
        "family": os.path.join(BASE_DIR, "cases", "family_cases.json"),
    }

    cases = {}
    for category, file_path in case_files.items():
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                cases[category] = json.load(f)
        else:
            cases[category] = []
            print(f"Warning: {file_path} not found. Using an empty list.")

    return cases["civil"], cases["criminal"], cases["family"]

# Load cases into memory
civil_cases, criminal_cases, family_cases = load_cases()

# Sidebar navigation
st.sidebar.title("Opti-Legal")
page = st.sidebar.radio("Menu", ["Home", "User Profile", "Pending Cases"])  # Home page, Profile, Pending Cases

# ------------------ HOME PAGE ------------------
if page == "Home":
    st.title("Opti-Legal")
    st.write("Describe your legal situation below, and we’ll help you find relevant cases.")

    # Option to enter situation via text or voice
    input_method = st.radio("How would you like to describe your situation?", ("Text Input", "Voice Recognition"))

    user_input = ""

    if input_method == "Text Input":
        user_input = st.text_area("Enter your situation:", "")

    else:
        st.write("Click the icon below to start voice recognition:")
        record_button = st.button("🎤 Start Recording")

        if record_button:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                st.write("Listening... Please speak clearly.")
                try:
                    audio = recognizer.listen(source, timeout=5)
                    user_input = recognizer.recognize_google(audio)
                    st.write(f"Recognized Text: {user_input}")
                except sr.UnknownValueError:
                    st.write("Could not understand the audio.")
                except sr.RequestError:
                    st.write("Could not connect to the voice recognition service.")

    # Check if input is provided and process it
    if st.button("Submit"):
        if user_input:
            # Determine the case category based on the input
            if "divorce" in user_input.lower() or "property" in user_input.lower():
                case_category = "family"
            elif "crime" in user_input.lower() or "assault" in user_input.lower():
                case_category = "criminal"
            else:
                case_category = "civil"
            
            # Based on the determined case category, navigate to the appropriate page
            if case_category == "civil":
                case_results = search_cases(user_input, civil_cases, criminal_cases, family_cases)
                st.subheader("Civil Case Results:")
                for case in case_results["civil"]:
                    st.write(f"- {case}")
            elif case_category == "criminal":
                case_results = search_cases(user_input, civil_cases, criminal_cases, family_cases)
                st.subheader("Criminal Case Results:")
                for case in case_results["criminal"]:
                    st.write(f"- {case}")
            elif case_category == "family":
                case_results = search_cases(user_input, civil_cases, criminal_cases, family_cases)
                st.subheader("Family Case Results:")
                for case in case_results["family"]:
                    st.write(f"- {case}")
        else:
            st.warning("Please enter or say a situation before submitting.")

# ------------------ USER PROFILE PAGE ------------------
elif page == "User Profile":
    st.title("User Profile")
    st.write("### Name: John Doe")
    st.write("### Email: johndoe@example.com")
    st.write("### Phone: +1 234 567 8901")
    st.write("### Address: 123 Legal Street, Lawtown, USA")

# ------------------ PENDING CASES PAGE ------------------
elif page == "Pending Cases":
    st.title("Pending Cases")
    st.write("No pending cases.")
