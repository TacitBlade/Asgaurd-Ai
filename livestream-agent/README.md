# Livestream AI Agent

This project creates an AI co-host for live streams. It listens to the host via microphone, passes transcriptions to an AI (Anthropic Claude), generates voice responses (Google TTS), and optionally integrates with Twitch chat.

## Architecture

* **Server:** A FastAPI application that handles Twitch bot integration, calls the Anthropic API to generate intelligent responses, and generates audio using Google Text-to-Speech.
* **Client:** A local Python script that captures microphone input, transcribes it using Google Speech-to-Text, sends the text to the server, and plays the audio responses locally.

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- A Google Cloud Project with the **Speech-to-Text API** and **Text-to-Speech API** enabled.
- An [Anthropic API Key](https://console.anthropic.com/).
- A [Twitch OAuth Token](https://twitchapps.com/tmi/).
- System dependencies for `pyaudio` (e.g. `sudo apt-get install portaudio19-dev` on Linux, or `brew install portaudio` on macOS).

### 2. Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd livestream-agent
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration

1. Create a `.env` file by copying the example:
   ```bash
   cp .env.example .env
   ```
2. Fill in the `.env` file with your credentials:
   - `TWITCH_TOKEN` & `TWITCH_CLIENT_ID`
   - `ANTHROPIC_API_KEY`
   - `GOOGLE_APPLICATION_CREDENTIALS` (Absolute path to your Google Cloud service account JSON key)
3. Edit `config.yaml` to customize the agent's personality, moderation rules, and Twitch channel.

### 4. Running the Application

**Start the Server:**
```bash
# From the project root with the venv active
python -m server.main
```
The server will start on `http://127.0.0.1:8000` and the Twitch bot will join your channel.

**Start the Client:**
```bash
# In a new terminal, from the project root with the venv active
python -m client.main
```
The client will start listening to your microphone. When you stop speaking, it sends the transcript to the server and plays the AI's response.
