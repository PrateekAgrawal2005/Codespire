# app.py

import os
import streamlit as st

# Try import genai client
try:
    from google import genai
except Exception as e:
    st.error("Missing google-genai package. Install with: pip install google-genai")
    raise

# Page setup
st.set_page_config(page_title="Mini AI Helper", page_icon="🤖")
st.title("Mini AI Helper ✨")
st.write("Practice app: Ask Gemini something (roadmap, study plan, project ideas).")

# Read API key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("GEMINI_API_KEY not set. In terminal: set GEMINI_API_KEY=your_key_here")
    st.stop()

# Initialize client
client = genai.Client(api_key=API_KEY)

# Inputs
name = st.text_input("Your name (optional)")
branch = st.text_input("Branch (e.g., AIML, CSE)")
goal = st.selectbox("Goal", ["Internship", "Job", "Learn Basics", "Project"])
skills = st.text_input("Current skills (comma separated)")

user_prompt = st.text_area(
    "Or type a direct question (example: 'Make a 3-day study plan for Python beginners')",
    height=120
)

# Generate button
if st.button("Generate"):
    # Build custom prompt
    if not user_prompt.strip():
        prompt = f"Create a 7-day study plan and 3 project ideas for a {branch} student whose goal is {goal}. Current skills: {skills}."
    else:
        prompt = user_prompt

    with st.spinner("Generating..."):
        try:
            # ---- FIXED MODEL CALL ----
            response = client.models.generate_content(
                model="gemini-2.0-flash",   # BEST MODEL
                contents=prompt
            )

            text = response.text

            st.success("AI Response:")
            st.text_area("Response", value=text, height=320)

        except Exception as e:
            st.error("Error calling Gemini API. See details below:")
            st.exception(e)