const API_URL = import.meta.env.VITE_BASE_API_URL;

// Llama al endpoint de Django que consume el servicio SOAP con zeep
export async function getCountryInfoApi(token, code) {
  let response;
  try {
    response = await fetch(
      `${API_URL}/api/v1/soap/country/?code=${encodeURIComponent(code)}`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
  } catch {
    throw new Error("No se pudo conectar con el servidor");
  }
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || "Error al consultar el servicio SOAP");
  return data;
}
