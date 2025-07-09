import speech_recognition as sr

def listen_to_microphone(timeout=5, phrase_time_limit=10):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("⏱️ Timeout: No speech detected.")
            return None
        except sr.UnknownValueError:
            print("🤷 Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            print("🚫 Speech recognition service error.")
            return None
