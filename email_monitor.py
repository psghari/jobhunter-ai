import imaplib
import email
from email.header import decode_header
import os
from ai.gemini_analyzer import bulk_analyze_jobs
from ai.gpt_verdict import escalate_job
from notify.telegram_push import send_telegram_alert
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_FOLDER = os.getenv("EMAIL_FOLDER", "INBOX")
ALERT_SENDERS = os.getenv("ALERT_SENDERS", "").split(",")

def fetch_job_emails():
    print("📬 Connecting to mailbox...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    mail.select(EMAIL_FOLDER)

    result, data = mail.search(None, '(UNSEEN)')
    email_ids = data[0].split()
    print(f"🧾 Found {len(email_ids)} new emails")

    job_entries = []

    for eid in email_ids:
        res, msg_data = mail.fetch(eid, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                sender = msg.get("From")

                if any(sender_id in sender for sender_id in ALERT_SENDERS):
                    subject = decode_header(msg["Subject"])[0][0]
                    subject = subject.decode() if isinstance(subject, bytes) else subject

                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()

                    job_entries.append({
                        "title": subject,
                        "company": "Unknown",
                        "summary": body,
                        "url": "Not Found",
                        "source": "Email"
                    })

    mail.logout()
    return job_entries

def run_email_monitor():
    print("📨 Checking for job alert emails...")
    jobs = fetch_job_emails()
    print(f"🧠 {len(jobs)} jobs found in inbox.")

    flagged = bulk_analyze_jobs(jobs)
    for job in flagged:
        enriched = escalate_job(job)
        if enriched:
            send_telegram_alert(enriched)

if __name__ == "__main__":
    run_email_monitor()
