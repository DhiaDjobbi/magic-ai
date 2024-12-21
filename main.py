from flask import Flask, request, jsonify
from pydub import AudioSegment
import whisper
import os

app = Flask(__name__)

# Load the Whisper model
model = whisper.load_model("base")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded audio file temporarily
    audio_path = f"temp_{file.filename}"
    file.save(audio_path)

    try:
        # Transcribe the audio with English language specified
        result = model.transcribe(audio_path, language='en')
    finally:
        # Delete the temporary file after processing
        os.remove(audio_path)

    return jsonify({"transcription": result["text"]})

if __name__ == '__main__':
    app.run(debug=True)