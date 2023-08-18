from aiogram.utils.markdown import link
from googletrans import Translator

def nick_with_link(text, blink):
    return link(f"{text}", f"tg://user?id={blink}")
