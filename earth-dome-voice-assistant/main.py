import os
import time
from dotenv import load_dotenv

from SRC.microphone import listen_to_microphone
from SRC.language_profile import get_language_profile
from SRC.assistant import get_chatgpt_reply
from SRC.tts import speak_text

# === Load credentials from .env ===
load_dotenv()
GOOGLE_TTS_CREDENTIALS = os.getenv("GOOGLE_TTS_CREDENTIALS")
if not GOOGLE_TTS_CREDENTIALS:
    raise EnvironmentError("❌ GOOGLE_TTS_CREDENTIALS not found in .env file")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_TTS_CREDENTIALS

# === Static system prompt ===
SYSTEM_PROMPT = """
You are the Earth Dome Voice Assistant, installed inside a museum exhibition.
Only respond to questions related to the following:
- The Earth Dome installation
- Art and architecture
- Cultural heritage
- Sustainable materials
- Historical context
- Qatar’s legacy and museum initiatives

If a visitor asks about anything outside these topics (like politics, personal advice, general trivia, or unrelated tech), politely respond with:
"I'm here to guide you through the Earth Dome and topics around art, culture, and heritage. Could you ask something in that context?"
"""


AUTO_MESSAGES = [
    "Artevo have been working on this earth dome, but Shouq keep changing. Jahana is tired already.",
    "Welcome! You're experiencing the Earth Dome installation. Ask me anything about it.",
    "The Earth Dome installation is a space where art and science converge. Would you like to know how this dome was originally built?",
    "The Earth Dome connects past and future through natural textures and architectural memory. Would you like to hear the story behind it?",
    "The first Earth Dome was commissioned by His Highness Sheikh Khalifa bin Hamad Al Thani, and today it is reimagined by Qatar Museums as a way to honor the nation’s legacy through art, architecture, and collective memory.",
    "The Earth Dome holds stories of sustainability, culture, and design. Ask me anything you’d like to learn."
]

AUTO_RESPONSES = {
    "how this dome was originally built": (
        "The original Earth Dome was built in 1975 using compacted soil and hand tools by earth-architecture specialists. "
        "It demonstrated sustainable design using locally available materials and passive cooling strategies."
    ),
    "hear the story behind it": (
        "This dome tells the story of Qatar’s heritage through architectural language. Its textures and form are inspired by traditional materials, "
        "connecting visitors to a deeper cultural narrative."
    )
}

# === Main Loop ===
if __name__ == "__main__":
    print("📢 Earth Dome Assistant is running. Say something...")

    last_message_time = time.time()
    auto_index = 0

    try:
        while True:
            # Auto message every 60 seconds
            if time.time() - last_message_time >= 60:
                auto_message = AUTO_MESSAGES[auto_index]
                speak_text(auto_message, language_code="en-US", voice_name="en-US-Studio-O")
                last_message_time = time.time()
                auto_index = (auto_index + 1) % len(AUTO_MESSAGES)

            # Listen for user input
            question = listen_to_microphone(timeout=5)
            if question:
                if "stop" in question.lower():
                    print("🔴 Exiting.")
                    break

                # Check if question is an affirmative response to a previous auto question
                agreement_keywords = ["yes", "yeah", "sure", "please", "go ahead", "okay", "alright"]
                if any(word in question.lower() for word in agreement_keywords):
                    for key_phrase, response in AUTO_RESPONSES.items():
                        if key_phrase in AUTO_MESSAGES[auto_index - 1]:
                            print(f"🤖 Auto Response: {response}")
                            speak_text(response, language_code="en-US", voice_name="en-US-Studio-O")
                            break
                    continue

                # Process question with GPT
                profile = get_language_profile(question)
                reply = get_chatgpt_reply(question, SYSTEM_PROMPT)
                print(f"🤖 ChatGPT: {reply}")
                speak_text(reply, language_code=profile["speech"], voice_name=profile["tts"])

    except Exception as e:
        print(f"❌ Error: {e}")
