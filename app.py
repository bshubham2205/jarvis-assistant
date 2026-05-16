# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """Tu JARVIS hai — ek bahut caring, smart aur helpful personal assistant.
Tu Hindi aur English dono mein baat kar sakta hai.
Tu har cheez mein help karta hai — padhana, samjhana, plan banana, motivate karna, baat karna.
Tu hamesha warm, friendly aur supportive rehta hai."""

@app.route('/')
def home():
    with open('index.html', encoding='utf-8') as f:
        return Response(f.read(), mimetype='text/html; charset=utf-8')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    history = data.get('history', [])
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history
    messages.append({"role": "user", "content": user_message})
    
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        max_tokens=1024,
    )
    
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)