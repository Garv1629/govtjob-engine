import urllib.request
import json

BOT_TOKEN = "8934752999:AAFjyAQffdzCaWN5mEXnUy_K7Roe2QH338s"
CHAT_ID = "2128933074"

text = """👋 *GovtJob AI Agent Command Center Connected!*

Hello Garv! Your AI Agent Telegram Bot is now 100% active and connected to your backend engine.

*Available Remote Control Commands:*
• `/start` - Launch Command Center
• `/jobs` - Discovered SSC, UPSC & Railway notifications
• `/profile` - Candidate readiness & qualification score
• `/documents` - Document Vault status
• `/health` - System live telemetry report
• `/help` - Full command list"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = json.dumps({
    "chat_id": CHAT_ID,
    "text": text,
    "parse_mode": "Markdown"
}).encode('utf-8')

req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode())
        if res.get("ok"):
            print("SUCCESS: Telegram message delivered to Garv!")
        else:
            print("Telegram API error:", res)
except Exception as e:
    print("Execution error:", str(e))
