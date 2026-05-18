import streamlit as st
import groq
import os
from dotenv import load_dotenv
from gtts import gTTS
import tempfile
import pygame
import threading

# ------------------------------
# Load API key
# ------------------------------
load_dotenv()
GROQ_API_KEY = os.environ["GROQ_API_KEY"]
client = groq.Client(api_key=GROQ_API_KEY)

# ------------------------------
# TTS using gTTS + pygame (reliable, multilingual)
# ------------------------------
def speak_text(text, lang_code):
    """Convert text to speech and play it without blocking UI."""
    def _speak():
        # Create a temporary MP3 file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            temp_filename = fp.name
        # Generate speech
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(temp_filename)
        # Play audio
        pygame.mixer.init()
        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        # Cleanup
        pygame.mixer.quit()
        os.unlink(temp_filename)
    
    threading.Thread(target=_speak, daemon=True).start()

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="Multilingual Voice AI Agent", page_icon="🎙️")
st.title("🎙️ Multilingual Voice AI Agent")
st.markdown("Record a question – get a spoken answer in your chosen language.")

# Language mapping (display name -> gTTS language code)
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

    # Step 1: Transcribe
    with st.spinner("Transcribing..."):
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=("audio.wav", audio_bytes),
            response_format="text"
        )
    st.text_area("📝 You said:", transcription, height=80)

    # Step 2: Generate response in selected language
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

    # Step 3: Speak aloud (every time, non-blocking)
    speak_text(answer, lang_code)
    st.success(f"✅ Answer spoken aloud in {selected_lang_name}.")