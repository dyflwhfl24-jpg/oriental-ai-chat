import streamlit as st
from openai import OpenAI

# -----------------------
# 페이지 설정
# -----------------------
st.set_page_config(page_title="竹风对话 · Bamboo Chat", layout="wide")

# -----------------------
# 스타일 (대나무 테마)
# -----------------------
BAMBOO_STYLE = """
<style>
body {
    background: url('https://i.imgur.com/YTgLx5n.png');
    background-size: cover;
    background-attachment: fixed;
    font-family: 'Noto Serif SC', serif;
}
.main-title {
    text-align: center;
    color: #154c2e;
    font-size: 42px;
    margin-top: 10px;
    text-shadow: 1px 1px 1px #ccc;
}
.chat-container {
    border-radius: 15px;
    padding: 20px;
    background: rgba(255, 255, 245, 0.85);
    border: 3px solid #d1c6a8;
    backdrop-filter: blur(3px);
}
.user-msg {
    background: #d4ffe1;
    color: #003c1f;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: right;
    border: 1px solid #91c7a6;
}
.bot-msg {
    background: #fff4d7;
    color: #5a3b00;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: left;
    border: 1px solid #e3c59b;
}
input[type="text"] {
    background: #fbfaf4 !important;
    border-radius: 10px !important;
    border: 2px solid #8bb892 !important;
    padding: 10px !important;
}
.bamboo-line {
    width: 100%;
    height: 4px;
    background: url('https://i.imgur.com/fo0Qe0z.png') repeat-x;
    margin: 20px 0;
}
</style>
"""
st.markdown(BAMBOO_STYLE, unsafe_allow_html=True)

# -----------------------
# OpenAI 클라이언트 (서버 시크릿 사용)
# 반드시 Streamlit Cloud의 Secrets에 OPENAI_API_KEY를 저장하세요.
# -----------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------
# 세션 초기화
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요. 무엇을 도와드릴까요? (竹风对话)"}
    ]

# -----------------------
# 입력 처리 콜백 (on_change에 연결)
# -----------------------
def handle_input():
    user_msg = st.session_state.input_text  # widget key와 동일해야 함
    if not user_msg or not user_msg.strip():
        # 빈 입력이면 아무것도 안함
        st.session_state.input_text = ""  # callback 안에서 초기화는 안전
        return

    # 1) 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": user_msg})

    # 2) OpenAI 호출 — 최신 SDK 접근 방식 사용
    response = client.chat.completions.create(
        model="gpt-4o-mini",            # 필요하면 모델명 바꿔도 됨
        messages=st.session_state.messages,
        temperature=0.7
    )

    # ===== 중요한 수정 =====
    # 객체 속성으로 접근해야 함 (대괄호가 아님)
    bot_reply = response.choices[0].message.content

    # 3) 중복 응답 방지 (마지막 메시지와 동일하면 추가하지 않음)
    last_content = st.session_state.messages[-1]["content"] if st.session_state.messages else None
    if bot_reply != last_content:
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # 4) 입력 초기화 (callback 내부에서 안전하게 수행)
    st.session_state.input_text = ""


# -----------------------
# 화면 렌더링
# -----------------------
st.markdown("<div class='main-title'>🎋 竹风对话 · Bamboo AI Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='bamboo-line'></div>", unsafe_allow_html=True)

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# text_input: on_change에 handle_input 연결 (엔터 입력 시 실행)
# key 이름은 handle_input에서 사용하는 이름과 같아야 함
# -----------------------
st.text_input(
    label="대화창",
    key="input_text",
    placeholder="메시지를 입력하세요...",
    on_change=handle_input
)
