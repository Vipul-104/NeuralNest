import whisper
import requests
import re
from bs4 import BeautifulSoup

def from_audio(path: str) -> str:
    model = whisper.load_model("base")
    return model.transcribe(path)["text"]

def from_text(path: str) -> str:
    return open(path, encoding="utf-8", errors="ignore").read()

def from_url(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
    return " ".join(p.text for p in soup.find_all("p"))

def from_whatsapp(path: str) -> str:
    """
    Handles both WhatsApp export formats:
    - [DD/MM/YY, HH:MM:SS] Name: message
    - DD/MM/YY, HH:MM - Name: message
    Strips timestamps, sender names, media omitted tags.
    """
    lines = open(path, encoding="utf-8", errors="ignore").readlines()
    messages = []
    # pattern covers both Android and iOS export formats
    pattern = re.compile(
        r"(\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?\s?(?:AM|PM)?\]|\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:AM|PM)?\s-)\s"
    )
    skip_keywords = ["<Media omitted>", "missed voice call",
                     "missed video call", "This message was deleted",
                     "image omitted", "video omitted", "audio omitted",
                     "sticker omitted", "document omitted"]

    for line in lines:
        cleaned = pattern.sub("", line).strip()
        # remove sender name (everything before first colon)
        if ": " in cleaned:
            cleaned = cleaned.split(": ", 1)[-1].strip()
        # skip empty, media, system messages
        if not cleaned:
            continue
        if any(kw.lower() in cleaned.lower() for kw in skip_keywords):
            continue
        if len(cleaned) < 3:
            continue
        messages.append(cleaned)

    return "\n".join(messages)