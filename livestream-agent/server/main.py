from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uvicorn
import asyncio
from typing import Optional
import os

from server.config import HOST, PORT
from server.agent import Agent
from server.tts import TTSManager
from server.twitch_bot import StreamBot

app = FastAPI()

agent = Agent()
tts_manager = TTSManager()
twitch_bot = None

class HostMessage(BaseModel):
    text: str

async def ai_pipeline(user: str, message: str, is_host: bool):
    """
    Handles passing the message to AI, generating TTS, and optionally replying in Twitch chat.
    """
    # 1. Get AI Response
    ai_response = agent.process_message(user, message, is_host)
    if not ai_response:
        return
        
    print(f"[AI]: {ai_response}")

    # 2. Generate Audio
    # In a real setup, we might stream this back over websockets. 
    # For MVP, we'll save it to a file that the client can download or just generate locally.
    # To keep it simple for the MVP, the server generates the file in a known path.
    audio_file = f"response_{os.urandom(4).hex()}.mp3"
    tts_manager.synthesize(ai_response, output_file=f"server/{audio_file}")
    
    # 3. (Optional) Send text response back to Twitch Chat
    # Note: For MVP, maybe we just have it speak, or we send to chat. Let's do both.
    if twitch_bot and twitch_bot.connected_channels:
        channel = twitch_bot.connected_channels[0]
        await channel.send(ai_response)
        
    return ai_response, audio_file


@app.post("/api/host_message")
async def receive_host_message(msg: HostMessage, background_tasks: BackgroundTasks):
    """
    Endpoint for the local client to send host transcriptions.
    """
    # Run the pipeline in the background so we don't block the STT client
    background_tasks.add_task(ai_pipeline, "Host", msg.text, True)
    return {"status": "processing"}

# Endpoint to check if audio is ready / get latest audio? 
# For MVP, a cleaner approach is WebSockets, but to keep it simple HTTP polling or returning the audio directly works.
# Let's change the pipeline to return audio directly if called by the host.

@app.post("/api/host_message_sync")
async def receive_host_message_sync(msg: HostMessage):
    """
    Synchronous endpoint that waits for AI and TTS, returning the audio file path.
    """
    ai_response, audio_file = await ai_pipeline("Host", msg.text, is_host=True)
    return {"text": ai_response, "audio_file": audio_file}


async def start_twitch_bot():
    global twitch_bot
    # The callback just triggers the pipeline
    async def callback(user, message, is_host):
        await ai_pipeline(user, message, is_host)
        
    twitch_bot = StreamBot(message_callback=callback)
    await twitch_bot.start()


@app.on_event("startup")
async def startup_event():
    # Start Twitch bot in the background
    asyncio.create_task(start_twitch_bot())

if __name__ == "__main__":
    uvicorn.run("server.main:app", host=HOST, port=PORT, reload=True)
