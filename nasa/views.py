import os
import requests
from datetime import date
from django.shortcuts import render

NASA_API_KEY = os.environ["NASA_API_KEY"]


def get_apod():
    try:
        r = requests.get(
            "https://api.nasa.gov/planetary/apod",
            params={"api_key": NASA_API_KEY},
            timeout=10
        )
        return r.json()
    except Exception:
        return {}


def get_asteroides():
    today = date.today().isoformat()
    try:
        r = requests.get(
            "https://api.nasa.gov/neo/rest/v1/feed",
            params={"start_date": today, "end_date": today, "api_key": NASA_API_KEY},
            timeout=10
        )
        asteroides = r.json().get("near_earth_objects", {}).get(today, [])
        asteroides.sort(key=lambda x: x["is_potentially_hazardous_asteroid"], reverse=True)
        return asteroides
    except Exception:
        return []


def get_fotos_marte():
    urls = [
        "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos",
        "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000",
    ]

    for url in urls:
        try:
            r = requests.get(url, params={"api_key": NASA_API_KEY}, timeout=10)

            if r.status_code != 200:
                print("NASA API error:", r.status_code)
                continue

            if "application/json" not in r.headers.get("Content-Type", ""):
                print("NASA returned HTML instead of JSON")
                continue

            data = r.json()

            fotos = data.get("latest_photos") or data.get("photos") or []
            if fotos:
                return fotos[:12]

        except Exception as e:
            print("Request failed:", e)

    return []
def get_epic():
    try:
        r = requests.get(
            "https://epic.gsfc.nasa.gov/api/natural",
            timeout=10
        )
        return r.json()[:1]
    except Exception:
        return []


def dashboard(request):
    return render(request, "dashboard.html", {
        "apod": get_apod(),
        "asteroides": get_asteroides(),
        "fotos_marte": get_fotos_marte(),
        "epic": get_epic(),
    })