#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
import pytz
import json

# ──────────────────────────────────────────────
# 1. Lista de lugares (sin cambios)
# ──────────────────────────────────────────────
places = [
    {"Lugar": "🇬🇧 (London)", "CC": "51.5012,-0.1397"},
    {"Lugar": "🇮🇨 (Las Palmas)", "CC": "28.1287,-15.4516"},
    {"Lugar": "🇪🇸 (Barcelona)", "CC": "41.4043,2.1757"},
    {"Lugar": "🇭🇺 (Budapest)", "CC": "47.5298,19.0515"},
    {"Lugar": "🇭🇷 (Zagreb)", "CC": "45.8104,15.9782"},
    {"Lugar": "🇲🇰 (Skopie)", "CC": "42.0057,21.4212"},
    {"Lugar": "🇱🇧 (Beirut)", "CC": "33.8937,35.4902"},
    {"Lugar": "🇬🇷 (Atenas)", "CC": "37.9726,23.7372"},
    {"Lugar": "🇹🇷 (Izmir)", "CC": "38.4634,27.2163"},
    {"Lugar": "🇦🇪 (Dubai)", "CC": "25.0774,55.1336"},
    {"Lugar": "🇸🇨 (Victoria)", "CC": "-4.6203,55.4526"},
    {"Lugar": "🇹🇲 (Ashgabat)", "CC": "6.9129,79.8612"},
    {"Lugar": "🇧🇹 (Thimphu)", "CC": "27.5004,89.6398"},
    {"Lugar": "🇹🇭 (Bangkok)", "CC": "13.7336,100.4970"},
    {"Lugar": "🇹🇼 (Taipéi)", "CC": "25.0422,121.5067"},
    {"Lugar": "🇨🇳 (Hong Kong)", "CC": "22.2777,114.1620"},
    {"Lugar": "🇯🇵 (Tokio)", "CC": "35.6892,139.6978"},
    {"Lugar": "🇰🇷 (Busan)", "CC": "35.1555,129.0591"},
    {"Lugar": "🇬🇺 (Tamuning)", "CC": "13.5135,144.8057"},
    {"Lugar": "🇦🇺 (Sydney)", "CC": "-33.8630,151.2153"},
    {"Lugar": "🇫🇯 (Suva)", "CC": "-18.1465,178.4245"},
    {"Lugar": "🇳🇿 (Wellington)", "CC": "-41.2824,174.7691"},
    {"Lugar": "🇰🇮 (London)", "CC": "1.9871,-157.4771"},
    {"Lugar": "🇼🇸 (Apia)", "CC": "-13.8313,-171.7664"},
    {"Lugar": "🇨🇻 (Praia)", "CC": "14.9184,-23.5085"},
    {"Lugar": "🇬🇱 (Nuuk)", "CC": "64.1741,-51.7385"},
    {"Lugar": "🇧🇷 (São Paulo)", "CC": "-23.5842,-46.6594"},
    {"Lugar": "🇨🇱 (Santiago)", "CC": "-33.4357,-70.6409"},
    {"Lugar": "🇦🇷 (Buenos Aires)", "CC": "-34.6177,-58.4328"},
    {"Lugar": "🇱🇨 (Castries)", "CC": "14.0107,-60.9887"},
    {"Lugar": "🇺🇸 (NY)", "CC": "40.7828,-73.9653"},
    {"Lugar": "🇳🇫 (Kingston)", "CC": "-29.0569,167.9593"},
    {"Lugar": "🇪🇨 (Quito)", "CC": "-0.1838,-78.4846"},
    {"Lugar": "🇵🇪 (Lima)", "CC": "-12.0627,-77.0362"},
    {"Lugar": "🇺🇸 (Colorado)", "CC": "39.7392,-104.9902"},
    {"Lugar": "🇺🇸 (Nuevo Mexico)", "CC": "35.0851,-106.6499"},
    {"Lugar": "🇺🇸 (Denver)", "CC": "39.7504,-104.9532"},
    {"Lugar": "🇺🇸 (San Francisco)", "CC": "37.8086,-122.4098"},
    {"Lugar": "🇺🇸 (Downtown Anchorage)", "CC": "61.2167,-149.8923"},
    {"Lugar": "🇺🇸 (Honolulu)", "CC": "21.2709,-157.8181"},
    {"Lugar": "🇦🇸 (Pago Pago)", "CC": "-14.2779,-170.6882"},
    {"Lugar": "🇺🇸 (Howland)", "CC": "0.8072,-176.6177"}
]

# ──────────────────────────────────────────────
# 2. Mapeo Lugar → zona horaria de pytz
# ──────────────────────────────────────────────
timezone_map = {
    "🇬🇧 (London)": "Europe/London",
    "🇮🇨 (Las Palmas)": "Atlantic/Canary",
    "🇪🇸 (Barcelona)": "Europe/Madrid",
    "🇭🇺 (Budapest)": "Europe/Budapest",
    "🇭🇷 (Zagreb)": "Europe/Zagreb",
    "🇲🇰 (Skopie)": "Europe/Skopje",
    "🇱🇧 (Beirut)": "Asia/Beirut",
    "🇬🇷 (Atenas)": "Europe/Athens",
    "🇹🇷 (Izmir)": "Europe/Istanbul",
    "🇦🇪 (Dubai)": "Asia/Dubai",
    "🇸🇨 (Victoria)": "Indian/Mahe",
    "🇹🇲 (Ashgabat)": "Asia/Ashgabat",
    "🇧🇹 (Thimphu)": "Asia/Thimphu",
    "🇹🇭 (Bangkok)": "Asia/Bangkok",
    "🇹🇼 (Taipéi)": "Asia/Taipei",
    "🇨🇳 (Hong Kong)": "Asia/Hong_Kong",
    "🇯🇵 (Tokio)": "Asia/Tokyo",
    "🇰🇷 (Busan)": "Asia/Seoul",
    "🇬🇺 (Tamuning)": "Pacific/Guam",
    "🇦🇺 (Sydney)": "Australia/Sydney",
    "🇫🇯 (Suva)": "Pacific/Fiji",
    "🇳🇿 (Wellington)": "Pacific/Auckland",
    "🇰🇮 (London)": "Pacific/Kiritimati",
    "🇼🇸 (Apia)": "Pacific/Apia",
    "🇨🇻 (Praia)": "Atlantic/Cape_Verde",
    "🇬🇱 (Nuuk)": "America/Godthab",
    "🇧🇷 (São Paulo)": "America/Sao_Paulo",
    "🇨🇱 (Santiago)": "America/Santiago",
    "🇦🇷 (Buenos Aires)": "America/Argentina/Buenos_Aires",
    "🇱🇨 (Castries)": "America/St_Lucia",
    "🇺🇸 (NY)": "America/New_York",
    "🇳🇫 (Kingston)": "Pacific/Norfolk",
    "🇪🇨 (Quito)": "America/Guayaquil",
    "🇵🇪 (Lima)": "America/Lima",
    "🇺🇸 (Colorado)": "America/Denver",
    "🇺🇸 (Nuevo Mexico)": "America/Denver",
    "🇺🇸 (Denver)": "America/Denver",
    "🇺🇸 (San Francisco)": "America/Los_Angeles",
    "🇺🇸 (Downtown Anchorage)": "America/Anchorage",
    "🇺🇸 (Honolulu)": "Pacific/Honolulu",
    "🇦🇸 (Pago Pago)": "Pacific/Pago_Pago",
    # Howland no existe en pytz ⇒ lo tratamos aparte
    "🇺🇸 (Howland)": None
}

# ──────────────────────────────────────────────
# 3. Helpers
# ──────────────────────────────────────────────
def calc_gmt_offset(tz_name: str, lugar: str) -> str:
    """Devuelve la cadena 'GMT±X'."""
    # Caso especial Howland (GMT-12)
    if lugar == "🇺🇸 (Howland)":
        return "GMT-12"
    try:
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        offset = now.utcoffset()            # timedelta
        hours = int(offset.total_seconds() // 3600)
        return f"GMT{hours:+d}"
    except Exception:
        return "GMT Unknown"

def local_datetime_str(lugar: str, tz_name: str) -> str:
    """Devuelve fecha+hora local 'YYYY-MM-DD HH:MM' o 'Desconocida'."""
    # Howland: UTC-12 → UTC ahora menos 12 h
    if lugar == "🇺🇸 (Howland)":
        now = datetime.utcnow() - timedelta(hours=12)
        return now.strftime("%Y-%m-%d %H:%M")
    try:
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        return now.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "Desconocida"

# ──────────────────────────────────────────────
# 4. Agrupar por GMT, añadiendo FechaHoraLocal
# ──────────────────────────────────────────────
grouped_by_gmt: dict[str, list[dict]] = {}

for place in places:
    lugar = place["Lugar"]
    tz_name = timezone_map.get(lugar)
    gmt = calc_gmt_offset(tz_name, lugar) if tz_name else "GMT Unknown"
    fecha_hora_local = local_datetime_str(lugar, tz_name)

    entry = {
        "Lugar": lugar,
        "CC": place["CC"],
        "FechaHoraLocal": fecha_hora_local
    }

    grouped_by_gmt.setdefault(gmt, []).append(entry)

# ──────────────────────────────────────────────
# 5. Guardar a JSON en carpeta 'temp'
# ──────────────────────────────────────────────
temp_folder = "temp"
os.makedirs(temp_folder, exist_ok=True)
json_file_path = os.path.join(temp_folder, "datalugares.json")

with open(json_file_path, "w", encoding="utf-8") as fp:
    json.dump(grouped_by_gmt, fp, ensure_ascii=False, indent=2)

print(f"✅ Datos guardados en: {json_file_path}")
