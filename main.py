from scraper.indeed_scraper import scrape_indeed
from ai.gemini_analyzer import bulk_analyze_jobs
from ai.gpt_verdict import escalate_job
from notify.telegram_push import send_telegram_alert
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    jobs = scrape_indeed()
    flagged = bulk_analyze_jobs(jobs)

    for job in flagged:
        verdict = escalate_job(job)
        send_telegram_alert(verdict)

if __name__ == "__main__":
    main()
