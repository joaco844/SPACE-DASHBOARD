---
name: Space Dashboard Project
description: NASA Open APIs dashboard project context, design system, and work division
type: project
originSessionId: 12ea6e4f-1b47-4acd-9c7c-133e23f9f9bc
---
# Space Dashboard

Panel web con datos diarios del espacio usando NASA Open APIs.

**Módulos:**
- APOD (Astronomy Picture of the Day) — imagen del día + explicación
- NeoWs — asteroides cercanos hoy
- Mars — fotos de Marte en tiempo real
- EPIC — imagen actual de la Tierra

**Stack:** Django (back) + Python (back) + HTML/CSS/JS (front)

**División de trabajo:**
- Usuario: backend (Python/Django), terminal, deploy
- Claude: frontend, UI, templates, assets, config de herramientas

**Design system:** Apple-inspired (ver diseño.md en la carpeta del proyecto)
- Tiles full-bleed alternando dark (#272729) y light (#f5f5f7)
- Accent único: Action Blue #0066cc
- Sin gradientes, sin sombras en cards (solo en imágenes)
- SF Pro / system-ui / Inter como fallback
- Body 17px/400, headlines 600 con tracking negativo
- Border radius: pill para CTAs, 18px para cards, 0 para tiles

**Why:** Proyecto personal/portfolio de dashboard espacial.
**How to apply:** Respetar estrictamente el design system al construir templates y componentes frontend.

**Feature pro pendiente:** Notificaciones diarias de asteroides (mockear cuando haya implementación real).
