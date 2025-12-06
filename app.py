import streamlit as st
from main import rag_chain
from gtts import gTTS
from datetime import datetime
from agent_fallback import agent_answer

st.set_page_config(page_title="गीता-रामचरितमानस AI", page_icon="ॐ")
st.markdown("<h1 style='text-align: center; color: #FF4500;'>गीता-रामचरितमानस AI</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("प्रश्न पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("श्री राम बता रहे हैं..."):
            # मेमोरी को सही तरीके से भेज रहे हैं
            history = st.session_state.messages[-10:] if st.session_state.messages else []
            answer = agent_answer(prompt, history)

        st.write(answer)

        # ऑडियो
        audio_file = f"temp_{datetime.now().strftime('%H%M%S')}.mp3"
        tts = gTTS(text=answer, lang='hi', slow=False)
        tts.save(audio_file)
        st.audio(audio_file)

    st.session_state.messages.append({"role": "assistant", "content": answer})