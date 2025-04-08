from gtts import gTTS

def speak_response(text, path="response.mp3"):
    tts = gTTS(text)
    tts.save(path)
    return path
