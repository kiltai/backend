import numpy as np
import io
import os
from scipy.io import wavfile
from openai import OpenAI

# TODO: Here, it was using this thing called Bark. Idk what it is, cursor generated it. Switch to some other API.
def tts_audio_bytes(text):
    # implement this, wont work otherwise
    # goal is to use some tts library to convert text into WAV or some other file format bytes. ask cursor for help.

# TODO: This was for generating diagrams. No point in the current project scope.
def generate_image(prompt, model="gpt-image-1", size="1024x1024"):
    print(prompt)
    client = OpenAI()
    try:
        response = client.images.generate(
            model=model,
            prompt="Generate a diagram to aid in explaining the following question, do not add a title to the diagram: " + prompt,
            size=size,
            quality="standard",
            n=1
        )
        return response.data[0].url
    except Exception as e:
        print(e)