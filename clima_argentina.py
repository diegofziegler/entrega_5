import json
import urllib.request
from datetime import datetime

# Coordenadas aproximadas de capitales de provincias de Argentina
provincias = {
    "Buenos Aires": {"lat": -34.6037, "lon": -58.3816},
    "Catamarca": {"lat": -28.4696, "lon": -65.7795},
    "Chaco": {"lat": -27.4278, "lon": -59.0243},
    "Chubut": {"lat": -43.3002, "lon": -65.1023},
    "Córdoba": {"lat": -31.4201, "lon": -64.1888},
    "Corrientes": {"lat": -27.4692, "lon": -58.8306},
    "Entre Ríos": {"lat": -31.7333, "lon": -60.5293},
    "Formosa": {"lat": -26.1775, "lon": -58.1781},
    "Jujuy": {"lat": -24.1858, "lon": -65.2995},
    "La Pampa": {"lat": -36.6167, "lon": -64.2833},
    "La Rioja": {"lat": -29.4131, "lon": -66.8558},
    "Mendoza": {"lat": -32.8895, "lon": -68.8458},
    "Misiones": {"lat": -27.3621, "lon": -55.9008},
    "Neuquén": {"lat": -38.9516, "lon": -68.0591},
    "Río Negro": {"lat": -40.8135, "lon": -62.9967},
    "Salta": {"lat": -24.7859, "lon": -65.4117},
    "San Juan": {"lat": -31.5375, "lon": -68.5364},
    "San Luis": {"lat": -33.2950, "lon": -66.3356},
    "Santa Cruz": {"lat": -51.6226, "lon": -69.2181},
    "Santa Fe": {"lat": -31.6333, "lon": -60.7000},
    "Santiago del Estero": {"lat": -27.7951, "lon": -64.2615},
    "Tierra del Fuego": {"lat": -54.8019, "lon": -68.3030},
    "Tucumán": {"lat": -26.8083, "lon": -65.2176},
    "Ciudad Autónoma de Buenos Aires": {"lat": -34.6037, "lon": -58.3816}
}

def consultar_clima(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,weather_code,wind_speed_10m"
        f"&timezone=America%2FArgentina%2FBuenos_Aires"
    )
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode())

def interpretar_clima(weather_code):
    # https://open-meteo.com/en/docs/weather-api
    tiene_sol = weather_code in [0, 1, 2, 3]
    esta_nublado = weather_code in [3, 45, 48] or (51 <= weather_code <= 99)
    va_llover = (51 <= weather_code <= 67) or (80 <= weather_code <= 99)
    return tiene_sol, esta_nublado, va_llover

resultado = []

for provincia, coords in provincias.items():
    data = consultar_clima(coords["lat"], coords["lon"])
    hourly = data.get("hourly", {})
    temps = hourly.get("temperature_2m", [])
    weather_codes = hourly.get("weather_code", [])
    winds = hourly.get("wind_speed_10m", [])

    # Próximas 24 horas
    now = datetime.now()
    current_hour = now.hour
    horas_a_considerar = min(24, len(temps) - current_hour)
    if horas_a_considerar <= 0:
        horas_a_considerar = 24
        current_hour = 0

    temps_24h = temps[current_hour:current_hour+horas_a_considerar]
    codes_24h = weather_codes[current_hour:current_hour+horas_a_considerar]
    winds_24h = winds[current_hour:current_hour+horas_a_considerar]

    temp_min = min(temps_24h)
    temp_max = max(temps_24h)

    va_llover = any((51 <= c <= 67) or (80 <= c <= 99) for c in codes_24h)
    esta_nublado = any(c in [3, 45, 48] or (51 <= c <= 99) for c in codes_24h)
    hay_sol = any(c in [0, 1, 2, 3] for c in codes_24h)
    hay_viento = any(w > 15 for w in winds_24h)  # >15 km/h

    resultado.append({
        "provincia": provincia,
        "temp_min": round(temp_min, 1),
        "temp_max": round(temp_max, 1),
        "va_llover": va_llover,
        "esta_nublado": esta_nublado,
        "hay_sol": hay_sol,
        "hay_viento": hay_viento
    })

print(json.dumps(resultado, indent=2, ensure_ascii=False))