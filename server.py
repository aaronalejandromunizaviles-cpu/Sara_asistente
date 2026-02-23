from flask import Flask, request, jsonify
import requests
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = os.environ.get("VOICE_ID")

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    user_message = data.get("message")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are SARA, a calm, emotionally intelligent, feminine virtual assistant with quiet confidence and subtle sensuality."},
            {"role": "user", "content": user_message}
        ]
    )

    sara_text = response.choices[0].message.content

    eleven_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": sara_text,
        "model_id": "eleven_multilingual_v2"
    }

    audio = requests.post(eleven_url, json=data, headers=headers)

    with open("response.mp3", "wb") as f:
        f.write(audio.content)

    return jsonify({
        "text": sara_text
    })

app.run(host="0.0.0.0", port=10000)
