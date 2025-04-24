import streamlit as st
import google.generativeai as genai
import pandas as pd
import os
from PIL import Image
import io

# Configure page
st.set_page_config(
    page_title="Resume AI Assistant",
    page_icon="👩‍💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a more attractive interface with improved text visibility
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
        color: #000000;
    }
    .chat-message.bot {
        background-color: #f3f4f6;
        border-left: 5px solid #11567f;
        color: #000000;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1rem;
    }
    .chat-message .message {
        flex-grow: 1;
    }
    .stButton>button {
        background-color: #11567f;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0d4b6f;
    }
    h1, h2, h3 {
        color: #11567f;
    }
    .highlight {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #2196f3;
        color: #000000;
    }
    .footer {
        text-align: center;
        margin-top: 20px;
        font-size: 14px;
        color: #555555;
    }
    .sidebar-content {
        color: #333333;
    }
    .sample-questions {
        background-color: #f0f2f5;
        padding: 10px;
        border-radius: 5px;
        color: #333333;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = """
NAVYA CHOUDHARI 
Bangalore| navyachoudhari2@gmail.com |08016568-058|www.linkedin.com/in/navyachoudhari 

EDUCATION 
CHRIST(deemed to be University),Bangalore                                                          July 2023-Present 
B.A Economics & Psychology                                   
Relevant Coursework: Microeconomics,Macroeconomics,Econometrics,Statistics,Developmental and 
Social Psychology  
                                                                                                    
Hopetown Girls' School                                                                              2021-2023

EXPERIENCE                                                                                    
Grapevine| Bangalore                                                                              April 2025-Present 
Growth Intern
●	Supported Growth strategy execution across digital channels, contributing to a 22% increase in user engagement and a 15% rise in new user acquisition over the first 8 weeks.
●	Conducted market and competitor research to inform data-driven growth initiatives and improve targeting strategies.

Zomato| Gurgaon                                                                                    November 2024 
Financial Analyst                                                        
●	Analyzed revenue trends and operational costs, contributing to improved profitability forecasts. 
●	Assisted in budgeting and financial planning for marketing and expansion projects. 
●	Worked with large datasets using Excel and SQL to generate business intelligence reports. 
●	Collaborated with cross-functional teams to improve cash flow management strategies. 

PROFESSIONAL COURSES AND CERTIFICATION 
Mckinsey Forward Learning Programme                                                                 April 2025 
Chartered Financial Analyst (CFA Level-1)|November Attempt 
●	Relevant Coursework: Derivatives, Economics, Quantitative Analysis, Portfolio Management, Corporate Issuers 

SEBI-Investor Certification Examination                                                             March 2025 
●	Grade:43/50 

PROJECTS 
●	Taxation & Black Money: Applied game theory (Prisoner's Dilemma) to analyze tax evasion behavior and the impact of demonetization on compliance in the informal economy. 
●	Venture Capital & Gender Disparities: Researched challenges faced by female entrepreneurs in securing venture capital, identifying key investor biases and proposing strategic solutions 

LEADERSHIP AND EXTRACURRICULARS 
●	Toastmasters International: Active member, honing public speaking, leadership, and communication skills.  
●	Winner – Delhi University Business Fest (DU BizCon): Secured first place in DU BizCon, one of Delhi's premier business case competitions 
●	Student Council Member at University
●	Peer Mentor for International Christite Community 

SKILLS 
Microsoft Suite(Word, Excel, PowerPoint), R programming, Python, Canva, Jamovi 
Communication Skills–Verbal and Written, Financial and market research, Adaptability and Time management 

LANGUAGES
●	Native speaker in: Hindi
●	Fluency in: English
●	Advanced proficiency in: Nepali
●	Intermediate in: French
"""

# Function to configure Gemini API
def configure_gemini():
    api_key = st.secrets.get("GEMINI_API_KEY", "AIzaSyBK6O55ONxwniYoNSunXgLjL92p2AL5A5A")
    genai.configure(api_key=api_key)
    
    # Configure the model
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 1024,
    }
    
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    
    return model

# Function to get AI response
def get_gemini_response(model, prompt, resume_data):
    system_prompt = f"""
    You are an AI assistant specifically designed to help recruiters understand Navya Choudhari's resume.
    You have detailed knowledge of the following resume and can answer any questions about Navya's 
    qualifications, skills, experience, and education.
    
    RESUME DATA:
    {resume_data}
    
    Guidelines:
    1. Provide clear, concise information about Navya's qualifications
    2. If asked about experience or skills, highlight relevant details from the resume
    3. Be professional and helpful to the recruiter
    4. If asked about something not in the resume, politely state that the information is not available
    5. Avoid creating or inferring information not present in the resume
    6. Keep answers relevant to recruitment purposes
    7. Sound enthusiastic about Navya's qualifications when appropriate
    
    Remember, your goal is to present Navya in the best professional light while being truthful and accurate.
    """
    
    try:
        chat = model.start_chat(history=[])
        chat.send_message(system_prompt)
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Sidebar content
with st.sidebar:
    st.title("Navya Choudhari")
    st.subheader("Resume AI Assistant")
    st.markdown("---")
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("### About this App")
    st.markdown("""
    This AI-powered assistant helps recruiters explore Navya's resume through natural conversation.
    
    **Features:**
    - Ask about qualifications
    - Explore work experience
    - Learn about skills and education
    - Discover professional certifications
    - Inquire about projects and leadership
    """)
    st.markdown("---")
    st.markdown("### Sample Questions")
    st.markdown('<div class="sample-questions">', unsafe_allow_html=True)
    st.markdown("""
    - What is Navya's educational background?
    - Tell me about her work experience at Zomato
    - What programming languages does she know?
    - What certifications does she have?
    - What projects has she worked on?
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Main content
st.title("💬 Navya's Resume AI Assistant")
st.markdown("""
<div class="highlight">
Ask me anything about Navya's qualifications, experience, skills, or education!
</div>
""", unsafe_allow_html=True)

# Initialize Gemini
model = configure_gemini()

# Display chat history
for message in st.session_state.messages:
    with st.container():
        avatar_img = "https://www.clipartmax.com/png/small/179-1797946_user-icon-gear-svg-png-icon-free-download-profile-icon-png.png" if message['role'] == 'bot' else None
        avatar_html = f'<img class="avatar" src="{avatar_img}" />' if avatar_img else '<div style="width:40px;"></div>'
        
        st.markdown(f"""
        <div class="chat-message {message['role']}">
            {avatar_html}
            <div class="message">{message['content']}</div>
        </div>
        """, unsafe_allow_html=True)

# Chat input
user_question = st.text_input("Ask a question about Navya's resume:", key="user_input")

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("Send"):
        if user_question:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_question})
            
            # Get AI response
            with st.spinner("Thinking..."):
                ai_response = get_gemini_response(model, user_question, st.session_state.resume_data)
            
            # Add AI response to chat history
            st.session_state.messages.append({"role": "bot", "content": ai_response})
            
            # Rerun the app to display the updated chat
            st.rerun()

with col2:
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("Powered by Gemini 1.5 Flash | Created with Streamlit | Coded by Navya", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
