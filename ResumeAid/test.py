import requests
import os

elevenlabs_key = "sk_ef30fc46d296dc894f49a0d9176156ff815f0fe0dc1b47a5"
voice_id = "iP95p4xoKVk53GoZ742B"
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

headers = {
    "accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "sk_ef30fc46d296dc894f49a0d9176156ff815f0fe0dc1b47a5"
}

data = {
    "text": "This is a test.",
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
}

response = requests.post(url, json=data, headers=headers)
if response.status_code == 200:
    with open("output.mp3", "wb") as f:
        f.write(response.content)
    print("Text-to-speech conversion successful. Audio saved to output.mp3")
else:
    print(f"Text-to-speech conversion failed with status code {response.status_code}: {response.text}")
