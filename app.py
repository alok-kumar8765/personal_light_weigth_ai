
import streamlit as st
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="Personal AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# App heading
st.title("🤖 Personal AI Assistant")
st.write("Your smart companion for questions, ideas, summaries, and more!")

# Sidebar API key input
st.sidebar.header("Settings")

api_key = st.sidebar.text_input(
    "Enter your OpenAI API Key:",
    type="password"
)

if not api_key:
    st.sidebar.info("Please enter your OpenAI API key to continue.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful personal AI assistant. "
                "Provide clear, concise, and friendly responses."
            )
        }
    ]

# Display chat history (skip the system message)
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add and display user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages
                )

                ai_reply = response.choices[0].message.content

                if ai_reply is None:
                    ai_reply = "Sorry, I couldn't generate a response."

                st.markdown(ai_reply)

                # Save assistant response
                st.session_state.messages.append(
                    {"role": "assistant", "content": ai_reply}
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")
