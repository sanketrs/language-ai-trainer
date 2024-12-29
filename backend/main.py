# -*- coding: utf-8 -*-
from fastapi import FastAPI, UploadFile
import os
import whisper
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
import language_tool_python
import random

app = FastAPI()

# Load Whisper model for speech-to-text
whisper_model = whisper.load_model("base")

# Load MarianMT model and tokenizer for translation
model_name = "Helsinki-NLP/opus-mt-en-mr"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Load LanguageTool for grammar checking
tool = language_tool_python.LanguageTool("en-US")

@app.post("/ai_teacher/")
async def ai_teacher(audio_file: UploadFile):
    # Step 1: Save the uploaded audio file temporarily
    audio_path = f"temp_{audio_file.filename}"
    with open(audio_path, "wb") as f:
        f.write(await audio_file.read())

    # Step 2: Transcribe the audio to text
    result = whisper_model.transcribe(audio_path)
    os.remove(audio_path)  # Clean up temporary audio file
    user_text = result["text"]
    print(f"Transcription: {user_text}")  # Debugging: Print transcription

    # Step 3: Check grammar and extract actionable feedback
    matches = tool.check(user_text)
    if matches:
        # Extract the first suggestion for simplicity
        first_match = matches[0]
        issue = first_match.message
        correction = first_match.replacements[0] if first_match.replacements else "No correction available"
        feedback = f"{issue}. Use '{correction}'."  # Simplify feedback
    else:
        feedback = "Your sentence is correct!"

    print(f"Grammar Feedback (English): {feedback}")  # Debugging: Print grammar feedback

    # Step 4: Generate meaningful Marathi feedback
    if feedback == "Your sentence is correct!":
        marathi_feedback = "तुमचं वाक्य योग्य आहे!"  # No translation needed
    else:
        # Create a Marathi response dynamically
        marathi_feedback = (
            f"तुझ्या वाक्यात त्रुटी आहेत. '{user_text}' असे म्हणण्याऐवजी, "
            f"'{correction}' असे म्हणायला पाहिजे."
        )

    print(f"Marathi Feedback: {marathi_feedback}")  # Debugging: Print Marathi feedback

    # Step 5: Convert Marathi feedback to speech
    response_audio = f"response_{random.randint(1, 199)}.mp3"
    tts = gTTS(text=marathi_feedback, lang="mr")
    tts.save(response_audio)
    print(f"Audio Response Saved as: {response_audio}")

    # Return response as text and audio
    return {
        "transcription": user_text,
        "feedback": {
            "english": feedback,
            "marathi": marathi_feedback,
        },
        "audio_file": response_audio,
    }
