import streamlit as st
from main import rag_chain
from gtts import gTTS
from datetime import datetime
from agent_fallback import agent_answer

st.set_page_config(page_title="गीता-रामचरितमानस AI", page_icon="")

st.markdown("<h1 style='text-align: center; color: #FF4500;'>गीता-रामचरितमानस AI</h1>", unsafe_allow_html=True)

# Memory सिर्फ app.py में
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुराने मैसेज दिखाओ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# नया सवाल
if prompt := st.chat_input("प्रश्न पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("श्री राम बता रहे हैं..."):
            # पिछले 6 मैसेज भेजो
            history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-6:]])
            answer = agent_answer(prompt)

        st.write(answer)

        # Audio
        audio_file = f"temp_{datetime.now().strftime('%H%M%S')}.mp3"
        tts = gTTS(text=answer, lang='hi', slow=False)
        tts.save(audio_file)
        st.audio(audio_file)

    # जवाब को memory में डालो
    st.session_state.messages.append({"role": "assistant", "content": answer})