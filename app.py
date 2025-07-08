from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import eventlet
from ollama_client import generate_ollama_response, generate_ollama_response_with_context

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins='*')

# Global context for LangChain
latest_whiteboard_snapshot = None

@app.route('/')
def index():
    return "SocketIO server is running."

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    send('You are connected!')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(msg):
    print('Received message: ' + msg)
    send('Echo: ' + msg)

@socketio.on('generate_response')
def handle_generate_response(prompt):
    print('Received prompt for Ollama:', prompt)
    try:
        global latest_whiteboard_snapshot
        context = latest_whiteboard_snapshot if latest_whiteboard_snapshot else None
        response1 = generate_ollama_response('Describe the following image for a model that will use it to answer a question', images=[latest_whiteboard_snapshot])
        response2 = generate_ollama_response_with_context('Output the following prompt response informally as if you were an eighth-grade teacher:' + prompt, context=response1)
        print('Ollama response:', response1)
        emit("model_response", {'type': 'ollama_response', 'data': response1})
        emit("draw_visual", {'type': 'ollama_response', 'data': response2})
    except Exception as e:
        print('Error:', e)
        emit("model_error", {'type': 'ollama_error', 'data': str(e)})

@socketio.on('whiteboard_snapshot')
def handle_whiteboard_snapshot(image_b64):
    global latest_whiteboard_snapshot
    latest_whiteboard_snapshot = image_b64
    print('Received whiteboard snapshot (base64, length):', len(image_b64))
    send({'type': 'whiteboard_ack', 'data': 'Snapshot received and added to context.'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=2323)