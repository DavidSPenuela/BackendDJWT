import { useEffect, useState } from "react";
import { Dropdown, Loader, Message } from "semantic-ui-react";
import { CITIES, describeWeather, getCurrentWeather } from "../api/weather";

// Widget de la API de terceros (Open-Meteo) consumida con fetch
export function WeatherWidget() {
  const [cityKey, setCityKey] = useState(CITIES[0].key);
  const [weather, setWeather] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const controller = new AbortController();
    const city = CITIES.find((c) => c.key === cityKey);
    setLoading(true);
    setError("");
    getCurrentWeather(city, controller.signal)
      .then((data) => setWeather(data))
      .catch((err) => {
        if (err.name !== "AbortError") setError(err.message);
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [cityKey]);

  return (
    <div className="widget" data-testid="weather-widget">
      <h3>Clima actual (API de terceros)</h3>
      <div className="widget__row">
        <Dropdown
          selection
          fluid
          value={cityKey}
          options={CITIES.map((c) => ({ key: c.key, value: c.key, text: c.name }))}
          onChange={(_, data) => setCityKey(data.value)}
        />
      </div>
      {loading && <Loader active inline="centered" />}
      {error && <Message negative content={error} />}
      {!loading && !error && weather && (
        <>
          <p className="widget__big">{weather.temperature_2m} °C</p>
          <ul className="widget__list">
            <li>Condición: {describeWeather(weather.weather_code)}</li>
            <li>Humedad: {weather.relative_humidity_2m} %</li>
            <li>Viento: {weather.wind_speed_10m} km/h</li>
          </ul>
        </>
      )}
      <p className="widget__source">Fuente: Open-Meteo (api.open-meteo.com)</p>
    </div>
  );
}
