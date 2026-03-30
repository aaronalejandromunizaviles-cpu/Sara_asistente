from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route("/")
def home():
    return """
    <h2>SARA está viva</h2>
    <input id='msg' placeholder='Escribe algo'>
    <button onclick='enviar()'>Enviar</button>
    <p id='respuesta'></p>

    <script>
async function enviar() {
    try {
        let mensaje = document.getElementById("msg").value;

        let res = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({message: mensaje})
        });

        let data = await res.json();

        document.getElementById("respuesta").innerText = data.reply;

    } catch (error) {
        document.getElementById("respuesta").innerText = "Error en el envío";
        console.error(error);
    }
}
</script>
    """

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://render.com",
        "X-Title": "SARA"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "Eres SARA, una asistente inteligente, calmada y natural."},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

   if response.status_code == 200:
    reply = response.json()["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})
else:
    error = response.text
    print("ERROR OPENROUTER:", error)
    return jsonify({"reply": error}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
