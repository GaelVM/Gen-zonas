import os
from datetime import datetime
import pytz
import json

# Data inicial
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
]

# Función para calcular GMT actual basado en zona horaria
def get_gmt_offset(location, lugar):
    try:
        # Manejo manual para Howland
        if lugar == "🇺🇸 (Howland)":
            return "GMT-12"
        tz = pytz.timezone(location)
        now = datetime.now(tz)
        offset = now.utcoffset()
        hours = offset.total_seconds() / 3600
        return f"GMT{int(hours):+d}"
    except Exception as e:
        return "GMT Unknown"

# Mapeo de zonas horarias (personalizar según necesidad)
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
    "🇺🇸 (Howland)": "Pacific/Howland"  # Zona horaria correcta para Howland
}

# Agrupar lugares por GMT actual
grouped_by_gmt = {}
for place in places:
    location = place["Lugar"]
    timezone = timezone_map.get(location, None)
    gmt = get_gmt_offset(timezone, location) if timezone else "GMT Unknown"
    if gmt not in grouped_by_gmt:
        grouped_by_gmt[gmt] = []
    grouped_by_gmt[gmt].append(place)

# Definir la carpeta temporal
temp_folder = "temp"

# Verificar si la carpeta temporal ya existe, y si no, crearla
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

# Definir la ruta completa del archivo JSON en la carpeta temporal
json_file_path = os.path.join(temp_folder, "datalugares.json")

# Guardar el diccionario en un archivo JSON en la carpeta temporal
with open(json_file_path, "w", encoding="utf-8") as json_file:
    json.dump(grouped_by_gmt, json_file, ensure_ascii=False, indent=2)

print(f"Datos guardados en {json_file_path}")