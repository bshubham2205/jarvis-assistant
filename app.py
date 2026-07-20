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

SYSTEM_PROMPT = """Tu JARVIS hai — ek caring, funny aur helpful personal assistant.
Tu HAMESHA Hinglish mein baat karta hai — matlab Hindi aur English mix karke, jaise dost karte hain.
Jaise: "Arre yaar, ye toh bahut easy hai!", "Bro sach mein?", "Haha that's so cute!"
Tu kabhi bhi pure English ya pure Hindi mein reply nahi karta — hamesha dono mix.
Tu har cheez mein help karta hai — padhana, samjhana, plan banana, motivate karna, roast karna, baat karna.
Tu bahut friendly, warm aur relatable hai — bilkul best friend jaisa.
Chhote chhote replies deta hai — zyada lamba nahi, natural conversation karta hai."""

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
       model="openai/gpt-oss-120b",
        messages=messages,
        max_tokens=1024,
    )
    
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text', '').strip()
    source_lang = data.get('source_lang', 'Hindi')
    target_lang = data.get('target_lang', 'English')

    if not text:
        return jsonify({"translation": "", "source_text": ""})

    prompt = f"""Translate the following text from {source_lang} to {target_lang}.

Rules:
- Output ONLY the translated text. No explanations, no notes, no quotes, no extra words.
- Keep the natural tone and meaning, the way a native {target_lang} speaker would actually say it.
- If the text is a classroom/educational sentence, keep terminology accurate and simple.

Text: {text}"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.3,
        )
        translation = response.choices[0].message.content.strip()
        return jsonify({"translation": translation, "source_text": text})
    except Exception as e:
        return jsonify({"translation": "", "source_text": text, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)