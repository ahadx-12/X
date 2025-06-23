import os
import requests


DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = os.getenv(
    "DEEPSEEK_URL",
    "https://api.deepseek.com/v1/chat/completions",
)


def generate_email(
    name: str,
    firm: str,
    city: str,
    template_path: str = "templates/lawyer_email.txt",
) -> str:
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    prompt = (
        template.replace("{{name}}", name)
        .replace("{{firm}}", firm)
        .replace("{{city}}", city)
    )

    payload = {
        "model": "deepseek-chat",
        "temperature": 0.7,
        "max_tokens": 300,
        "messages": [
            {
                "role": "system",
                "content": "Rewrite the following email to sound natural and personalized.",
            },
            {"role": "user", "content": prompt},
        ],
    }
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
    resp = requests.post(DEEPSEEK_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()
