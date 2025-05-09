import streamlit as st
import requests
import json
import time
import uuid
from typing import Optional

st.set_page_config(page_title="Meta Prompt Generator", page_icon="🤖", layout="wide")

st.title("Meta Prompt Generator 🤖")
st.markdown("Talk to LLM and generate prompts.")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize thread_id (unique ID per session)
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Show previous message
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Enter your message"):
    # Displaying user messages
    with st.chat_message("human"):
        st.markdown(prompt)

    # Save a message
    st.session_state.messages.append({"role": "human", "content": prompt})

    # Generate AI responses
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # SSE Stream Connections
            with requests.get(
                "http://localhost:8000/chat/stream",
                params={"query": prompt, "thread_id": st.session_state.thread_id},
                headers={"Accept": "text/event-stream"},
                stream=True,
            ) as response:
                response.raise_for_status()

                for line in response.iter_lines(decode_unicode=True):
                    if line.strip():
                        if line.startswith("data: "):
                            try:
                                # Parsing JSON
                                data = json.loads(line.split("data: ")[-1])

                                if "text" in data:
                                    full_response += data["text"]
                                    message_placeholder.markdown(full_response + "▌")
                                elif "error" in data:
                                    st.error(f"Error: {data['error']}")
                                    break

                            except json.JSONDecodeError as e:
                                st.error(f"JSON parsing errors: {e}")
                                continue

                            time.sleep(0.01)

            # Show final response
            message_placeholder.markdown(full_response)

            # Save AI responses
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except requests.exceptions.RequestException as e:
            st.error(f"Network errors: {str(e)}")
        except Exception as e:
            st.error(f"Unexpected errors: {str(e)}")

# Show session information for debugging (uncomment as needed)
# st.sidebar.write("Session Thread ID:", st.session_state.thread_id)
