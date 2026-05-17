import requests
import pygame
import threading
import time
import os

from client.config import SERVER_URL
from client.stt import listen_and_transcribe

def play_audio(file_path):
    """
    Plays an MP3 file using pygame.
    """
    if not os.path.exists(file_path):
        print(f"Audio file not found: {file_path}")
        return

    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

def handle_transcript(transcript):
    """
    Sends the transcribed text to the server.
    """
    if not transcript.strip():
        return

    try:
        response = requests.post(f"{SERVER_URL}/api/host_message_sync", json={"text": transcript})
        if response.status_code == 200:
            data = response.json()
            audio_file = data.get("audio_file")
            if audio_file:
                # In this MVP, the server outputs the file locally relative to where the server runs.
                # If running on the same machine, the client can just read it.
                # A more robust approach downloads the file from an endpoint, but this works for local MVP.
                server_audio_path = os.path.join("server", os.path.basename(audio_file))
                
                # Check if it exists in the server folder (if running from root)
                if os.path.exists(server_audio_path):
                    play_audio(server_audio_path)
                    
                    # Cleanup
                    try:
                        os.remove(server_audio_path)
                    except:
                        pass
                else:
                    print(f"Could not find audio file at {server_audio_path}")
        else:
            print(f"Server error: {response.status_code}")
    except Exception as e:
        print(f"Failed to communicate with server: {e}")

def main():
    print("Starting Client...")
    
    # Optional: wait for server to be up
    try:
        requests.get(SERVER_URL)
    except:
        print(f"Warning: Could not connect to server at {SERVER_URL}. Make sure it is running.")

    # Start listening to microphone. This will block.
    try:
        listen_and_transcribe(handle_transcript)
    except KeyboardInterrupt:
        print("\nStopping client.")

if __name__ == "__main__":
    main()
