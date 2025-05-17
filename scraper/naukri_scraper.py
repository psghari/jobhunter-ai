import requests
from bs4 import BeautifulSoup
import time

JOB_TITLES = [
    "Service Delivery Manager", "ITSM Lead", "Problem Manager",
    "Major Incident Manager", "Change Manager", "Knowledge Manager",
    "SIAM Consultant", "IT Operations Manager", "ITIL Process Manager",
    "Service Management Lead", "Infrastructure Delivery Manager", "Application Delivery Manager"
]

LOCATIONS = [
    "Bangalore", "Hyderabad", "Pune", "Chennai", "Noida",
    "Gurgaon", "Coimbatore", "Remote"
]

def scrape_naukri():
    base_url = "https://www.naukri.com/"
    jobs = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for title in JOB_TITLES:
        for location in LOCATIONS:
            search_query = f"{title} jobs in {location}".replace(" ", "-")
            url = f"https://www.naukri.com/{search_query}"
            try:
                resp = requests.get(url, headers=headers)
                soup = BeautifulSoup(resp.text, "html.parser")
                cards = soup.select("article.jobTuple")

                for card in cards:
                    job_title = card.find("a", class_="title").text.strip()
                    job_url = card.find("a", class_="title").get("href")
                    company = card.find("a", class_="subTitle").text.strip() if card.find("a", class_="subTitle") else "N/A"
                    summary = card.find("ul", class_="tags has-description").text.strip() if card.find("ul", class_="tags has-description") else ""

                    jobs.append({
                        "title": job_title,
                        "company": company,
                        "url": job_url,
                        "summary": summary,
                        "search_term": title,
                        "location": location
                    })

                time.sleep(1)  # Avoid rate limit
            except Exception as e:
                print(f"Error scraping Naukri for {title} in {location}: {e}")

    return jobs
