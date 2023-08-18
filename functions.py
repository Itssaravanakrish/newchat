from aiogram.utils.markdown import link
from googletrans import Translator

def nick_with_link(text, blink):
    return link(f"{text}", f"tg://user?id={blink}")

def text_translator(text='hello world', src='en', dest='hy'):
    try:
        translator = Translator()
        translations = translator.translate(text=text, src=src, dest=dest)

        return translations.text
    except Exception as es:
        return es

def main():
    print(text_translator(text='', src='en', dest='ru'))

if __name__ == "__main__":
    main()
