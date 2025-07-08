from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import eventlet
from ollama_client import generate_ollama_response

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins='*')

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
    print('Received prompt for Ollama:', 'Output the following prompt response informally as if you were a eight-grade teacher:' + prompt)
    try:
        response = generate_ollama_response('Output the following prompt response informally as if you were a eight-grade teacher:' + prompt)
        print('Ollama response:', response)
        emit("model_response", {'type': 'ollama_response', 'data': response})
    except Exception as e:
        print('Error:', e)
        emit("model_error", {'type': 'ollama_error', 'data': str(e)})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=2323)