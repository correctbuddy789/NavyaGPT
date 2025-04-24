import streamlit as st
import google.generativeai as genai

# Configure page
st.set_page_config(
    page_title="Navya's Resume Assistant",
    layout="wide",
)

# Custom CSS for clean aesthetics with accent
st.markdown("""
<style>
    body, .main {
        background-color: #fafafa;
        color: #111;
        font-family: 'Segoe UI', Tahoma, sans-serif;
    }
    .stApp {
        padding: 2rem;
    }
    h1 {
        color: #0b3d91;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .description {
        margin-bottom: 1.5rem;
        font-size: 1.1rem;
        color: #333;
    }
    .stButton>button {
        background-color: #0b3d91;
        color: #fff;
        border-radius: 0.4rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #093076;
    }
    .chat-box {
        border: 1px solid #ddd;
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff;
        max-height: 60vh;
        overflow-y: auto;
    }
    .user-msg {
        text-align: right;
        margin: 0.5rem 0;
    }
    .bot-msg {
        text-align: left;
        margin: 0.5rem 0;
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

Hopetown Girls’ School							2021 - 2023

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
- Taxation & Black Money: I applied game theory (Prisoner’s Dilemma) to analyze tax evasion and demonetization impacts.
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

# Sidebar with brief bio
with st.sidebar:
    st.header("About Navya")
    st.write("I'm Navya Choudhari, a growth intern and financial analyst with a passion for data-driven impact. Ask me about my background!")
    st.markdown("---")

# Main UI
st.title("👩‍💼 Navya's Resume Assistant")
st.markdown("<div class=\"description\">Chat with me to explore my qualifications, experience, projects, and skills. I’ll answer in first person!</div>", unsafe_allow_html=True)

# Configure Gemini
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={"temperature":0.7, "top_p":0.9, "max_output_tokens":512},
    safety_settings=[{"category":"HARM_CATEGORY_HARASSMENT","threshold":"BLOCK_MEDIUM_AND_ABOVE"}]
)

# Input and chat
col1, col2 = st.columns([5,1])
with col1:
    query = st.text_input("Your question:")
with col2:
    send = st.button("Send")

if send and query:
    st.session_state.history.append({"role":"user","content":query})
    # system prompt
    sys = f"You are Navya Choudharii. Answer as Navya in first person based solely on this resume: {RESUME}"
    chat = model.start_chat(history=[])
    chat.send_message(sys)
    resp = chat.send_message(query).text
    st.session_state.history.append({"role":"bot","content":resp})

# Display chat
st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
for msg in st.session_state.history:
    if msg['role']=='user':
        st.markdown(f"<div class='user-msg'><strong>You:</strong> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'><strong>Navya:</strong> {msg['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Clear chat option
if st.button("Clear Chat"):
    st.session_state.history = []
