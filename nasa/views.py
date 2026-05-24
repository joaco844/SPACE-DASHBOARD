import os
import json
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
    # Eliminamos el parámetro '?sol=1000' de la URL base porque 
    # es mejor pasarlo ordenadamente en el diccionario de params.
    urls = [
        "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos",
        "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos",
    ]

    for url in urls:
        try:
            # Configuramos los parámetros limpitos
            params = {"api_key": NASA_API_KEY}
            if "latest_photos" not in url:
                params["sol"] = 1000  # Solo agregamos el sol si es el endpoint general

            r = requests.get(url, params=params, timeout=10)

            # Si no es 200, imprimimos el error y saltamos a la siguiente URL
            if r.status_code != 200:
                print(f"NASA API error {r.status_code} en {url}")
                continue

            # Tu validación de HTML es perfecta. Si la NASA se cae (como ahora), 
            # saltará aquí en lugar de romper el programa al intentar hacer .json()
            if "application/json" not in r.headers.get("Content-Type", ""):
                print(f"NASA devolvió HTML (posible caída del servidor) en {url}")
                continue

            data = r.json()
            
            # Buscamos las fotos en cualquiera de las dos llaves posibles
            fotos = data.get("latest_photos") or data.get("photos") or []
            
            if fotos:
                return fotos[:12]
            else:
                print(f"No se encontraron fotos en la respuesta de {url}")

        except requests.exceptions.RequestException as e:
            # Es mejor capturar errores específicos de requests
            print(f"Error de conexión en {url}: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    # Si ambas URLs fallaron, retornamos la lista vacía para que tu app no se rompa
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


def get_co2():
    try:
        r = requests.get(
            "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.csv",
            timeout=10
        )
        r.raise_for_status()

        lines = r.text.strip().split("\n")
        data = []

        for line in lines:
            if line.startswith("#") or not line.strip():
                continue

            parts = line.split(",")

            # Saltear header u otras filas inválidas
            if not parts[0].strip().isdigit():
                continue

            if len(parts) >= 2:
                data.append({
                    "year": int(parts[0]),
                    "mean": float(parts[1])
                })

        return data

    except Exception as e:
        print(f"Error fetching CO₂ data: {e}")
        return []


def dashboard(request):
    return render(request, "dashboard.html", {
        "apod": get_apod(),
        "asteroides": get_asteroides(),
        "fotos_marte": get_fotos_marte(),
        "epic": get_epic(),
    })


def get_eonet():
    try:
        r = requests.get(
            "https://eonet.gsfc.nasa.gov/api/v3/events",
            params={"status": "open", "limit": 50, "days": 30},
            timeout=10
        )
        r.raise_for_status()
        events = r.json().get("events", [])
        # Extraemos solo lo necesario para el template
        clean = []
        for e in events:
            geo = e.get("geometry", [])
            if not geo:
                continue
            last = geo[-1]
            coords = last.get("coordinates", [])
            if len(coords) < 2:
                continue
            cat = e.get("categories", [{}])[0]
            clean.append({
                "id":       e["id"],
                "title":    e["title"],
                "cat_id":   cat.get("id", ""),
                "cat_title":cat.get("title", ""),
                "date":     last.get("date", "")[:10],
                "lon":      coords[0],
                "lat":      coords[1],
                "link":     e.get("link", ""),
                "closed":   e.get("closed"),
            })
        return clean
    except Exception as e:
        print(f"Error fetching EONET data: {e}")
        return []


def earth(request):
    return render(request, "earth.html", {
        "co2": get_co2(),
    })


def eonet(request):
    events = get_eonet()
    # Categorías únicas presentes en los eventos actuales
    seen = {}
    for e in events:
        if e["cat_id"] not in seen:
            seen[e["cat_id"]] = e["cat_title"]
    categories = list(seen.items())
    return render(request, "eonet.html", {
        "events":      events,
        "events_json": json.dumps(events),
        "categories":  categories,
    })

