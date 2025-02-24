import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
    "temperature": 0.8,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 4096,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction="You are an expert Software Engineer specializing in Developer Productivity and AI-powered IDEs. Provide concise, correct solutions with strategic insights into automated code generation, advanced debugging, and CI/CD automation. Your responses should enhance coding efficiency, suggest intelligent bug fixes, and streamline software development workflows.",
)

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Streamlit UI
st.title("🚀 AI-Powered IDE Assistant")
st.write("Welcome to the Intelligent IDE chatbot! Ask me anything about code generation, debugging, and CI/CD automation.")

with st.sidebar:
    st.header("⚙️ Configuration")
    selected_model = st.selectbox(
        "Choose Model",
        ["GEMINI 2.0 Flash"],
        index=0
    )
    st.divider()
    st.markdown("### Model Capabilities")
    st.markdown("""
    - 💡 Automated Code Generation
    - 🛠️ Debugging & Bug Fix Suggestions
    - 🔄 CI/CD Process Automation
    - 📊 Code Refactoring & Optimization
    """)
    st.divider()
    st.markdown("Built with [GEMINI](https://aistudio.google.com/)")

# Display chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask your coding or automation question:")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get chatbot response
    response = st.session_state.chat_session.send_message(user_input)
    chatbot_response = response.text

    # Add chatbot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": chatbot_response})
    with st.chat_message("assistant"):
        st.markdown(chatbot_response)
