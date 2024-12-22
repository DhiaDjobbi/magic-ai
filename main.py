from flask import Flask, request, jsonify
from pydub import AudioSegment
import os
from faster_whisper import WhisperModel

app = Flask(__name__)

# Load the Faster Whisper model with compute_type="int8"
model = WhisperModel("base", compute_type="int8")

def speed_up_audio(input_path, output_path, speed=1.3):
    """Speed up audio playback."""
    audio = AudioSegment.from_file(input_path)
    faster_audio = audio.speedup(playback_speed=speed)
    faster_audio.export(output_path, format="wav")

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello, World!"

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

    # Path for the sped-up audio file
    sped_up_audio_path = f"sped_up_{file.filename}"

    try:
        # Speed up the audio
        speed_up_audio(audio_path, sped_up_audio_path)

        # Transcribe the sped-up audio in segments
        segments, _ = model.transcribe(sped_up_audio_path, language='en')

        # Combine the transcription text from all segments
        transcription = " ".join(segment.text for segment in segments)
    finally:
        # Delete the temporary files after processing
        os.remove(audio_path)
        os.remove(sped_up_audio_path)

    return jsonify({"transcription": transcription})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
