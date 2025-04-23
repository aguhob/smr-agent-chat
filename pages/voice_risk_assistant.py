import streamlit as st
import speech_recognition as sr
import pyttsx3
from lyzr import Agent
import openai

# Set your OpenAI key (or use Streamlit secrets)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Init Lyzr agent (uses GPT-3.5 by default)
agent = Agent(
    model="gpt-3.5-turbo",
    system="You are a kind, intelligent assistant helping with climate, community, and civic engagement."
)

# TTS setup
tts = pyttsx3.init()
def speak(text):
    tts.say(text)
    tts.runAndWait()

# Speech transcription
def transcribe():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now.")
        audio = r.listen(source, phrase_time_limit=10)
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError as e:
            return f"Error: {e}"

# App UI
st.title("🎙️ Voice & Text Agent (Streamlit + Lyzr)")

input_mode = st.radio("Choose input mode:", ["🎤 Voice", "⌨️ Type"], horizontal=True)

if input_mode == "🎤 Voice":
    if st.button("Start Voice Agent"):
        user_input = transcribe()
        st.write(f"🗣️ You said: `{user_input}`")

        if user_input and not user_input.startswith("Error"):
            response = agent.run(user_input)
            st.success(f"🤖 Agent: {response}")
            speak(response)

elif input_mode == "⌨️ Type":
    typed_input = st.text_input("Type your question:")
    if typed_input:
        response = agent.run(typed_input)
        st.success(f"🤖 Agent: {response}")
        speak(response)
