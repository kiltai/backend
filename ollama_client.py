import requests

OLLAMA_API_URL = 'http://localhost:11434/api/generate'

def generate_ollama_response(prompt, model='mathstral'):
    payload = {
        'model': model,
        'prompt': prompt,
        'stream': False
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()
    return response.json().get('response', '') 