import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from dotenv import load_dotenv
from ollama_client import generate_ollama_response, generate_ollama_response_with_context
from tts_stream import tts_audio_bytes, generate_image

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins='*')

# Global context for LangChain
latest_whiteboard_snapshot = None

@app.route('/')
def index():
    return "SocketIO server is running."

# Irrelevant, for logging connections.
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    send('You are connected!')

# Again, logging when disconnected.
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Irrelevant, boilerplate, does nothing.
@socketio.on('message')
def handle_message(msg):
    print('Received message: ' + msg)
    send('Echo: ' + msg)

# This event generates a text response then sends it as speech.
@socketio.on('generate_response')
def handle_generate_response(prompt):
    print('Received prompt for Ollama:', prompt)
    try:
        global latest_whiteboard_snapshot
        context = latest_whiteboard_snapshot if latest_whiteboard_snapshot else None

        # Generate diagram
        # diagram_code = generate_image(prompt['text'])
        # print("Diagram generated: " + diagram_code)
        # socketio.emit('viz_generated', diagram_code)

        # Generate AI response
        response = generate_ollama_response_with_context(
            'Your role is a teacher. Output the following prompt response informally: ' + prompt,
            context=context
        )

        emit("model_response", {'type': 'ollama_response', 'data': response})
        sid = request.sid
        # Crucial to start this background task - triggers the "send tts" event, so as soon as a text response is generated
        # you stream speech to the client.
        socketio.start_background_task(send_tts_audio_to_client, response, sid)
    except Exception as e:
        print('Error:', e)
        emit("model_error", {'type': 'ollama_error', 'data': str(e)})


# This event generates a text-only response.
@socketio.on('text_response')
def handle_text_response(prompt):
    print('--- Received text_response event ---')
    print('Input prompt:', prompt)
    try:
        global latest_whiteboard_snapshot
        context = latest_whiteboard_snapshot if latest_whiteboard_snapshot else None

        # Generate AI response
        response = generate_ollama_response_with_context(
            'Your role is a teacher. Output the following prompt response informally: ' + prompt,
            context=context
        )

        print('Generated AI Response:', response)
        print('--- Emitting text_model_response ---')
        emit("text_model_response", {'type': 'ollama_response', 'data': response})
    except Exception as e:
        print('Error in text_response handler:', e)
        emit("model_error", {'type': 'ollama_error', 'data': str(e)})


# Send complete TTS audio to the client. Process the text into speech (in bytes) and then stream that to the client.
def send_tts_audio_to_client(text, sid):
    audio_bytes = tts_audio_bytes(text)
    socketio.emit('tts_audio', audio_bytes, to=sid)

# This event is responsible for taking a base64 image uri and then setting that to a global context variable
@socketio.on('whiteboard_snapshot')
def handle_whiteboard_snapshot(image_b64):
    global latest_whiteboard_snapshot
    latest_whiteboard_snapshot = image_b64
    print('Received whiteboard snapshot (base64, length):', len(image_b64))
    send({'type': 'whiteboard_ack', 'data': 'Snapshot received and added to context.'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=2323)