from flask import Flask, render_template
from flask_socketio import SocketIO, send
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
    print('Received prompt for Ollama:', prompt)
    try:
        response = generate_ollama_response(prompt)
        emit({'type': 'ollama_response', 'data': response})
    except Exception as e:
        emit({'type': 'ollama_error', 'data': str(e)})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)