from flask import Flask, request, jsonify
from pydub import AudioSegment
import whisper
import os

app = Flask(__name__)

# Load the Whisper model
model = whisper.load_model("base")

def speed_up_audio(input_path, output_path, speed=1.3):
    """Speed up audio playback."""
    audio = AudioSegment.from_file(input_path)
    faster_audio = audio.speedup(playback_speed=speed)
    faster_audio.export(output_path, format="wav")

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

        # Transcribe the sped-up audio with English language specified
        result = model.transcribe(sped_up_audio_path, language='en')
    finally:
        # Delete the temporary files after processing
        os.remove(audio_path)
        os.remove(sped_up_audio_path)

    return jsonify({"transcription": result["text"]})

if __name__ == '__main__':
    app.run(debug=True)
