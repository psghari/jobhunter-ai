import requests
import os

def send_telegram_alert(job):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    user_id = os.getenv("TELEGRAM_USER_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    text = f"""*Job Match Alert 🚨*

*Title:* {job.get("title")}
*Company:* {job.get("company")}
*Location:* {job.get("location", "N/A")}
*Score:* {job.get("score", "N/A")}
*Verdict:* {job.get("verdict", "N/A")}

[Apply Here]({job.get("url")})

_Cover Letter:_  
{job.get("cover_letter", "Not available")}

_Source:* {job.get("source", "Unknown")}
"""

    data = {
        "chat_id": user_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    requests.post(url, data=data)
