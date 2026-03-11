import os
import streamlit as st
from datetime import datetime
import json
import textwrap
from dotenv import load_dotenv
load_dotenv(override=True)

# Session state initialization
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
if "prompt_value" not in st.session_state:
    st.session_state.prompt_value = ""

# Try import genai client
try:
    from google import genai
    from google.genai import types
except Exception:
    st.error("Missing google-genai package. Install with: pip install google-genai")
    raise

# ------------------------------------
# PAGE CONFIG - PREMIUM THEME
# ------------------------------------
st.set_page_config(
    page_title="Mini AI Helper",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
* {
    color-scheme: dark;
}
.main {
    background: linear-gradient(135deg, #0a0e27 0%, #1a0e3f 50%, #0a0e27 100%);
}
body {
    background-color: #0a0e27;
}
/* FORCE ALL TEXT TO LIGHT COLOR */
.stMarkdown, .stText, p, span, div, h1, h2, h3, h4, h5, h6, label, .stTextInput label {
    color: #ffffff !important;
}
/* Header with stunning gradient */
.header-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
    padding: 50px;
    border-radius: 20px;
    margin-bottom: 40px;
    text-align: center;
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
    border: 2px solid rgba(255, 255, 255, 0.1);
}
.header-container h1 {
    color: #ffffff;
    font-size: 3.2em;
    margin-bottom: 15px;
    text-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    font-weight: 900;
    letter-spacing: 1px;
}
.header-container p {
    color: #f0f4ff;
    font-size: 1.25em;
    font-weight: 600;
    margin: 8px 0;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}
/* Premium buttons */
.stButton>button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: #ffffff !important;
    border: 2px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 12px;
    padding: 16px 32px !important;
    font-weight: 800 !important;
    font-size: 1.1em !important;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    text-transform: uppercase;
    letter-spacing: 1px;
}
.stButton>button:hover {
    transform: translateY(-4px);
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
}
/* Input fields with high contrast */
.stTextInput>div>div>input, 
.stTextArea>div>div>textarea, 
.stSelectbox>div>div>select,
input[type="text"],
textarea,
select {
    background-color: #1a1f3f !important;
    color: #ffffff !important;
    border: 2px solid #667eea !important;
    border-radius: 12px;
    padding: 14px 18px !important;
    font-size: 1.05em !important;
    font-weight: 500;
    transition: all 0.3s ease;
}
.stTextInput>div>div>input::placeholder, 
.stTextArea>div>div>textarea::placeholder {
    color: #a0aec0 !important;
}
.stTextInput>div>div>input:focus, 
.stTextArea>div>div>textarea:focus,
input[type="text"]:focus,
textarea:focus {
    border-color: #f093fb !important;
    box-shadow: 0 0 20px rgba(240, 147, 251, 0.5) !important;
    background-color: #202847 !important;
}
/* Info card - High visibility */
.info-card {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(240, 147, 251, 0.15) 100%);
    border-left: 6px solid #667eea;
    border-radius: 14px;
    padding: 20px;
    margin: 20px 0;
    color: #ffffff;
    font-weight: 500;
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
}
.info-card strong {
    color: #f0f4ff;
    font-size: 1.1em;
}
/* Success card */
.success-card {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(74, 222, 128, 0.15) 100%);
    border-left: 6px solid #22c55e;
    padding: 20px;
    border-radius: 14px;
    margin: 20px 0;
    color: #e8f5e9;
    font-weight: 600;
    box-shadow: 0 8px 20px rgba(34, 197, 94, 0.2);
}
/* Warning card */
.warning-card {
    background: linear-gradient(135deg, rgba(251, 146, 60, 0.15) 0%, rgba(253, 126, 20, 0.15) 100%);
    border-left: 6px solid #fb923c;
    padding: 20px;
    border-radius: 14px;
    margin: 20px 0;
    color: #fff7ed;
    font-weight: 600;
    box-shadow: 0 8px 20px rgba(251, 146, 60, 0.2);
}
/* Output container - Premium styling */
.output-container {
    background: linear-gradient(135deg, rgba(26, 31, 63, 0.9) 0%, rgba(15, 20, 45, 0.9) 100%);
    border: 2px solid #667eea;
    border-radius: 18px;
    padding: 35px;
    margin-top: 35px;
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
    color: #ffffff;
}
.output-container h3 {
    color: #87ceeb;
    font-size: 1.6em;
    margin-bottom: 20px;
    font-weight: 800;
}
.output-container p, 
.output-container li {
    color: #e8eef7;
    font-size: 1.05em;
    line-height: 1.8;
}
/* Sidebar header */
.sidebar-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    margin-bottom: 30px;
    color: #ffffff;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    border: 2px solid rgba(255, 255, 255, 0.1);
}
.sidebar-header h2 {
    margin: 0;
    font-size: 1.6em;
    font-weight: 800;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}
/* Section headers */
.section-header {
    color: #87ceeb;
    font-size: 1.5em;
    font-weight: 800;
    margin-top: 30px;
    margin-bottom: 20px;
    border-bottom: 3px solid #667eea;
    padding-bottom: 12px;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
/* Feature card */
.feature-card {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(240, 147, 251, 0.2) 100%);
    border: 2px solid #667eea;
    padding: 18px;
    border-radius: 12px;
    margin: 15px 0;
    color: #ffffff;
    font-weight: 600;
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
}
.feature-card strong {
    color: #87ceeb;
    font-size: 1.1em;
}
.feature-card ul {
    color: #e8eef7;
    margin: 12px 0;
}
.feature-card li {
    margin: 6px 0;
    color: #e8eef7;
}
/* Footer */
.footer-text {
    text-align: center;
    color: #cbd5e1;
    font-size: 1em;
    margin-top: 40px;
    padding-top: 25px;
    border-top: 2px solid #667eea;
    font-weight: 600;
}
/* Slider styling */
.stSlider {
    color: #ffffff;
}
.stSlider p {
    color: #ffffff !important;
    font-weight: 600;
}
/* Select box */
.stSelectbox label,
.stSlider label {
    color: #ffffff !important;
    font-weight: 700;
    font-size: 1.05em;
}
.stInfo {
    background-color: rgba(102, 126, 234, 0.15) !important;
    color: #ffffff !important;
    border-color: #667eea !important;
}
.stWarning {
    background-color: rgba(251, 146, 60, 0.15) !important;
    color: #fff7ed !important;
    border-color: #fb923c !important;
}
.stSuccess {
    background-color: rgba(34, 197, 94, 0.15) !important;
    color: #e8f5e9 !important;
    border-color: #22c55e !important;
}
.stError {
    background-color: rgba(239, 68, 68, 0.15) !important;
    color: #fee2e2 !important;
    border-color: #ef4444 !important;
}
[data-testid="column"] {
    padding: 10px;
}
.stSpinner {
    color: #667eea;
}
hr {
    border-color: #475569 !important;
    margin: 30px 0;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------
# HEADER SECTION
# ------------------------------------
st.markdown("""
<div class="header-container">
    <h1>🤖 MINI AI HELPER</h1>
    <p>✨ Your Intelligent Learning & Problem-Solving Assistant</p>
    <p style="font-size: 0.95em; margin-top: 8px;">Powered by Google Gemini 2.5 Flash</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
<strong>🎯 Welcome!</strong> Get personalized study plans, coding help, career guidance, project ideas, interview prep, and instant answers to any question!
</div>
""", unsafe_allow_html=True)

# ------------------------------------
# SIDEBAR CONFIGURATION
# ------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-header"><h2>⚙️ SETTINGS</h2></div>', unsafe_allow_html=True)
    
    st.markdown("### 🎨 Customization")
    
    # Theme selector
    theme = st.selectbox("Theme", ["Dark (Recommended)", "Light"])
    
    # AI Model selector
    model_choice = st.selectbox(
        "AI Model",
        ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-2.5-pro"],
        help="⚡ 2.5 Flash: Recommended | ⚡ 2.0 Flash: Fast | ⚡ 2.0 Flash Lite: Light | 🧠 2.5 Pro: Most capable"
    )
    
    # Response length
    response_length = st.slider(
        "Response Length",
        1, 5, 3,
        help="1=Brief | 3=Balanced | 5=Comprehensive"
    )
    
    # Temperature
    temperature = st.slider(
        "Creativity Level",
        0.0, 1.0, 0.7,
        help="0.0=Factual | 0.7=Balanced | 1.0=Creative"
    )
    
    st.markdown("---")
    
    st.markdown('<div class="section-header">📋 System Prompt</div>', unsafe_allow_html=True)
    
    default_prompt = """You are an expert AI mentor and educator with deep knowledge in technology, coding, career development, and academics. You are enthusiastic, engaging, and love explaining things in a way that truly helps people understand and grow.

**YOUR PERSONALITY:**
🎯 Passionate teacher who makes complex things simple and exciting
💡 Always gives rich, detailed, thorough answers — never one-liners
🚀 Motivating and encouraging — you believe in the user's potential
🔍 Curious and thorough — you cover all angles of a topic

**RESPONSE STYLE — ALWAYS DO THIS:**
✅ Write LONG, DETAILED, THOROUGH responses — the more detail the better
✅ Use clear ## headings and ### subheadings to organize content
✅ Use bullet points, numbered lists, tables where helpful
✅ Include REAL-WORLD EXAMPLES, analogies, and stories to explain concepts
✅ Add code snippets with explanations whenever relevant
✅ End EVERY response with: 🔥 Key Takeaways, ⭐ Next Steps, and 💬 Follow-up Questions the user can ask
✅ Use emojis to make responses engaging and easy to scan
✅ Bold **important terms** and highlight key concepts
✅ If explaining a roadmap or plan — give it DAY BY DAY or WEEK BY WEEK with specifics
✅ If explaining code — explain WHAT it does, WHY it works, and HOW to customize it

**NEVER DO:**
❌ Give short, vague, one-paragraph answers
❌ Say "it depends" without explaining the options
❌ Skip examples or just list theory without practical application"""
    
    SYSTEM_PROMPT = st.text_area(
        "Custom Instructions:",
        value=default_prompt,
        height=180,
        help="Edit to customize AI behavior"
    )
    
    st.markdown("---")
    st.markdown("""
    <div class="feature-card">
    <strong>💡 Pro Tips for Better Responses:</strong>
    <ul>
    <li>Be specific and detailed in your questions</li>
    <li>Mention your current skill level</li>
    <li>Ask for step-by-step breakdowns</li>
    <li>Request code examples when needed</li>
    <li>Ask follow-up questions for clarity</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------
# API KEY VALIDATION
# ------------------------------------
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("""
    ❌ **GEMINI_API_KEY not configured!**
    
    **Quick Setup (5 minutes):**
    
    1. Get your free API key: https://aistudio.google.com/app/apikey
    2. Set environment variable:
       - **Windows**: `set GEMINI_API_KEY=your_key_here`
       - **Mac/Linux**: `export GEMINI_API_KEY=your_key_here`
    3. Restart the app: `streamlit run app.py`
    """)
    st.stop()

# Initialize Gemini client
try:
    client = genai.Client(api_key=API_KEY)
    st.sidebar.success("✅ API Connected Successfully!")
except Exception as e:
    st.error(f"❌ API Connection Error: {str(e)}")
    st.stop()

# ------------------------------------
# QUICK TEMPLATES
# ------------------------------------
st.markdown('<div class="section-header">⚡ QUICK START TEMPLATES</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📚 Study Plan", use_container_width=True):
        st.session_state.prompt_value = "Create a detailed 30-day learning roadmap for [TOPIC] starting from [YOUR_LEVEL]. Include daily schedule, resources, projects, and milestones."
        st.session_state.input_key += 1

with col2:
    if st.button("💼 Career Guide", use_container_width=True):
        st.session_state.prompt_value = "What are the best steps to become a [JOB_ROLE]? Provide required skills, learning path, timeline, salary expectations, and job search tips."
        st.session_state.input_key += 1

with col3:
    if st.button("🐛 Debug Help", use_container_width=True):
        st.session_state.prompt_value = "I'm getting this error in my [LANGUAGE] code: [ERROR_MESSAGE]. Here's my code: [PASTE_CODE]. How do I fix it step-by-step?"
        st.session_state.input_key += 1

# ------------------------------------
# USER INPUT SECTION
# ------------------------------------
st.markdown('<div class="section-header">📝 YOUR INFORMATION</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    name = st.text_input(
        "👤 Your Name (optional)",
        placeholder="e.g., Sarah",
        label_visibility="collapsed"
    )
    st.markdown("<p style='color: #a0aec0; font-size: 0.9em; margin-top: -20px;'>Your Name (optional)</p>", unsafe_allow_html=True)
    
    branch = st.text_input(
        "🎓 Your Branch/Field (optional)",
        placeholder="e.g., AIML, Frontend, Data Science",
        label_visibility="collapsed"
    )
    st.markdown("<p style='color: #a0aec0; font-size: 0.9em; margin-top: -20px;'>Your Branch/Field</p>", unsafe_allow_html=True)

with col2:
    goal = st.selectbox(
        "🎯 Your Goal",
        [
            "Learn Something New",
            "Internship Preparation",
            "Job Interview Prep",
            "Project Development",
            "Problem Solving",
            "Career Guidance",
            "Skill Enhancement"
        ]
    )
    
    skills = st.text_input(
        "💼 Your Skills (comma separated)",
        placeholder="e.g., Python, React, SQL, Problem-Solving",
        label_visibility="collapsed"
    )
    st.markdown("<p style='color: #a0aec0; font-size: 0.9em; margin-top: -20px;'>Your Skills</p>", unsafe_allow_html=True)

st.markdown("---")

# Main question input
st.markdown('<div class="section-header">❓ WHAT DO YOU NEED HELP WITH?</div>', unsafe_allow_html=True)

user_prompt = st.text_area(
    "Question",
    value=st.session_state.prompt_value,
    height=160,
    placeholder="Type your question, topic, or request here...\nExample: 'How to learn Python in 2 weeks?' or 'Debug my code'",
    label_visibility="collapsed",
    key=f"user_prompt_{st.session_state.input_key}"
)

# ------------------------------------
# ACTION BUTTONS
# ------------------------------------
st.markdown("---")
col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

with col_btn1:
    generate_btn = st.button("✨ GENERATE", use_container_width=True, type="primary")

with col_btn2:
    clear_btn = st.button("🔄 CLEAR", use_container_width=True)

with col_btn3:
    example_btn = st.button("📖 EXAMPLES", use_container_width=True)

with col_btn4:
    help_btn = st.button("❓ HELP", use_container_width=True)

# Handle buttons
if clear_btn:
    st.session_state.response = None
    st.session_state.prompt_value = ""
    st.session_state.input_key += 1
    st.rerun()

if example_btn:
    st.info("""
    **EXAMPLE QUESTIONS:**
    
    📚 **Learning**: "I want to learn web development. I know HTML/CSS but not JavaScript. Create a detailed 60-day roadmap with resources."
    
    💼 **Career**: "I have 3 years Python experience. How do I transition to machine learning engineering?"
    
    🐛 **Coding**: "My React component keeps re-rendering unnecessarily. Here's the code: [CODE]. What's wrong?"
    
    📊 **Projects**: "Give me 5 beginner-to-intermediate project ideas to learn data science"
    
    🔧 **Tools**: "What's the difference between TypeScript and JavaScript? When should I use each?"
    """)

if help_btn:
    st.info("""
    **HOW TO USE MINI AI HELPER:**
    
    **1️⃣ FILL YOUR PROFILE** (optional but recommended)
       - Name, field, goals, and skills help AI personalize responses
       - More context = Better answers
    
    **2️⃣ ASK YOUR QUESTION**
       - Be specific and detailed
       - Include error messages or code snippets
       - Mention what you've already tried
       - Ask for step-by-step explanations
    
    **3️⃣ CLICK GENERATE**
       - AI processes your request
       - Adjust response length in settings for more/less detail
    
    **4️⃣ COPY & SAVE**
       - Save responses for reference
       - Try follow-up questions
       - Ask for clarifications
    
    **💡 TIPS FOR BEST RESULTS:**
    - Specific questions → Specific answers
    - Include your experience level
    - Ask for step-by-step breakdowns
    - Request code examples or diagrams
    - Be clear about what you're trying to achieve
    """)        

# Helper: map response length to max tokens
def map_length_to_tokens(level: int) -> int:
    return {1: 500, 2: 1000, 3: 2000, 4: 3500, 5: 6000}.get(level, 2000)

# ------------------------------------
# MAIN GENERATION LOGIC
# ------------------------------------
if generate_btn:
    if not user_prompt.strip():
        st.markdown("""
        <div class="warning-card">
        <strong>⚠️ PLEASE ENTER A QUESTION!</strong> What would you like help with?
        </div>
        """, unsafe_allow_html=True)
    else:
        # Build comprehensive prompt
        response_instruction = {
            1: "Write a focused response (400-600 words) covering the key points with at least 1 example.",
            2: "Write a solid response (700-1000 words) with examples, explanations, and a next steps section.",
            3: "Write a detailed, well-structured response (1000-1500 words) with sections, examples, code if relevant, and actionable advice.",
            4: "Write a COMPREHENSIVE, in-depth response (1500-2500 words). Cover all aspects, include multiple examples, pros/cons, tips, and a full action plan.",
            5: "Write an EXHAUSTIVE, expert-level deep dive (2500+ words). This should feel like reading a complete guide or tutorial — cover everything from basics to advanced, with examples, code, comparisons, pitfalls, best practices, resources, and a step-by-step action plan."
        }
        
        user_context = f"""**USER CONTEXT:**
- Name: {name if name else 'Not provided'}
- Field: {branch if branch else 'Not specified'}
- Goal: {goal}
- Skills: {skills if skills else 'Not specified'}
- Response Length: Level {response_length}/5 ({response_instruction[response_length]})"""
        
        final_prompt = f"""{SYSTEM_PROMPT}

{user_context}

---

**USER'S QUESTION/REQUEST:**
{user_prompt}

---

**IMPORTANT:** {response_instruction[response_length]}

Please format your response with:
- Clear headings for sections
- Bullet points for lists
- Code blocks for code snippets (if applicable)
- Bold text for important concepts
- Step-by-step instructions when appropriate"""
        
        with st.spinner("🔄 Generating your personalized response..."):
            try:
                # --- CORRECTED: use types.GenerateContentConfig via `config` ---
                max_tokens = map_length_to_tokens(response_length)
                response = client.models.generate_content(
                    model=model_choice,
                    contents=final_prompt,
                    config=types.GenerateContentConfig(
                        temperature=float(temperature),
                        top_p=0.95,
                        max_output_tokens=int(max_tokens)
                    )
                )
                
                output = response.text or ""
                if not output.strip():
                    st.warning("⚠️ The AI returned an empty response. Try rephrasing your question.")
                    st.stop()
                
                # Display success message
                st.markdown("""
                <div class="success-card">
                <strong>✅ RESPONSE GENERATED SUCCESSFULLY!</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Display output in beautiful container
                st.markdown('<div class="output-container">', unsafe_allow_html=True)
                st.markdown("### 🧠 AI Response")
                st.markdown(output)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Additional actions
                col_action1, col_action2 = st.columns(2)
                
                with col_action1:
                    st.success("💡 **TIP:** Copy this response and save it for later reference!")
                
                with col_action2:
                    st.info("✨ **Want more?** Ask a follow-up question above!")
                
                st.session_state.response = output
                
            except Exception as e:
                st.error(f"❌ Error generating response: {str(e)}")
                st.warning("""
                **TROUBLESHOOTING:**
                - Verify your API key is correct
                - Check your internet connection
                - Try a simpler question first
                - Ensure you have API credits remaining
                """)

# ------------------------------------
# FOOTER
# ------------------------------------
st.markdown("""
<div class="footer-text">
<strong>🚀 Mini AI Helper</strong> • Powered by Google Gemini API<br>
🔐 Your questions and data are not stored • ⚡ Fast, Accurate, Always Learning<br>
Made with ❤️ for Students & Professionals Worldwide
</div>
""", unsafe_allow_html=True)

