import streamlit as st
import google.generativeai as genai

# Configure page
st.set_page_config(
    page_title="Resume AI Assistant",
    layout="wide",
)

# Styles: minimal, high-contrast
st.markdown("""
<style>
    .main {
        background-color: #ffffff;
        color: #000000;
    }
    .stButton>button {
        background-color: #000000;
        color: #ffffff;
        border-radius: 0.3rem;
        padding: 0.4rem 0.8rem;
        border: none;
    }
    h1, h2, h3 {
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)

# Resume content
RESUME = """
... (Navya's resume data) ...
"""

# Configure Gemini API
def configure_gemini():
    api_key = st.secrets.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={"temperature": 0.7, "top_p": 0.95, "max_output_tokens": 512},
        safety_settings=[{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}]
    )

# Chat history
if 'history' not in st.session_state:
    st.session_state.history = []

# UI
st.title("Navya's Resume Assistant")
st.write("Ask me about my qualifications, experience, or skills.")

model = configure_gemini()

query = st.text_input("Your question:")
if st.button("Send") and query:
    st.session_state.history.append({"role": "user", "content": query})
    # system prompt sets first-person
    system = f"You are Navya Choudhari. Answer in first person based on the resume: {RESUME}"
    chat = model.start_chat(history=[])
    chat.send_message(system)
    response = chat.send_message(query)
    reply = response.text
    st.session_state.history.append({"role": "bot", "content": reply})

for msg in st.session_state.history:
    if msg['role'] == 'user':
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Navya:** {msg['content']}")

if st.button("Clear"):
    st.session_state.history = []
