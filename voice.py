import threading
import asyncio
import edge_tts
import io
import pygame

pygame.mixer.init(frequency=22050)

def speak(text):
    threading.Thread(target=_speak_thread, args=(text,), daemon=True).start()

def _speak_thread(text):
    asyncio.run(_speak_async(text))

async def _speak_async(text):
    communicate = edge_tts.Communicate(text, voice="en-US-AndrewNeural", rate="+30%")
    
    audio_buffer = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])
    
    audio_buffer.seek(0)
    pygame.mixer.music.load(audio_buffer)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)