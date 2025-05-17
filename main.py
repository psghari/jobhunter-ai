from scraper.indeed_scraper import scrape_indeed
from scraper.naukri_scraper import scrape_naukri
from ai.gemini_analyzer import bulk_analyze_jobs
from ai.gpt_verdict import escalate_job
from notify.telegram_push import send_telegram_alert

def gather_all_jobs():
    jobs = []
    print("🔍 Scraping Indeed...")
    jobs += scrape_indeed()

    print("🔍 Scraping Naukri...")
    jobs += scrape_naukri()

    print(f"✅ Gathered {len(jobs)} job listings.")
    return jobs

def main():
    print("🚀 Starting job hunt automation...")

    jobs = gather_all_jobs()
    print("🤖 Analyzing jobs via Gemini...")
    flagged_jobs = bulk_analyze_jobs(jobs)

    print(f"✅ {len(flagged_jobs)} jobs flagged for deep analysis.")

    for job in flagged_jobs:
        print(f"🎯 Escalating job: {job['title']} at {job['company']}")
        enriched = escalate_job(job)
        if enriched:
            print(f"📬 Sending alert to Telegram: {enriched['title']} ({enriched.get('score', '?')}/10)")
            send_telegram_alert(enriched)

    print("✅ All done for this run.")

if __name__ == "__main__":
    main()
