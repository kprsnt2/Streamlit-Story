import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import random
import streamlit as st
import tempfile
import webbrowser

# Sample stories database
stories = [
    "Once upon a time, there was a little rabbit.",
    "In a magical land far away, there lived a brave knight.",
    "A long time ago, in a deep forest, there was a wise owl.",
    "On a sunny day, a mischievous monkey swung from tree to tree.",
]

def listen_for_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        try:
            audio = recognizer.listen(source, timeout=5)  # Set a timeout for listening
        except sr.WaitTimeoutError:
            st.warning("Listening timed out. Please type or click 'Listen' again.")
            return ""

    try:
        st.info("Recognizing...")
        user_input = recognizer.recognize_google(audio)
        st.write("You said:", user_input)
        return user_input.lower()
    except sr.UnknownValueError:
        st.error("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        st.error("Could not request results. Please check your internet connection.")
        return ""

def generate_story_response():
    return random.choice(stories)

def speak_text(text):
    tts = gTTS(text=text, lang="en")
    audio_file = "response.mp3"
    tts.save(audio_file)

    # Play the audio using playsound
    playsound.playsound(audio_file)
    os.remove(audio_file)  # Remove the audio file after playing

    st.write("Chatbot:", text)

def main():
    st.title("Story Chatbot")
    st.write("You can ask the chatbot to tell you a story.")

    user_input_type = st.radio("Select input type:", ("Speech", "Text"))

    if user_input_type == "Speech":
        user_input = listen_for_voice()
    else:
        user_input = st.text_input("Your Message:")

    if st.button("Send"):
        if "exit" in user_input:
            st.write("Goodbye!")
        elif "tell me a story" in user_input:
            story_response = generate_story_response()
            speak_text(story_response)
        else:
            st.write("Sorry, I didn't understand that. Please say 'tell me a story' or 'exit'.")

        st.text("")  # Add some space between conversations

    st.text("")  # Add some space between conversations
    st.subheader("Conversation History:")
    st.text("")  # Add some space between conversations

if __name__ == "__main__":
    main()
