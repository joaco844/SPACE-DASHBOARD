# Space Dashboard

Panel web con datos diarios del espacio usando NASA Open APIs y JPL. Construido con Django + Python en el backend y HTML/CSS/JS puro en el frontend.

## Secciones

| Ruta | Descripción |
|---|---|
| `/` | **Space** — APOD, asteroides NeoWs, fotos Mars Rover, imagen EPIC |
| `/earth/` | **Climate Change** — mapa GIBS, gráfico CO₂ histórico, stats de cambio climático |
| `/earth/eonet/` | **EONET** — eventos naturales activos (incendios, tormentas, volcanes) en mapa |
| `/gallery/` | **Space Gallery** — buscador de imágenes y videos NASA, favoritos, playlists |
| `/mission/` | **Mission Planner** — calculadora de trayectorias, ventanas de lanzamiento a Marte, simulador |
| `/solar/` | **Solar System** — simulador 3D con Three.js, órbitas de Kepler, cometas desde JPL |

## Stack

- **Backend:** Python 3.13 · Django 6
- **Frontend:** HTML · CSS · JavaScript (vanilla)
- **3D:** Three.js (CDN, sin npm)
- **Mapas:** Leaflet · NASA GIBS WMS
- **Gráficos:** Chart.js
- **APIs:** NASA Open APIs · JPL Small Body Database · NOAA CO₂ · EONET

## Setup local

```bash
git clone https://github.com/tu-usuario/space-dashboard.git
cd space-dashboard

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Crear un archivo `.env` en la raíz del proyecto:

```
NASA_API_KEY=tu_api_key_de_api.nasa.gov
SECRET_KEY=un_string_secreto_largo
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Conseguí tu NASA API key gratis en [api.nasa.gov](https://api.nasa.gov).

```bash
python manage.py runserver
```

Abrí `http://localhost:8000`.

## Deploy (Render)

El proyecto incluye `render.yaml` y `build.sh` listos para usar.

1. Subí el repo a GitHub
2. Creá un nuevo **Web Service** en [render.com](https://render.com) conectando el repo
3. Configurá los comandos:
   - Build: `./build.sh`
   - Start: `gunicorn space_dashboard.wsgi:application`
4. Agregá las variables de entorno en el dashboard:

| Variable | Valor |
|---|---|
| `NASA_API_KEY` | tu key |
| `SECRET_KEY` | string random largo |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com` |

Render hace auto-deploy en cada `git push` a main.

## Variables de entorno

| Variable | Descripción |
|---|---|
| `NASA_API_KEY` | API key de api.nasa.gov (requerida) |
| `SECRET_KEY` | Django secret key (requerida) |
| `DEBUG` | `True` en local, `False` en producción |
| `ALLOWED_HOSTS` | Hosts permitidos separados por coma |
