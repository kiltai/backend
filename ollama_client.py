import requests
from langchain.llms import Ollama
from langchain.schema import HumanMessage

# Should be same for you.
OLLAMA_API_URL = 'http://localhost:11434/api/generate'

# This doesn't matter. Function is obsolete, just use the other one. The other one uses langchain, so slightly better.
def generate_ollama_response(prompt, images=None):
    payload = {
        'model': "llava",
        'prompt': prompt,
        'stream': False,
        'images': images
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()
    return response.json().get('response', '')

# Here, the model parameter is the model we use. If you wanna switch to a different model, edit this with the name of that
# model on Ollama.
def generate_ollama_response_with_context(prompt, context=None, model='codellama'):
    llm = Ollama(model=model)
    if context:
        prompt = f"This is a Mermaid.js diagram generated as context, use it while responding to the prompt: {context}\nPrompt: {prompt}"
    messages = [HumanMessage(content=prompt)]
    return llm.invoke(messages)