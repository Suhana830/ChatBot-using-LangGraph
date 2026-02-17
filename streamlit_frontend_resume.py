import streamlit as st
import uuid
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# -----------------------------
# Initialize session state
# -----------------------------


if "chats" not in st.session_state:
    st.session_state["chats"] = {} 

if "current_chat" not in st.session_state:
    st.session_state["current_chat"] = None

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("LangGraph Chats")

# New chat button
if st.sidebar.button("➕ New Chat"):
    
    st.session_state["current_chat"] = str(uuid.uuid4())
    st.rerun()


# st.session_state["chats"] = {
#     "a1b2c3": [ {"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello"} ],
#     "d4e5f6": [ {"role": "user", "content": "How are you?"} ]
# }

st.sidebar.text("MY Conversations")
for chat_id, messages in st.session_state["chats"].items():
    if len(messages) > 0:
        if st.sidebar.button(f"ChatID: {chat_id[:6]}", key=chat_id):
            st.session_state["current_chat"] = chat_id
            st.rerun()

# -----------------------------
# Load current chat
# -----------------------------
if st.session_state["current_chat"] is None:
    st.info("Click 'New Chat' to start a conversation.")
    st.stop()

chat_id = st.session_state["current_chat"]

# Load messages or empty if new chat
messages = st.session_state["chats"].get(chat_id, [])

config = {"configurable": {"thread_id": chat_id}}

# -----------------------------
# Display chat messages
# -----------------------------
for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat input
# -----------------------------
user_input = st.chat_input("Type your message")

if user_input:
    # Append user message
    messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # -----------------------------
    # Stream AI response from LangGraph
    # -----------------------------
    with st.chat_message("assistant"):
        
        full_response = st.write_stream(chunk.content for chunk, metadata in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="messages"))

    
        messages.append({"role": "assistant", "content": full_response})

    
        st.session_state["chats"][chat_id] = messages
