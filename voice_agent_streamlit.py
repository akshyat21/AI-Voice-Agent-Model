import streamlit as st
import groq
import os
from dotenv import load_dotenv
from gtts import gTTS
import tempfile

# Load API key
load_dotenv()
GROQ_API_KEY = os.environ["GROQ_API_KEY"]
client = groq.Client(api_key=GROQ_API_KEY)

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="Multilingual Voice AI Agent", page_icon="🎙️")
st.title("🎙️ Multilingual Voice AI Agent")
st.markdown("Record a question – get a spoken answer in your chosen language.")

# Language mapping
lang_options = {
    "English": "en",
    "العربية (Arabic)": "ar",
    "हिन्दी (Hindi)": "hi",
    "Français (French)": "fr",
    "Español (Spanish)": "es"
}
selected_lang_name = st.selectbox("Select response language", list(lang_options.keys()))
lang_code = lang_options[selected_lang_name]

# Audio input
audio_file = st.audio_input("Speak your question")

if audio_file is not None:
    audio_bytes = audio_file.read()

    # 1. Transcribe
    with st.spinner("Transcribing..."):
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=("audio.wav", audio_bytes),
            response_format="text"
        )
    st.text_area("📝 You said:", transcription, height=80)

    # 2. Generate response in selected language
    with st.spinner("Thinking..."):
        system_prompt = f"You are a helpful, concise assistant. Always respond in {selected_lang_name} language. Keep your answer short and clear."
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcription}
            ],
        )
        answer = completion.choices[0].message.content
    st.text_area("🤖 AI answer:", answer, height=120)

    # 3. Convert answer to speech and play automatically
    with st.spinner("Generating speech..."):
        tts = gTTS(text=answer, lang=lang_code, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            with open(tmp_file.name, 'rb') as audio_f:
                audio_bytes_out = audio_f.read()
        # Autoplay the audio
        st.audio(audio_bytes_out, format='audio/mp3', autoplay=True)
        # Optional: remove temp file after playback (can't delete immediately, but it's fine)
    st.success(f"✅ Answer spoken aloud in {selected_lang_name}.")