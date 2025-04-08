from googletrans import Translator

def translate_text(text, dest_language="hi"):  # Hindi by default
    translator = Translator()
    translation = translator.translate(text, dest=dest_language)
    return translation.text
