import openai
from openai import OpenAI
from google.cloud import texttospeech
import speech_recognition as sr
import os
from langdetect import detect
import time


LANGUAGE_MAP = {
    "en": {"speech": "en-US", "tts": "en-US-Wavenet-D"},
    "fr": {"speech": "fr-FR", "tts": "fr-FR-Wavenet-E"},
    "ar": {"speech": "ar-XA", "tts": "ar-XA-Wavenet-B"},
    "tl": {"speech": "fil-PH", "tts": "fil-PH-Wavenet-A"},  # Tagalog
}

def get_language_profile(text):
    lang_code = detect(text)
    print(f"🌐 Detected language: {lang_code}")
    return LANGUAGE_MAP.get(lang_code[:2], LANGUAGE_MAP["en"])  # fallback to English



# === API Setup ===
client = OpenAI(api_key="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")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\MARK\Documents\Gallery 11 project\tts-service-key.json"

# === Get user's voice input ===
def listen_to_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"📝 You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❗ Sorry, I couldn't understand that.")
        return None
    except sr.RequestError:
        print("❗ Speech recognition service unavailable.")
        return None

# === Get ChatGPT response ===
def get_chatgpt_reply(prompt):
    system_prompt = """
You are a knowledgeable and warm museum guide for the Earth Dome installation at the National Museum of Qatar.

Your job is to answer ONLY questions related to the Earth Dome — its history, symbolism, purpose, people involved, and its importance during the 1975 opening and the 2025 revival. Do not answer anything unrelated to the Earth Dome.

Here’s the Earth Dome context:

- The Earth Dome was originally inaugurated in 1975 by Sheikh Khalifa bin Hamad Al Thani, as part of Qatar’s first national museum.
- It was installed opposite the main entrance of the State Palace (Qasr Al Dawla) and welcomed visitors with a film featuring Quranic verses and scientific theories like the Great Dust Cloud and continental drift.
- The dome narrates the geological formation of Qatar over millions of years — from being an island to becoming a peninsula.
- It was a key feature visited by dignitaries such as Sheikh Zayed, King Khalid, Muammar Gaddafi, and others.
- In 2025, it was reimagined by Qatari artist Shouq Al Mana under the patronage of H.E. Sheikha Al Mayassa bint Hamad Al Thani for the museum’s 50th anniversary.
- It symbolizes the merging of science, heritage, and identity — anchoring Qatar’s past while pointing toward the future.

If the user asks about another gallery, topic, or something outside this, politely respond:
"Sorry, I can only answer questions related to the Earth Dome."

Respond in a calm, confident, and educational tone, like a live cultural guide speaking to a visitor.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content



# === Speak ChatGPT response ===
def speak_text(text, language_code="en-US", voice_name="en-US-Wavenet-D"):
    tts_client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = tts_client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config
    )

    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)

    os.system("start output.mp3")

# === Auto-play welcome message every 60 seconds ===
def play_welcome_message():
    welcome_text = (
        "Welcome to the Earth Dome exhibition stand. "
        "Feel free to ask any question about the history or meaning of this unique installation."
    )
    speak_text(welcome_text)


import time  # Make sure this stays near the top of your file

# === MAIN LOOP ===
if __name__ == "__main__":
    last_welcome_time = time.time()

    while True:
        # 🔁 Play welcome message every 60 seconds
        if time.time() - last_welcome_time >= 60:
            play_welcome_message()
            last_welcome_time = time.time()

        print("🗣️ Speak your question directly (no wake word needed)...")
        question = listen_to_microphone()

        if question:
            if "stop" in question.lower():
                print("🛑 Exiting.")
                break

            # 🌐 Detect language
            profile = get_language_profile(question)

            # 🤖 Get response
            reply = get_chatgpt_reply(question)
            print(f"🤖 ChatGPT: {reply}")

            # 🔊 Speak the reply
            speak_text(reply, language_code=profile["speech"], voice_name=profile["tts"])
