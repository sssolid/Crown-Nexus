# backend/scripts/auto_translate.py
import json
import os
import requests
from pathlib import Path
import polib

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_LOCALE = "en"
TARGET_LOCALES = ["es", "fr", "de"]

# LibreTranslate endpoint - use a public instance or self-host
LIBRETRANSLATE_URL = "https://libretranslate.com/translate"

def translate_text(text, target_language):
    """Translate text using LibreTranslate."""
    payload = {
        "q": text,
        "source": SOURCE_LOCALE,
        "target": target_language,
        "format": "text"
    }
    
    try:
        response = requests.post(LIBRETRANSLATE_URL, json=payload)
        if response.status_code == 200:
            return response.json()["translatedText"]
        else:
            print(f"Translation error: {response.text}")
            return text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def translate_json_file(source_file, target_file, target_locale):
    """Translate a JSON file to the target locale."""
    with open(source_file, 'r', encoding='utf-8') as f:
        source_data = json.load(f)
    
    # Recursive function to translate nested objects
    def translate_obj(obj):
        if isinstance(obj, str):
            return translate_text(obj, target_locale)
        elif isinstance(obj, dict):
            return {k: translate_obj(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [translate_obj(item) for item in obj]
        else:
            return obj
    
    translated_data = translate_obj(source_data)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)
    
    print(f"Translated {source_file} to {target_file}")

def translate_po_file(source_file, target_file, target_locale):
    """Translate a PO file to the target locale."""
    source_po = polib.pofile(source_file)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    
    # Create a new PO file for the target locale
    target_po = polib.POFile()
    target_po.metadata = source_po.metadata.copy()
    target_po.metadata['Language'] = target_locale
    
    # Translate each entry
    for entry in source_po:
        translated_entry = polib.POEntry(
            msgid=entry.msgid,
            msgstr=translate_text(entry.msgid, target_locale),
            occurrences=entry.occurrences,
            comment=entry.comment,
            flags=entry.flags
        )
        target_po.append(translated_entry)
    
    target_po.save(target_file)
    print(f"Translated {source_file} to {target_file}")

def main():
    # Translate frontend JSON files
    frontend_dir = os.path.join(BASE_DIR, "..", "frontend", "src", "i18n", "locales")
    source_json = os.path.join(frontend_dir, f"{SOURCE_LOCALE}.json")
    
    if os.path.exists(source_json):
        for locale in TARGET_LOCALES:
            target_json = os.path.join(frontend_dir, f"{locale}.json")
            translate_json_file(source_json, target_json, locale)
    
    # Translate backend PO files
    backend_locale_dir = os.path.join(BASE_DIR, "app", "i18n", "locales")
    source_po = os.path.join(backend_locale_dir, SOURCE_LOCALE, "LC_MESSAGES", "messages.po")
    
    if os.path.exists(source_po):
        for locale in TARGET_LOCALES:
            target_po_dir = os.path.join(backend_locale_dir, locale, "LC_MESSAGES")
            os.makedirs(target_po_dir, exist_ok=True)
            target_po = os.path.join(target_po_dir, "messages.po")
            translate_po_file(source_po, target_po, locale)

if __name__ == "__main__":
    main()
