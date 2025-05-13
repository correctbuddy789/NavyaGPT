import os
import streamlit as st
import google.generativeai as genai

# ——— Load API key ———
API_KEY = st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.error("API key not found. Please add GOOGLE_API_KEY to Streamlit secrets.")
    st.stop()

genai.configure(api_key=API_KEY)

# ——— Streamlit Config ———
st.set_page_config(page_title="Navya's Resume Assistant", layout="wide")

# ——— Custom CSS ———
st.markdown("""
<style>
body { background-color: #f7f7f7; font-family: 'Inter', sans-serif; }
.chat-container { max-width: 800px; margin: auto; padding: 1rem; }
.msg { padding: 0.8rem 1.2rem; border-radius: 18px; margin-bottom: 0.8rem; max-width: 80%; word-wrap: break-word; }
.user-bubble { background-color: #e1f5fe; color: #01579b; margin-left: auto; border-bottom-right-radius: 4px; }
.bot-bubble { background-color: #f1f1f1; color: #333; margin-right: auto; border-bottom-left-radius: 4px; }
.stTextInput>div>div>input { border-radius: 20px; padding: 0.5rem 1rem; border: 1px solid #ddd; }
.stButton>button { border-radius: 20px; background-color: #0084ff; color: white; border: none; padding: 0.5rem 1.2rem; font-weight: 500; }
.stButton>button:hover { background-color: #0073e6; }
footer, iframe[height="0"] { display: none; visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ——— Resume Content ———
RESUME = """
NAVYA CHOUDHARI  
Bangalore | navyachoudhari2@gmail.com | 08016568-058 | www.linkedin.com/in/navyachoudhari  

EDUCATION  
CHRIST (Deemed to be University), Bangalore — B.A. Economics & Psychology  
July 2023 - Present  
Relevant Coursework: Microeconomics, Macroeconomics, Econometrics, Statistics, Developmental and Social Psychology  

Hopetown Girls' School  
2021 - 2023  

EXPERIENCE  
**Grapevine | Bangalore** — Growth Intern  
April 2025 - Present  
• Supported growth strategy execution across digital channels, driving a 22% increase in user engagement and 15% rise in new user acquisition in 8 weeks.  
• Conducted market & competitor research to inform data-driven growth initiatives.  

**NIMHANS | Dept. of Mental Health Education** — Internship  
May 2024  
• Contributed to research projects by conducting literature reviews, assisting in data collection, and supporting the analysis of mental health education interventions.  
• Developed educational materials and awareness content aimed at reducing stigma and improving mental health literacy.  
• Participated in community engagement, workshops, and public policy discussions.  

PROFESSIONAL CERTIFICATIONS  
• McKinsey Forward Learning Programme – April 2025  
• CFA Level I (November Attempt) – Coursework: Derivatives, Economics, Quantitative Analysis, Portfolio Management, Corporate Issuers  
• SEBI Investor Certification – March 2025 | Score: 43/50  

PROJECTS  
• Taxation & Black Money – Applied game theory (Prisoner's Dilemma) to analyze tax evasion and demonetization impacts.  
• Venture Capital & Gender Disparities – Researched funding gaps for female founders, identified biases, and proposed solutions.  

LEADERSHIP & EXTRACURRICULARS  
• Toastmasters International – Public speaking and leadership development  
• Student Council Member, CHRIST University  
• Peer Mentor for International Christite Community  

SKILLS  
Microsoft Word, Excel, PowerPoint | R | Python | Canva | Jamovi  
Communication | Financial & Market Research | Adaptability | Time Management  

LANGUAGES  
Hindi (Native), English (Fluent), Nepali (Advanced), French (Intermediate)
"""

# ——— Chat Session State ———
if 'history' not in st.session_state:
    st.session_state.history = []

if 'chat' not in st.session_state:
    st.session_state.chat = genai.GenerativeModel("gemini-1.5-flash").start_chat()
    st.session_state.chat.send_message(
        f"You are Navya Choudhari. Respond in first person based only on this resume:\n{RESUME}\n"
        "If the user asks anything irrelevant or NSFW, politely decline and redirect to the resume."
    )

# ——— NSFW Filter ———
def is_nsfw(text):
    nsfw_keywords = {"sex", "porn", "nude", "xxx", "nsfw", "onlyfans", "explicit"}
    return any(word in text.lower() for word in nsfw_keywords)

# ——— Chat Interface ———
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
st.title("Talk to Navya 💬")

# Show history
for msg in st.session_state.history:
    cls = 'user-bubble' if msg['role'] == 'user' else 'bot-bubble'
    st.markdown(f"<div class='msg {cls}'>{msg['content']}</div>", unsafe_allow_html=True)

# Input box
col1, col2 = st.columns([5, 1])
with col1:
    query = st.text_input("", placeholder="Type your question here...", label_visibility="collapsed")
with col2:
    send = st.button("Send")

# Handle query
if send and query:
    st.session_state.history.append({"role": "user", "content": query})

    if is_nsfw(query):
        response = "Sorry, I can’t help with that. Let’s talk about my resume or experience!"
    else:
        try:
            response = st.session_state.chat.send_message(query).text
        except Exception as e:
            response = f"Oops! Something went wrong: {e}"

    st.session_state.history.append({"role": "bot", "content": response})
    st.experimental_rerun()

# Clear chat button
if st.session_state.history and st.button("Clear Chat"):
    st.session_state.history.clear()
    del st.session_state.chat
    st.experimental_rerun()

# Footer
st.markdown(
    "<div style='text-align: center; margin-top: 20px; color: #777; font-size: 0.8rem;'>Built by Navya</div>",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)
