# server.py
from flask import Flask, jsonify, request
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio
import json
import time
import threading

app = Flask(__name__)
sessions = {}
tasks = {}

# Конфигурация
with open('config.json') as f:
    config = json.load(f)

async def auth_user(api_id, api_hash, phone, code=None):
    client = TelegramClient(StringSession(), api_id, api_hash)
    await client.connect()
    
    if not await client.is_user_authorized():
        if code:
            await client.sign_in(phone, code)
        else:
            await client.send_code_request(phone)
    
    return client.session.save()

@app.route('/api/send_code', methods=['POST'])
def send_code():
    data = request.json
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        session = loop.run_until_complete(auth_user(
            data['api_id'], 
            data['api_hash'], 
            data['phone']
        ))
        return jsonify({'status': 'code_sent'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/confirm_code', methods=['POST'])
def confirm_code():
    data = request.json
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        session = loop.run_until_complete(auth_user(
            data['api_id'], 
            data['api_hash'], 
            data['phone'],
            data['code']
        ))
        # Сохраняем сессию
        with open('sessions.json', 'a') as f:
            f.write(json.dumps({
                'session': session,
                'api_id': data['api_id'],
                'api_hash': data['api_hash'],
                'phone': data['phone']
            }) + '\n')
        return jsonify({'status': 'authorized'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(port=5000)