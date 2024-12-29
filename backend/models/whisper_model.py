import whisper

# Load Whisper model
model = whisper.load_model("base")

def speech_to_text(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]
