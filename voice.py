from elevenlabs import generate, play, set_api_key
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

set_api_key(os.getenv("elevenlabs_apikey"))

def get_voices(input):
    '''getting voices'''

    audio = generate(
    text=input,
    voice="Josh",
    model="eleven_monolingual_v1"
    )
    print(audio)
    # play(audio)
    return(audio)

