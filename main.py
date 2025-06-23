import os
import csv
import time
from scraper import scrape_contacts
from gpt_generator import generate_email
from email_sender import send_email


CITIES = [
    "Toronto",
    "Ottawa",
    "Hamilton",
    "London",
    "Windsor",
]


def load_contacts(path: str = "lawyers.csv") -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_sent(path: str = "sent.csv") -> set[str]:
    if not os.path.exists(path):
        return set()
    with open(path, newline="", encoding="utf-8") as f:
        return {row["email"] for row in csv.DictReader(f, fieldnames=["email"])}


def append_sent(email: str, path: str = "sent.csv") -> None:
    exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["email"])
        if not exists:
            writer.writeheader()
        writer.writerow({"email": email})


def main() -> None:
    if not os.path.exists("lawyers.csv"):
        scrape_contacts(CITIES)
    contacts = load_contacts()
    sent = load_sent()
    for contact in contacts:
        email = contact["email"]
        if email in sent:
            continue
        body = generate_email(contact["name"], contact["firm"], contact["city"])
        send_email(email, body)
        append_sent(email)
        time.sleep(20)


if __name__ == "__main__":
    main()
