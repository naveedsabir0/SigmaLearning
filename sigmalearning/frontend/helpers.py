from googletrans import Translator
import pandas as pd
from googletrans.client import Translator



translator = Translator()

def translate_text(text, target_lang='fr'):
    try:
        return translator.translate(text, dest=target_lang).text
    except Exception as e:
        return f"Translation error: {str(e)}"

def load_users():
    return pd.read_csv("data/sample_users.csv")  # Simulating database
