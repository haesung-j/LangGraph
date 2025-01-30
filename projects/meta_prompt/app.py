import streamlit as st
import requests
import json
import time
import uuid
from typing import Optional

st.set_page_config(page_title="Meta Prompt Generator", page_icon="🤖", layout="wide")

st.title("Meta Prompt Generator 🤖")
st.markdown("LLM과 대화하며 프롬프트를 생성해보세요.")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# thread_id 초기화 (세션별 고유 ID)
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# 이전 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요"):
    # 사용자 메시지 표시
    with st.chat_message("human"):
        st.markdown(prompt)

    # 메시지 저장
    st.session_state.messages.append({"role": "human", "content": prompt})

    # AI 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # SSE 스트림 연결
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
                                # JSON 파싱
                                data = json.loads(line.split("data: ")[-1])

                                if "text" in data:
                                    full_response += data["text"]
                                    message_placeholder.markdown(full_response + "▌")
                                elif "error" in data:
                                    st.error(f"Error: {data['error']}")
                                    break

                            except json.JSONDecodeError as e:
                                st.error(f"JSON 파싱 에러: {e}")
                                continue

                            time.sleep(0.01)

            # 최종 응답 표시
            message_placeholder.markdown(full_response)

            # AI 응답 저장
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except requests.exceptions.RequestException as e:
            st.error(f"네트워크 에러: {str(e)}")
        except Exception as e:
            st.error(f"예상치 못한 에러: {str(e)}")

# 디버깅용 세션 정보 표시 (필요시 주석 해제)
# st.sidebar.write("Session Thread ID:", st.session_state.thread_id)
