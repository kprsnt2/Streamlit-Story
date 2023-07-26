import speech_recognition as sr
from gtts import gTTS
import playsound
import random
import streamlit as st

# Sample stories database
stories = [
    "Once upon a time, there was a little rabbit.",
    "In a magical land far away, there lived a brave knight.",
    "A long time ago, in a deep forest, there was a wise owl.",
    "On a sunny day, a mischievous monkey swung from tree to tree.",
    "Once upon a time, there was a shiny red train chugging along the tracks.",
    "In a bustling city, a double-decker bus roamed the streets, picking up passengers.",
    "A long drive through the countryside, a family of bears went on a car adventure.",
]


def listen_for_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        user_input = recognizer.recognize_google(audio)
        print("You said:", user_input)
        return user_input.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Could not request results. Please check your internet connection.")
        return ""

def generate_story_response():
    return random.choice(stories)

def speak_text(text):
    tts = gTTS(text=text, lang="en")
    audio_file = "response.mp3"
    tts.save(audio_file)

    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.quit()
    print("Chatbot:", text)

def main():
    st.title("Story Chatbot")
    st.write("You can ask the chatbot to tell you a story.")

    user_input = st.text_input("Your Message:")
    if st.button("Send"):
        # Process the user input here and generate the response
        if "exit" in user_input:
            response = "Goodbye!"
        elif "tell me a story" in user_input:
            response = generate_story_response()
            speak_text(response)
        else:
            response = "Sorry, I didn't understand that. Please say 'tell me a story' or 'exit'."

        st.write("Chatbot says:", response)

if __name__ == "__main__":
    main()
