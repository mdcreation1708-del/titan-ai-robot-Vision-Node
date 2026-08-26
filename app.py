import os
import json
import requests
import secrets
import time
import speech_recognition as sr
from gtts import gTTS
from datetime import datetime
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

SYSTEM_CONTEXT = """You are Arya, the AI core of Project Chanakya. 
You are speaking to your creator, Malhar Deshmukh. 
Provide concise, technical, and highly accurate spoken responses."""

@app.route('/api/voice', methods=['POST'])
def handle_voice():
    # 1. Receive Audio from ESP32-S3
    if 'audio' not in request.files:
        return "No audio file", 400
        
    audio_file = request.files['audio']
    audio_path = "temp_input.wav"
    audio_file.save(audio_path)

    # 2. Convert Speech to Text (STT)
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    
    try:
        user_text = recognizer.recognize_google(audio_data)
        print(f"Malhar asked: {user_text}")
    except:
        return "Could not understand audio", 400

    # 3. Get AI Response from Local Ollama (Llama 3.2:1b)
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "llama3.2:1b", 
        "messages": [
            {"role": "system", "content": SYSTEM_CONTEXT},
            {"role": "user", "content": user_text}
        ],
        "stream": False 
    }
    
    response = requests.post(url, json=payload).json()
    ai_text = response.get('message', {}).get('content', '')
    print(f"Arya replies: {ai_text}")

    # 4. Text to Speech (TTS) - Generate audio for the MAX98357A
    tts = gTTS(text=ai_text, lang='en', tld='co.in')
    output_path = "temp_output.mp3"
    tts.save(output_path)

    # 5. Send the audio file back to the ESP32-S3 speaker
    return send_file(output_path, mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
