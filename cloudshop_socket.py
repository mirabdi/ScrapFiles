import websocket
import json
import threading
import time

# Authentication payloads
AUTH_SIMPLE = {
    "company_id": "57c09c3b3ce7d59d048b46c9",
    "user_id": "57c09c3b3ce7d59d048b46c8",
    "type": "auth",
    "status": True
}

AUTH_BY_TOKEN = {
    "command": "auth_by_token",
    "user": "57c09c3b3ce7d59d048b46c8",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiNTdjMDljM2IzY2U3ZDU5ZDA0OGI0NmM4In0.zeapBbGkNoyqyyrVHFTz53wnhojZYJc86XFfmz47koQ"
}

def on_message(ws, message):
    print("🔔 Message:", message)
    try:
        data = json.loads(message)
        if data.get("type") == "ping":
            ws.send(json.dumps({"type": "pong"}))
            print("↔️ Sent pong")
    except Exception as e:
        print("⚠️ Parse error:", e)

def on_error(ws, error):
    print("❌ Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("🔒 Closed")

def on_open(ws):
    print("✅ Connected, authenticating...")
    # Send auth payload (choose the one that works)
    ws.send(json.dumps(AUTH_BY_TOKEN))
    # ws.send(json.dumps(AUTH_SIMPLE))

url = "wss://socket.cloudshop.ru/"

headers = {
    "Origin": "https://web.cloudshop.ru",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
}

ws = websocket.WebSocketApp(
    url,
    header=[f"{k}: {v}" for k, v in headers.items()],
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
    on_open=on_open,
)

# Run in a thread so it auto-reconnects
def run():
    ws.run_forever()

threading.Thread(target=run).start()
