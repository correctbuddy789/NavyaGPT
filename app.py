import streamlit as st
import google.generativeai as genai

# Configure page
st.set_page_config(
    page_title="Navya's Resume Assistant",
    layout="wide",
)

# Custom CSS for minimalistic bubble chat design
st.markdown("""
<style>
    /* Clean, minimalistic design */
    body {
        background-color: #f7f7f7;
        color: #333;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    h1 {
        color: #333;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Chat container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* Chat bubbles */
    .msg {
        padding: 0.8rem 1.2rem;
        border-radius: 18px;
        margin-bottom: 0.8rem;
        max-width: 80%;
        word-wrap: break-word;
        line-height: 1.4;
    }
    
    .user-bubble {
        background-color: #e1f5fe;
        color: #01579b;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }
    
    .bot-bubble {
        background-color: #f1f1f1;
        color: #333;
        margin-right: auto;
        border-bottom-left-radius: 4px;
    }
    
    /* Input area */
    .stTextInput>div>div>input {
        border-radius: 20px;
        padding: 0.5rem 1rem;
        border: 1px solid #ddd;
    }
    
    /* Send button */
    .stButton>button {
        border-radius: 20px;
        background-color: #0084ff;
        color: white;
        border: none;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
    }
    
    .stButton>button:hover {
        background-color: #0073e6;
    }
    
    /* Hide empty elements */
    iframe[height="0"] {
        display: none;
    }
    
    /* Footer spacing */
    footer {
        visibility: hidden;
    }
    
    /* Clear chat button */
    .clear-btn {
        color: #666;
        font-size: 0.8rem;
        cursor: pointer;
        text-align: center;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Hardcoded resume data
RESUME = """
NAVYA CHOUDHARI
Bangalore | navyachoudhari2@gmail.com | 08016568-058 | www.linkedin.com/in/navyachoudhari

EDUCATION
CHRIST (deemed to be University), Bangalore		July 2023 - Present
B.A. Economics & Psychology
Relevant Coursework: Microeconomics, Macroeconomics, Econometrics, Statistics, Developmental and Social Psychology

Hopetown Girls' School							2021 - 2023

EXPERIENCE
Grapevine | Bangalore					 April 2025 - Present
Growth Intern
- I supported growth strategy execution across digital channels, driving a 22% increase in user engagement and 15% rise in new user acquisition in 8 weeks.
- I conducted market & competitor research to inform data-driven growth initiatives.

Zomato | Gurgaon					 November 2024
Financial Analyst
- I analyzed revenue trends and operational costs to improve profitability forecasts.
- I assisted in budgeting and financial planning for marketing and expansion.
- I worked with large datasets using Excel & SQL to generate BI reports.
- I collaborated with cross-functional teams on cash flow management strategies.

PROFESSIONAL CERTIFICATIONS
McKinsey Forward Learning Programme		 April 2025
CFA Level I | November Attempt
- Coursework: Derivatives, Economics, Quantitative Analysis, Portfolio Management, Corporate Issuers

SEBI Investor Certification Examination	 March 2025
- Score: 43/50

PROJECTS
- Taxation & Black Money: I applied game theory (Prisoner's Dilemma) to analyze tax evasion and demonetization impacts.
- Venture Capital & Gender Disparities: I researched challenges female entrepreneurs face securing VC, identified biases & proposed solutions.

LEADERSHIP & EXTRACURRICULARS
- Toastmasters International: Active member enhancing public speaking & leadership.
- Winner, DU BizCon: First place at Delhi University Business Fest.
- Student Council Member, CHRIST University.
- Peer Mentor for International Christite Community.

SKILLS
Microsoft Word, Excel, PowerPoint | R | Python | Canva | Jamovi
Communication, Financial & Market Research, Adaptability, Time Management

LANGUAGES
Hindi (Native), English (Fluent), Nepali (Advanced), French (Intermediate)
"""

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

# Main UI with centered elements
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
st.title("Navya's Resume Assistant")

# Display chat messages in bubble style
if st.session_state.history:
    for msg in st.session_state.history:
        if msg['role'] == 'user':
            st.markdown(f"<div class='msg user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='msg bot-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='msg bot-bubble'>Hi there! I'm Navya's resume assistant. Ask me anything about Navya's experience and skills!</div>", unsafe_allow_html=True)

# Input area with send button side by side
col1, col2 = st.columns([5, 1])
with col1:
    query = st.text_input("", placeholder="Type your question here...", label_visibility="collapsed")
with col2:
    send = st.button("Send")

# Configure Gemini
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={"temperature":0.7, "top_p":0.9, "max_output_tokens":512},
    safety_settings=[{"category":"HARM_CATEGORY_HARASSMENT","threshold":"BLOCK_MEDIUM_AND_ABOVE"}]
)

# Process input
if send and query:
    st.session_state.history.append({"role":"user","content":query})
    # system prompt
    sys = f"You are Navya Choudhari. Answer as Navya in first person based solely on this resume: {RESUME}"
    chat = model.start_chat(history=[])
    chat.send_message(sys)
    resp = chat.send_message(query).text
    st.session_state.history.append({"role":"bot","content":resp})
    st.experimental_rerun()  # Rerun to update the UI

# Clear chat option - minimalist design
if st.session_state.history:
    if st.button("Clear Chat", key="clear"):
        st.session_state.history = []
        st.experimental_rerun()

st.markdown("</div>", unsafe_allow_html=True)
