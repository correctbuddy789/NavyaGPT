import os
import streamlit as st
import google.generativeai as genai

# ——— Load API key from Streamlit secrets ———
API_KEY = st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.error("API key not found. Please add GOOGLE_API_KEY to Streamlit secrets.")
    st.stop()
# Configure the GenAI SDK
genai.configure(api_key=API_KEY)

# ——— Streamlit page config ———
st.set_page_config(
    page_title="Navya's Resume Assistant",
    layout="wide",
)

# ——— Custom CSS for bubble chat ———
st.markdown("""
<style>
    body { background-color: #f7f7f7; color: #333; font-family: 'Inter', sans-serif; }
    h1 { color: #333; font-size: 1.8rem; font-weight: 600; margin-bottom: 1rem; }
    .chat-container { max-width: 800px; margin: 0 auto; padding: 1rem; }
    .msg { padding: 0.8rem 1.2rem; border-radius: 18px; margin-bottom: 0.8rem; max-width: 80%; word-wrap: break-word; line-height: 1.4; }
    .user-bubble { background-color: #e1f5fe; color: #01579b; margin-left: auto; border-bottom-right-radius: 4px; }
    .bot-bubble { background-color: #f1f1f1; color: #333; margin-right: auto; border-bottom-left-radius: 4px; }
    .stTextInput>div>div>input { border-radius: 20px; padding: 0.5rem 1rem; border: 1px solid #ddd; }
    .stButton>button { border-radius: 20px; background-color: #0084ff; color: white; border: none; padding: 0.5rem 1.2rem; font-weight: 500; }
    .stButton>button:hover { background-color: #0073e6; }
    iframe[height="0"] { display: none; }
    footer { visibility: hidden; }
    .clear-btn { color: #666; font-size: 0.8rem; cursor: pointer; text-align: center; margin-top: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ——— Hardcoded resume data ———
RESUME = """
NAVYA CHOUDHARI
Bangalore | navyachoudhari2@gmail.com | 08016568-058 | www.linkedin.com/in/navyachoudhari

EDUCATION
CHRIST (deemed to be University), Bangalore        July 2023 - Present
B.A. Economics & Psychology
Relevant Coursework: Microeconomics, Macroeconomics, Econometrics, Statistics, Developmental and Social Psychology

Hopetown Girls' School                            2021 - 2023

EXPERIENCE
Grapevine | Bangalore                     April 2025 - Present
Growth Intern
- I supported growth strategy execution across digital channels, driving a 22% increase in user engagement and 15% rise in new user acquisition in 8 weeks.
- I conducted market & competitor research to inform data-driven growth initiatives.

Zomato | Gurgaon                         November 2024
Financial Analyst
- I analyzed revenue trends and operational costs to improve profitability forecasts.
- I assisted in budgeting and financial planning for marketing and expansion.
- I worked with large datasets using Excel & SQL to generate BI reports.
- I collaborated with cross-functional teams on cash flow management strategies.

PROFESSIONAL CERTIFICATIONS
McKinsey Forward Learning Programme         April 2025
CFA Level I | November Attempt
- Coursework: Derivatives, Economics, Quantitative Analysis, Portfolio Management, Corporate Issuers

SEBI Investor Certification Examination     March 2025
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

# ——— Session state for chat history ———
if 'history' not in st.session_state:
    st.session_state.history = []

# ——— Simple NSFW filter ———
def is_nsfw(text: str) -> bool:
    nsfw_keywords = ["sex", "xxx", "porn", "nsfw"]
    lowered = text.lower()
    return any(k in lowered for k in nsfw_keywords)

# ——— UI Layout ———
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
st.title("Talk to Navya 💬")

# Display history
for msg in st.session_state.history:
    cls = 'user-bubble' if msg['role']=='user' else 'bot-bubble'
    st.markdown(f"<div class='msg {cls}'>{msg['content']}</div>", unsafe_allow_html=True)

# Input area
col1, col2 = st.columns([5,1])
with col1:
    query = st.text_input("", placeholder="Type your question here...", label_visibility="collapsed")
with col2:
    send = st.button("Send")

# Handle send
if send and query:
    st.session_state.history.append({"role":"user","content":query})

    # NSFW check
    if is_nsfw(query):
        resp = "Sorry, I can’t help with that. Let’s talk about my resume or experience!"
    else:
        # System prompt enforces character
        sys_prompt = f"You are Navya Choudhari. Answer as Navya in first person based solely on this resume. If user asks anything off-topic or NSFW, politely decline and bring back to resume. Resume:\n{RESUME}"
        chat = genai.GenerativeModel(model_name="gemini-1.5-flash").start_chat()
        chat.send_message(sys_prompt)
        resp = chat.send_message(query).text

    st.session_state.history.append({"role":"bot","content":resp})
    st.experimental_rerun()

# Clear chat
if st.session_state.history and st.button("Clear Chat", key="clear"):
    st.session_state.history.clear()
    st.experimental_rerun()

# Footer
st.markdown("<div style='text-align: center; margin-top: 20px; color: #777; font-size: 0.8rem;'>Built by Navya</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
