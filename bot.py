import os
from flask import Flask, request
from groq import Groq
import requests as req

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)
app = Flask(__name__)

def send_message(chat_id, text):
    req.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
             json={"chat_id": chat_id, "text": text})

@app.route("/")
def home():
    return "Jamiebot is running!"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text == "/start":
            send_message(chat_id, "👋 Hi! I'm an AI assistant. Ask me anything!")
        else:
            send_message(chat_id, "🤔 Thinking...")
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": text}
                ],
                model="llama-3.3-70b-versatile",
            )
            send_message(chat_id, response.choices[0].message.content)
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
