import whisper
import requests
from bs4 import BeautifulSoup

def from_audio(path: str) -> str:
    model = whisper.load_model("base")
    return model.transcribe(path)["text"]

def from_text(path: str) -> str:
    return open(path).read()

def from_url(url: str) -> str:
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    return " ".join(p.text for p in soup.find_all("p"))

def from_whatsapp(path: str) -> str:
    lines = open(path).readlines()
    # strip timestamps, keep message text only
    return "\n".join(
        l.split("] ")[-1] for l in lines if "] " in l
    )