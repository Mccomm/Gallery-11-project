import os
import uuid
from playsound import playsound
from google.cloud import texttospeech

def speak_text(text, language_code="en-US", voice_name="en-US-Studio-O"):
    # Initialize the client
    tts_client = texttospeech.TextToSpeechClient()

    # Prepare the text input
    input_text = texttospeech.SynthesisInput(text=text)

    # Set the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    # Debug info: show which voice is being used
    print(f"🔊 Speaking with voice: {voice_name}")

    # Set the audio format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = tts_client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config
    )

    # 🔧 Create temp folder for audio output
    temp_dir = "temp_audio"
    os.makedirs(temp_dir, exist_ok=True)

    # 🎧 Save the audio to a unique temporary file
    filename = os.path.join(temp_dir, f"output_{uuid.uuid4().hex}.mp3")
    with open(filename, "wb") as out:
        out.write(response.audio_content)

    # ▶️ Play and then clean up
    try:
        playsound(filename)  # Wait until audio finishes
    finally:
        os.remove(filename)  # Clean up after playback
