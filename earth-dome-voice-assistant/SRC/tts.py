import os
import uuid
from playsound import playsound
from google.cloud import texttospeech

def speak_text(text, language_code="en-US", voice_name="en-US-Studio-O"):
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
        input=input_text, voice=voice, audio_config=audio_config
    )

    # 🔧 Create folder for temporary audio files
    temp_dir = "temp_audio"
    os.makedirs(temp_dir, exist_ok=True)

    # 🎧 Save to unique file inside that folder
    filename = os.path.join(temp_dir, f"output_{uuid.uuid4().hex}.mp3")
    with open(filename, "wb") as out:
        out.write(response.audio_content)

    try:
        playsound(filename)  # ⏸️ Wait until audio finishes
    finally:
        os.remove(filename)  # 🧹 Clean up after playback
