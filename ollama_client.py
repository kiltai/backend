import requests
from langchain.llms import Ollama
from langchain.schema import HumanMessage

OLLAMA_API_URL = 'http://localhost:11434/api/generate'

def generate_ollama_response(prompt, model='mathstral', images=None):
    payload = {
        'model': model,
        'prompt': prompt,
        'stream': False,
        'images': images
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()
    return response.json().get('response', '')

def generate_ollama_response_with_context(prompt, context=None, model='mathstral'):
    llm = Ollama(model=model)
    if context:
        prompt = f"Context: {context}\nPrompt: {prompt}"
    messages = [HumanMessage(content=prompt)]
    return llm.invoke(messages) 