import numpy as np
from bark import SAMPLE_RATE, generate_audio
import io
import os
from scipy.io import wavfile
from openai import OpenAI

def tts_audio_bytes(text):
    # Generate audio array using Bark
    audio_array = generate_audio(text)
    # Save to a BytesIO buffer as WAV using scipy
    buf = io.BytesIO()
    wavfile.write(buf, SAMPLE_RATE, audio_array)
    buf.seek(0)
    return buf.read()

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