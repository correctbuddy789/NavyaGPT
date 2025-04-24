import streamlit as st
import google.generativeai as genai

# Configure page
st.set_page_config(
    page_title="Talk to Navya 💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished UI
st.markdown("""
<style>
    /* Base styling */
    body, .main, .stApp {
        background-color: #f5f7fa;
        color: #111;
        font-family: 'Segoe UI', Tahoma, sans-serif;
    }
    .stApp {
        padding: 2rem 3rem;
    }
    /* Header */
    h1 {
        color: #0b3d91;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    /* Description text */
    .description {
        margin-bottom: 1.5rem;
        font-size: 1.1rem;
        color: #333;
    }
    /* Chat box container */
    .chat-box {
        border: 1px solid #ddd;
        padding: 1rem;
        border-radius: 1rem;
        background-color: #fff;
        max-height: 60vh;
        overflow-y: auto;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    /* Message styling */
    .user-msg, .bot-msg {
        margin: 0.75rem 0;
        padding: 0.5rem 1rem;
        border-radius: 1rem;
        max-width: 75%;
        line-height: 1.4;
    }
    .user-msg {
        background-color: #e1f5fe;
        text-align: right;
        margin-left: 25%;
    }
    .bot-msg {
        background-color: #f0f0f0;
        text-align: left;
        margin-right: 25%;
    }
    /* Button styling */
    .stButton>button {
        background-color: #0b3d91;
        color: #fff;
        border-radius: 0.5rem;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #093076;
    }
    /* Input box styling */
    .stTextInput>div>div>input {
        border: 1px solid #ccc;
        border-radius: 0.5rem;
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Hardcoded resume data
RESUME = """
NAVYA CHOUDHARI
Bangalore | navyachoudhari2@gmail.com | 08016568-058 | www.linkedin.com/in/navyachoudhari

... full resume ...
"""

# Initialize session state for chat history
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar with brief bio
with st.sidebar:
    st.header("About Navya")
    st.write("I'm Navya Choudhari, a growth intern and financial analyst with a passion for data-driven impact. Ask me about my background!")
    st.markdown("---")

# Main UI
st.title("💬 Talk to Navya")
st.markdown("<div class='description'>Chat with me to explore my qualifications, experience, projects, and skills. I’ll answer in first person!</div>", unsafe_allow_html=True)

# Configure Gemini with character safety
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={"temperature":0.7, "top_p":0.9, "max_output_tokens":512},
    safety_settings=[{"category":"HARM_CATEGORY_HARASSMENT","threshold":"BLOCK_MEDIUM_AND_ABOVE"}],
)

# Input and chat button
col1, col2 = st.columns([5, 1])
with col1:
    query = st.text_input("Your question:", placeholder="Ask me anything about my resume...")
with col2:
    send = st.button("Send")

# Handle sending
if send and query:
    st.session_state.history.append({"role":"user","content":query})
    # system prompt enhanced
    sys_prompt = (
        f"You are Navya Choudharii. Answer as Navya in first person based solely on this resume: {RESUME}. "
        "Never break character. If the user asks anything NSFW or outside resume scope, politely refuse."
    )
    chat = model.start_chat(history=[])
    chat.send_message(sys_prompt)
    resp = chat.send_message(query).text
    st.session_state.history.append({"role":"bot","content":resp})

# Display chat
st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
for msg in st.session_state.history:
    if msg['role'] == 'user':
        st.markdown(f"<div class='user-msg'><strong>You:</strong> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'><strong>Navya:</strong> {msg['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Clear chat option
if st.button("Clear Chat"):
    st.session_state.history = []
