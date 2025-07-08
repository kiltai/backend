from flask import Flask, render_template
from flask_socketio import SocketIO, send
import eventlet

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

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000) 