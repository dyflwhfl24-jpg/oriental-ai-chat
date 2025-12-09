import streamlit as st
from openai import OpenAI

# ------------------------------------------------------
# 페이지 설정
# ------------------------------------------------------
st.set_page_config(page_title="竹风对话 · Bamboo Chat", layout="wide")

# ------------------------------------------------------
# 대나무 테마 스타일
# ------------------------------------------------------
BAMBOO_STYLE = """
<style>
body {
    background: url('https://i.imgur.com/YTgLx5n.png'); /* 은은한 대나무 문양 */
    background-size: cover;
    background-attachment: fixed;
    font-family: 'Noto Serif SC', serif;
}

/* 중앙 큰 제목 */
.main-title {
    text-align: center; 
    color: #154c2e; 
    font-size: 42px;
    margin-top: 10px;
    text-shadow: 1px 1px 1px #ccc;
}

/* 대화 박스 */
.chat-container {
    border-radius: 15px;
    padding: 20px;
    background: rgba(255, 255, 245, 0.85);
    border: 3px solid #d1c6a8;
    backdrop-filter: blur(3px);
}

/* 유저 메시지 */
.user-msg {
    background: #d4ffe1;
    color: #003c1f;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: right;
    border: 1px solid #91c7a6;
}

/* AI 메시지 */
.bot-msg {
    background: #fff4d7;
    color: #5a3b00;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: left;
    border: 1px solid #e3c59b;
}

/* 입력창 */
input[type="text"] {
    background: #fbfaf4 !important;
    border-radius: 10px !important;
    border: 2px solid #8bb892 !important;
    padding: 10px !important;
}

/* 대나무 장식 선 */
.bamboo-line {
    width: 100%;
    height: 4px;
    background: url('https://i.imgur.com/fo0Qe0z.png') repeat-x;
    margin: 20px 0;
}
</style>
"""

st.markdown(BAMBOO_STYLE, unsafe_allow_html=True)

# ------------------------------------------------------
# OpenAI 클라이언트 (Secret Key)
# ------------------------------------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ------------------------------------------------------
# 메시지 초기화
# ------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요. 무엇을 도와드릴까요? (竹风对话)"}
    ]

# ------------------------------------------------------
# 제목
# ------------------------------------------------------
st.markdown("<div class='main-title'>🎋 竹风对话 · Bamboo AI Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='bamboo-line'></div>", unsafe_allow_html=True)

# ------------------------------------------------------
# 채팅 박스
# ------------------------------------------------------
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------
# 사용자 입력
# ------------------------------------------------------
user_input = st.text_input("대화창", "", key="input_text", placeholder="메시지를 입력하세요...")

if user_input:
    # 유저 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})

    # OpenAI 호출
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=st.session_state.messages,
        temperature=0.7
    )

    bot_reply = response.choices[0].message["content"]

    # 반복 방지
    if st.session_state.messages[-1]["content"] != bot_reply:
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    st.session_state.input_text = ""
    st.experimental_rerun()
