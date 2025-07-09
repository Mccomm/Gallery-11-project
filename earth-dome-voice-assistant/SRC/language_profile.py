# SRC/language_profile.py

def get_language_profile(text):
    # Always return English language and TTS voice
    return {
        "speech": "en-US",
        "tts": "en-US-Wavenet-F"
    }
