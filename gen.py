import os
import json
from datetime import datetime
import pytz

"""
Script único: agrupa todos los lugares (manuales y del JSON masivo) por su GMT **dinámico**
-------------------------------------------------------------------------------
• Mantiene la lista manual de lugares y el `timezone_map` original.
• Carga `datalugares_completo.json` si existe y aplanará:
    - Sección `estructurado` → recorre continente → zona → países → lugares.
    - Lista plana con claves `Lugar`, `CC`, `TZ`.
• Cada entrada debe tener **o** una zona horaria (`TZ`) **o** un string de offset (`+05:30`, `-02:00`, etc.).
• Genera **un único** `temp/datalugares.json` con la forma:
    {
        "GMT+1": [ {"Lugar": "...", "CC": "...", "TZ": "..."}, ... ],
        "GMT-5": [ ... ],
        ...
    }
"""

# ------------------------------------------------------------------
# 1) Lista manual (igual que tu script original)
# ------------------------------------------------------------------
places_manual = [
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
]

# ------------------------------------------------------------------
# 2) Mapeo de zona horaria para la lista manual
# ------------------------------------------------------------------
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
    "🇺🇸 (Howland)": "Pacific/Howland",
}

# ------------------------------------------------------------------
# 3) Helper functions
# ------------------------------------------------------------------

def _format_gmt(hours: float) -> str:
    """Devuelve 'GMT+9' o 'GMT+5.5'"""
    if hours.is_integer():
        return f"GMT{int(hours):+d}"
    return f"GMT{hours:+.1f}".replace(".0", "")


def _offset_str_to_hours(offset: str) -> float:
    """Convierte '+05:45' → 5.75, '-02:30' → -2.5"""
    sign = 1 if offset.startswith('+') else -1
    hh, mm = offset[1:].split(':')
    return sign * (int(hh) + int(mm) / 60)


# ------------------------------------------------------------------
# 4) Construir lista unificada (manual + JSON masivo)
# ------------------------------------------------------------------
combined_places: list[dict] = []

# A) manual con su TZ
for p in places_manual:
    tz_manual = timezone_map.get(p["Lugar"])
    combined_places.append({
        **p,
        "TZ": tz_manual,
        "src": "manual",
    })

# B) cargar JSON masivo si existe
if os.path.exists("datalugares_completo.json"):
    with open("datalugares_completo.json", "r", encoding="utf-8") as f:
        raw_json = json.load(f)

    def _add_place(obj: dict):
        combined_places.append({
            "Lugar": obj.get("Lugar", obj.get("j", "?")),
            "CC": obj.get("CC", obj.get("l", "")),
            "TZ": obj.get("TZ"),
            "offset_str": obj.get("GMT_offset") or obj.get("d") or obj.get("offset") or obj.get("d1"),
            "src": "ext",
        })

    # Caso 1: lista plana
    if isinstance(raw_json, list):
        for item in raw_json:
            _add_place(item)

    # Caso 2: dict con claves
    elif isinstance(raw_json, dict):
        # 2a) 'gmt_auto' ya viene agrupado → des-agrupamos
        if isinstance(raw_json.get("gmt_auto"), dict):
            for gmt, lst in raw_json["gmt_auto"].items():
                for it in lst:
                    it["offset_str"] = gmt.replace("GMT", "+") if gmt != "GMT" else "+00:00"
                    _add_place(it)

        # 2b) 'estructurado'
        if isinstance(raw_json.get("estructurado"), list):
            for cont in raw_json["estructurado"]:
                for zona in cont.get("c", []):
                    offset_raw = zona.get("d")  # +14:00, -02:30, etc.
                    for pais in zona.get("f", []):
                        for loc in pais.get("i", []):
                            _add_place({
                                "Lugar": f"{loc['j']} ({pais['h']})",
                                "CC": loc["l"],
                                "TZ": None,
                                "GMT_offset": offset_raw,
                            })

# ------------------------------------------------------------------
# 5) Agrupar por GMT actual
# ------------------------------------------------------------------
result: dict[str, list[dict]] = {}
for pl in combined_places:
    gmt_key = "GMT Unknown"

    # A) si tiene TZ computamos con pytz
    if pl.get("TZ"):
        try:
            now = datetime.now(pytz.timezone(pl["TZ"]))
            gmt_key = _format_gmt(now.utcoffset().total_seconds() / 3600)
        except Exception:
            pass
    # B) si no tiene TZ pero hay offset_str
    elif pl.get("offset_str"):
        try:
            gmt_key = _format_gmt(_offset_str_to_hours(pl["offset_str"]))
        except Exception:
            pass

    result.setdefault(gmt_key, []).append(pl)

# ------------------------------------------------------------------
# 6) Guardar archivo final
# ------------------------------------------------------------------
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)
OUT_FILE = os.path.join(TEMP_DIR, "datalugares.json")
with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"✅ Datos agrupados por GMT guardados en {OUT_FILE}")