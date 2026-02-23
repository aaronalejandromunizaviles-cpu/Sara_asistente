from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def home():
    return """
    <h2>SARA está viva</h2>
    <input id='msg' placeholder='Habla con SARA'>
    <button onclick='enviar()'>Enviar</button>
    <p id='respuesta'></p>

    <script>
    async function enviar() {
        let mensaje = document.getElementById("msg").value;

        let res = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: mensaje})
        });

        if (res.ok) {
            let data = await res.json();
            document.getElementById("respuesta").innerText = data.reply;
        } else {
            document.getElementById("respuesta").innerText = "Error al conectar con SARA.";
        }
    }
    </script>
    """

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "Eres SARA, una asistente femenina, inteligente, calmada, natural, humana y profesional."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    else:
        return jsonify({"reply": "Hubo un error al contactar a SARA."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
