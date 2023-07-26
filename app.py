import speech_recognition as sr
from gtts import gTTS
import playsound
import pygame
import random
import streamlit as st

# Initialize pygame mixer only once
if not pygame.get_init():
    pygame.mixer.init()
    
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
        audio = recognizer.listen(source)

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
    audio_file = "/app/response.mp3"  # Absolute path to the audio file
    tts.save(audio_file)

    # Load the audio file with pygame
    pygame.mixer.music.load(audio_file)

    # Play the audio
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        continue

    # Clean up
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    st.write("Chatbot:", text)

def main():
    st.title("Story Chatbot")
    st.write("You can ask the chatbot to tell you a story.")
    
    user_input = st.text_input("Your Message:")
    
    if st.button("Send"):
        if "exit" in user_input:
            st.write("Goodbye!")
        elif "tell me a story" in user_input:
            story_response = generate_story_response()
            speak_text(story_response)
        else:
            st.write("Sorry, I didn't understand that. Please say 'tell me a story' or 'exit'.")

if __name__ == "__main__":
    main()
