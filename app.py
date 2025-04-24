PYTHON
import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime

# Configure page with professional settings
st.set_page_config(
    page_title="Navya Choudhari - AI Resume Assistant",
    page_icon="👩‍💼",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/navyachoudhari',
        'Report a bug': "mailto:navyachoudhari2@gmail.com",
        'About': "# AI-Powered Resume Assistant\nFor recruiters to explore Navya's qualifications interactively"
    }
)

# Enhanced Custom CSS
st.markdown("""
<style>
    :root {
        --primary-color: #11567f;
        --secondary-color: #2196f3;
        --accent-color: #e3f2fd;
        --text-color: #333333;
        --light-bg: #f8fafc;
    }
    
    .main {
        background-color: var(--light-bg);
        color: var(--text-color);
    }
    
    .stApp {
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 2rem;
        border-radius: 0 0 15px 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: flex-start;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s ease;
    }
    
    .chat-message:hover {
        transform: translateY(-2px);
    }
    
    .chat-message.user {
        background-color: var(--accent-color);
        border-left: 5px solid var(--secondary-color);
        margin-left: 20%;
    }
    
    .chat-message.bot {
        background-color: white;
        border-left: 5px solid var(--primary-color);
        margin-right: 20%;
    }
    
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1.2rem;
        flex-shrink: 0;
    }
    
    .chat-message .message {
        flex-grow: 1;
    }
    
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 8px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #0d4b6f;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .stTextInput>div>div>input {
        border-radius: 8px !important;
        padding: 12px !important;
        border: 1px solid #ddd !important;
    }
    
    h1, h2, h3 {
        color: var(--primary-color);
    }
    
    .highlight-box {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid var(--secondary-color);
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
    
    .sidebar .sidebar-content {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0 15px 15px 0;
        box-shadow: 2px 0 10px rgba(0,0,0,0.05);
    }
    
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #666;
        font-size: 0.9rem;
        margin-top: 2rem;
        border-top: 1px solid #eee;
    }
    
    .typing-indicator {
        display: inline-block;
        padding-left: 5px;
    }
    
    .typing-indicator span {
        height: 8px;
        width: 8px;
        background-color: #666;
        border-radius: 50%;
        display: inline-block;
        margin-right: 3px;
        opacity: 0.4;
    }
    
    .typing-indicator span:nth-child(1) {
        animation: typing 1s infinite;
    }
    
    .typing-indicator span:nth-child(2) {
        animation: typing 1s infinite 0.2s;
    }
    
    .typing-indicator span:nth-child(3) {
        animation: typing 1s infinite 0.4s;
    }
    
    @keyframes typing {
        0% { opacity: 0.4; transform: translateY(0); }
        50% { opacity: 1; transform: translateY(-3px); }
        100% { opacity: 0.4; transform: translateY(0); }
    }
    
    .resume-section {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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
if 'last_activity' not in st.session_state:
    st.session_state.last_activity = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

# Function to get AI response with typing animation effect
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
    8. Format responses with bullet points when listing multiple items
    9. Highlight key achievements with bold text
    10. Keep responses between 50-150 words unless more detail is requested
    
    Remember, your goal is to present Navya in the best professional light while being truthful and accurate.
    """
    
    try:
        chat = model.start_chat(history=[])
        chat.send_message(system_prompt)
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Sidebar with enhanced content
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("Navya Choudhari")
    st.markdown("**Economics & Psychology Graduate**")
    st.markdown("📍 Bangalore, India")
    st.markdown("---")
    
    st.markdown("### Quick Resume Overview")
    with st.expander("📚 Education"):
        st.markdown("""
        - **CHRIST University**  
          B.A Economics & Psychology (2023-Present)  
          Relevant coursework: Econometrics, Statistics, Developmental Psychology
        - **Hopetown Girls' School** (2021-2023)
        """)
    
    with st.expander("💼 Experience"):
        st.markdown("""
        - **Grapevine** - Growth Intern  
          - 22% increase in user engagement  
          - Market research & competitor analysis
        - **Zomato** - Financial Analyst  
          - Profitability forecasting  
          - Business intelligence reporting
        """)
    
    with st.expander("📜 Certifications"):
        st.markdown("""
        - McKinsey Forward Learning (2025)
        - CFA Level 1 Candidate
        - SEBI Investor Certification (43/50)
        """)
    
    st.markdown("---")
    st.markdown("### Sample Questions")
    sample_questions = [
        "What is Navya's educational background?",
        "Tell me about her work experience at Zomato",
        "What programming languages does she know?",
        "What projects has she worked on?",
        "How did Navya contribute to user growth at Grapevine?",
        "What leadership experience does she have?",
        "What are Navya's strongest technical skills?"
    ]
    
    for question in sample_questions:
        if st.button(question, key=f"sample_{question[:20]}"):
            st.session_state.user_input = question
            st.rerun()
    
    st.markdown("---")
    st.markdown(f"**Last activity:** {st.session_state.last_activity}")

# Main content with improved layout
st.markdown("""
<div class="header">
    <h1 style="color: white; margin-bottom: 0;">Navya Choudhari</h1>
    <p style="color: white; opacity: 0.9; margin-top: 0.5rem;">AI-Powered Resume Assistant</p>
</div>
""", unsafe_allow_html=True)

# Initialize Gemini
model = configure_gemini()

# Display chat history with typing animation effect
for message in st.session_state.messages:
    with st.container():
        avatar = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png" if message['role'] == 'user' else "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
        
        if message['role'] == 'bot' and message.get('thinking', False):
            with st.markdown(f"""
            <div class="chat-message bot">
                <img class="avatar" src="{avatar}" />
                <div class="message">
                    <div class="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True):
                time.sleep(1)  # Simulate thinking time
        else:
            st.markdown(f"""
            <div class="chat-message {message['role']}">
                <img class="avatar" src="{avatar}" />
                <div class="message">{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)

# Chat input with improved UX
with st.form(key='chat_form'):
    user_question = st.text_input(
        "Ask a question about Navya's resume:",
        key="user_input",
        placeholder="e.g. What experience does Navya have with data analysis?"
    )
    
    col1, col2, col3 = st.columns([1,1,3])
    with col1:
        send_button = st.form_submit_button("🚀 Send")
    with col2:
        clear_button = st.form_submit_button("🗑️ Clear Chat")
    
    if send_button and user_question:
        # Update last activity
        st.session_state.last_activity = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_question})
        
        # Add temporary "thinking" message
        st.session_state.messages.append({"role": "bot", "content": "", "thinking": True})
        
        # Rerun to show thinking animation
        st.rerun()
        
        # Replace thinking message with actual response
        st.session_state.messages.pop()
        with st.spinner(""):
            ai_response = get_gemini_response(model, user_question, st.session_state.resume_data)
        st.session_state.messages.append({"role": "bot", "content": ai_response})
        
        # Rerun to show the response
        st.rerun()
    
    if clear_button:
        st.session_state.messages = []
        st.session_state.last_activity = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.rerun()

# Resume quick view section
st.markdown("---")
st.markdown("### 📄 Resume Quick View")
with st.expander("View Full Resume Summary"):
    st.markdown("""
    <div class="resume-section">
        <h4>🎓 Education</h4>
        <p><strong>CHRIST University</strong> | B.A Economics & Psychology (2023-Present)<br>
        Relevant coursework: Microeconomics, Econometrics, Statistics, Social Psychology</p>
        
        <h4>💼 Professional Experience</h4>
        <p><strong>Grapevine</strong> | Growth Intern (April 2025-Present)<br>
        - Contributed to 22% user engagement growth<br>
        - Conducted market and competitor research</p>
        
        <p><strong>Zomato</strong> | Financial Analyst (Nov 2024)<br>
        - Analyzed revenue trends and operational costs<br>
        - Worked with large datasets using Excel and SQL</p>
        
        <h4>🛠️ Technical Skills</h4>
        <p>Microsoft Suite, R programming, Python, SQL, Canva, Jamovi</p>
        
        <h4>🏆 Achievements</h4>
        <p>- Winner of Delhi University Business Fest<br
