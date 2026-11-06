// API de terceros (gratuita y sin llave): Open-Meteo  https://open-meteo.com
const BASE = "https://api.open-meteo.com/v1/forecast";

export const CITIES = [
  { key: "cdmx", name: "Ciudad de México", lat: 19.4326, lon: -99.1332 },
  { key: "gdl", name: "Guadalajara", lat: 20.6597, lon: -103.3496 },
  { key: "mty", name: "Monterrey", lat: 25.6866, lon: -100.3161 },
  { key: "mid", name: "Mérida", lat: 20.9674, lon: -89.5926 },
  { key: "tij", name: "Tijuana", lat: 32.5149, lon: -117.0382 },
];

// Códigos WMO que devuelve la API
export function describeWeather(code) {
  if (code === 0) return "Despejado";
  if (code === 1) return "Mayormente despejado";
  if (code === 2) return "Parcialmente nublado";
  if (code === 3) return "Nublado";
  if (code === 45 || code === 48) return "Niebla";
  if (code >= 51 && code <= 57) return "Llovizna";
  if (code >= 61 && code <= 67) return "Lluvia";
  if (code >= 71 && code <= 77) return "Nieve";
  if (code >= 80 && code <= 82) return "Chubascos";
  if (code >= 95) return "Tormenta";
  return "Sin descripción";
}

export async function getCurrentWeather({ lat, lon }, signal) {
  const params = new URLSearchParams({
    latitude: lat,
    longitude: lon,
    current: "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
    timezone: "auto",
  });
  const response = await fetch(`${BASE}?${params}`, { signal });
  if (!response.ok) throw new Error("No se pudo obtener el clima");
  const data = await response.json();
  return data.current;
}
