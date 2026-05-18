# 🎙️ AI Voice Agent – Multilingual Speech‑to‑Speech Assistant

A fully functional voice AI agent that listens to your question, transcribes it, generates an intelligent answer, and speaks the response aloud – all in your chosen language. Built with **Streamlit**, **Groq API** (Whisper‑turbo + Llama 3.3), and **gTTS** for reliable, multilingual text‑to‑speech.

## ✨ Features

- 🎤 **Voice Input** – Record your question directly from the browser.
- 📝 **Fast Transcription** – Uses Groq’s `whisper-large-v3-turbo` (extremely low latency).
- 🧠 **Intelligent Answers** – Powered by Groq’s `llama-3.3-70b-versatile` model.
- 🌍 **Multilingual Output** – Supports English, Arabic, Hindi, French, Spanish (easily extendable).
- 🔊 **Reliable Speech** – gTTS + pygame ensures the answer is spoken **every time** (no refresh needed).
- ⚡ **Non‑blocking UI** – Speech plays in a background thread – the interface stays responsive.

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend / UI | [Streamlit](https://streamlit.io/) |
| Speech‑to‑Text | Groq – `whisper-large-v3-turbo` |
| Language Model | Groq – `llama-3.3-70b-versatile` |
| Text‑to‑Speech | `gTTS` (Google Text‑to‑Speech) + `pygame` |
| Environment | Python 3.9+ |
