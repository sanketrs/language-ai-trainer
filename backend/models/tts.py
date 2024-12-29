from gtts import gTTS

def text_to_speech(text, lang="mr"):
    file_path = "response.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(file_path)
    return file_path
