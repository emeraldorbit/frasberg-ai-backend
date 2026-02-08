"""Sofia Core Slack Bot Integration"""

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests
import os

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

SOFIA_BASE_URL = os.environ.get("SOFIA_BASE_URL", "http://localhost:8000")

@app.message("sofia")
def handle_sofia_mention(message, say):
    """Handle mentions of Sofia"""
    text = message['text'].replace('sofia', '').strip()
    
    try:
        # Generate response using Sofia
        response = requests.post(
            f"{SOFIA_BASE_URL}/api/v3/ai/llm/generate",
            json={"prompt": text}
        )
        
        if response.status_code == 200:
            data = response.json()
            say(f"🤖 {data['response']}\n\n_Powered by Sofia Core v5.0.0_")
        else:
            say("❌ Sorry, I couldn't process that request.")
    except Exception as e:
        say(f"❌ Error: {str(e)}")

@app.command("/sofia-health")
def handle_health_command(ack, say):
    """Check Sofia health"""
    ack()
    
    try:
        response = requests.get(f"{SOFIA_BASE_URL}/health/detailed")
        if response.status_code == 200:
            data = response.json()
            say(f"✅ Sofia Core is {data['overall_status']}\nVersion: {data['version']}")
        else:
            say("❌ Health check failed")
    except Exception as e:
        say(f"❌ Cannot connect to Sofia: {e}")

@app.command("/sofia-speak")
def handle_speak_command(ack, respond, command):
    """Generate speech"""
    ack()
    
    text = command['text']
    
    try:
        response = requests.post(
            f"{SOFIA_BASE_URL}/api/v2/voice/tts/synthesize",
            json={"text": text, "language": "en"}
        )
        
        if response.status_code == 200:
            data = response.json()
            respond(f"🔊 Speech generated!\nDuration: {data['duration_seconds']}s\nAudio: {data['audio_url']}")
        else:
            respond("❌ Speech synthesis failed")
    except Exception as e:
        respond(f"❌ Error: {e}")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
