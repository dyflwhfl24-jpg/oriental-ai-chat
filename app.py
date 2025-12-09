import streamlit as st
from openai import OpenAI

# -----------------------------
# 기본 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="东方AI 대화 시스템",
    page_icon="🀄",
    layout="centered"
)

# -----------------------------
# 중국풍 스타일 (전체 CSS)
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Serif SC', serif !important;
    background: #f9f5ef;
}

.chat-box {
    background: #fff9f2;
    border: 2px solid #d4a373;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 10px;
}

.user {
    color: #b32d2e;
    font-weight: bold;
}

.bot {
    color: #5b3716;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 제목
# -----------------------------
st.markdown(
    "<h1 style='text-align:center;color:#b32d2e;'>✨ 어른스러운 东方AI 대화 시스템 ✨</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;color:#5b3716;'>동양의 지혜로 당신과 대화를 나눕니다.</p>",
    unsafe_allow_html=True
)

# -----------------------------
# API Key 입력
# -----------------------------
api_key = st.text_input("🔑 OpenAI API Key 입력", type="password", key="api_key")
if not api_key:
    st.stop()

client = OpenAI(api_key=api_key)

# -----------------------------
# 대화 메시지 리스트 초기화
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "당신은 지혜롭고 어른스러운 중국풍 AI입니다. 품격 있고 부드러운 말투로 대화하세요."
        }
    ]

# -----------------------------
# 입력 처리 함수 (반복 입력 방지)
# -----------------------------
def handle_input():
    user_msg = st.session_state.input

    if not user_msg.strip():
        return

    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": user_msg})

    # AI 응답 생성
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    # AI 메시지 저장
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # 입력창 초기화
    st.session_state.input = ""


# -----------------------------
# 기존 대화 출력
# -----------------------------
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue

    css_class = "user" if msg["role"] == "user" else "bot"
    st.markdown(
        f"<div class='chat-box {css_class}'>{msg['content']}</div>",
        unsafe_allow_html=True
    )

# -----------------------------
# 대화 입력창 (엔터 자동 전송)
# -----------------------------
st.text_input(
    "💬 대화창",
    placeholder="대화를 입력하세요...",
    key="input",
    on_change=handle_input
)
