import { useState } from "react";
import { Button, Input, Message } from "semantic-ui-react";
import { getCountryInfoApi } from "../api/soap";
import { useAuth } from "../hooks/useAuth";

// Consume el endpoint de Django que a su vez llama al servicio SOAP con zeep
export function SoapWidget() {
  const { auth } = useAuth();
  const [code, setCode] = useState("MX");
  const [country, setCountry] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const search = async () => {
    setLoading(true);
    setError("");
    try {
      setCountry(await getCountryInfoApi(auth.token, code));
    } catch (err) {
      setCountry(null);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="widget" data-testid="soap-widget">
      <h3>País (servicio SOAP vía Django)</h3>
      <div className="widget__row">
        <Input
          fluid
          maxLength={2}
          placeholder="Código ISO (MX, US, ES...)"
          value={code}
          onChange={(e) => setCode(e.target.value.toUpperCase())}
          onKeyDown={(e) => e.key === "Enter" && search()}
        />
        <Button primary content="Consultar" loading={loading} onClick={search} />
      </div>
      {error && <Message negative content={error} />}
      {country && (
        <ul className="widget__list">
          <li><b>País:</b> {country.name}</li>
          <li><b>Capital:</b> {country.capital}</li>
          <li><b>Moneda:</b> {country.currency}</li>
          <li><b>Tel.:</b> +{country.phone_code}</li>
          <li><b>Idiomas:</b> {country.languages?.join(", ")}</li>
        </ul>
      )}
      <p className="widget__source">{country ? country.source : "Fuente: CountryInfoService (SOAP)"}</p>
    </div>
  );
}
