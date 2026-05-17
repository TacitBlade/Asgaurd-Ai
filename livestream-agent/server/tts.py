from google.cloud import texttospeech
from server.config import config
import os

class TTSManager:
    def __init__(self):
        # We assume GOOGLE_APPLICATION_CREDENTIALS is set in env
        try:
            self.client = texttospeech.TextToSpeechClient()
        except Exception as e:
            print(f"Failed to initialize Google TTS client: {e}")
            self.client = None
            
        tts_cfg = config.get("tts", {})
        self.language_code = tts_cfg.get("language_code", "en-US")
        self.voice_name = tts_cfg.get("voice_name", "en-US-Journey-F")

    def synthesize(self, text, output_file="output.mp3"):
        if not self.client:
            print("TTS client not initialized.")
            return None

        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code=self.language_code,
            name=self.voice_name
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        try:
            response = self.client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            with open(output_file, "wb") as out:
                out.write(response.audio_content)
                print(f"Audio content written to file '{output_file}'")
            return output_file
        except Exception as e:
            print(f"Error synthesizing speech: {e}")
            return None
