Livestream AI Agent
This project creates an AI co-host for live streams. It listens to the host via microphone, passes transcriptions to an AI (Anthropic Claude), generates voice responses (Google TTS), and optionally integrates with Twitch chat.

Architecture
Server: A FastAPI application that handles Twitch bot integration, calls the Anthropic API to generate intelligent responses, and generates audio using Google Text-to-Speech.
Client: A local Python script that captures microphone input, transcribes it using Google Speech-to-Text, sends the text to the server, and plays the audio responses locally.
Setup Instructions
1. Prerequisites
Python 3.10+
A Google Cloud Project with the Speech-to-Text API and Text-to-Speech API enabled.
An Anthropic API Key.
A Twitch OAuth Token.
System dependencies for pyaudio (e.g. sudo apt-get install portaudio19-dev on Linux, or brew install portaudio on macOS).
2. Installation
Clone the repository:
git clone <repo-url>
cd livestream-agent
Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate
Install dependencies:
pip install -r requirements.txt
3. Configuration
Create a .env file by copying the example:
cp .env.example .env
Fill in the .env file with your credentials:
TWITCH_TOKEN & TWITCH_CLIENT_ID
ANTHROPIC_API_KEY
GOOGLE_APPLICATION_CREDENTIALS (Absolute path to your Google Cloud service account JSON key)
Edit config.yaml to customize the agent's personality, moderation rules, and Twitch channel.
4. Running the Application
Start the Server:

# From the project root with the venv active
python -m server.main
The server will start on http://127.0.0.1:8000 and the Twitch bot will join your channel.

Start the Client:

# In a new terminal, from the project root with the venv active
python -m client.main
The client will start listening to your microphone. When you stop speaking, it sends the transcript to the server and plays the AI's response.
