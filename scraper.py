import csv
import os
import re
import requests
from bs4 import BeautifulSoup

SERP_API_KEY = os.getenv("SERPAPI_KEY")
SERP_URL = "https://serpapi.com/search"


def fetch_lawyers(city: str):
    params = {
        "engine": "google_maps",
        "q": "personal injury lawyer",
        "type": "search",
        "google_domain": "google.ca",
        "hl": "en",
        "gl": "ca",
        "location": f"{city}, Ontario",
        "api_key": SERP_API_KEY,
    }
    resp = requests.get(SERP_URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("places_results", [])


def scrape_email(url: str) -> str | None:
    try:
        resp = requests.get(url, timeout=10)
    except Exception:
        return None
    if not resp.ok:
        return None
    soup = BeautifulSoup(resp.text, "html.parser")
    email_re = re.compile(r"[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+")
    match = email_re.search(soup.get_text())
    if match:
        return match.group(0)
    return None


def scrape_contacts(cities: list[str], outfile: str = "lawyers.csv") -> None:
    fieldnames = ["name", "firm", "email", "city", "website"]
    with open(outfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for city in cities:
            for place in fetch_lawyers(city):
                website = place.get("website")
                if not website:
                    continue
                email = scrape_email(website)
                if not email:
                    continue
                writer.writerow(
                    {
                        "name": place.get("title", ""),
                        "firm": place.get("title", ""),
                        "email": email,
                        "city": city,
                        "website": website,
                    }
                )
