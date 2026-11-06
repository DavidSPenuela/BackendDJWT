const API_URL = import.meta.env.VITE_BASE_API_URL;

// Convierte {campo: ["error1", ...]} del backend en un texto legible
function flattenErrors(data) {
  if (!data || typeof data !== "object") return "";
  return Object.entries(data)
    .flatMap(([field, msgs]) => [].concat(msgs).map((m) => `${field}: ${m}`))
    .join(" | ");
}

export async function loginApi(formData) {
  let response;
  try {
    response = await fetch(`${API_URL}/api/v1/auth/token/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
  } catch {
    throw new Error("No se pudo conectar con el servidor");
  }
  if (response.status === 401) throw new Error("Correo o contraseña incorrectos");
  if (!response.ok) throw new Error("Error al iniciar sesión");
  return response.json(); // { access, refresh }
}

export async function registerApi(formData) {
  let response;
  try {
    response = await fetch(`${API_URL}/api/v1/auth/register/`, {
      method: "POST",
      headers: { accept: "application/json", "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
  } catch {
    throw new Error("No se pudo conectar con el servidor");
  }
  const data = await response.json().catch(() => ({}));
  if (response.status !== 201) {
    throw new Error(flattenErrors(data) || "No se puede crear el usuario");
  }
  return data;
}

export async function getMeApi(token) {
  const response = await fetch(`${API_URL}/api/v1/auth/me/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  // El manual no revisaba el status: con un token vencido guardaba el JSON de error como "usuario"
  if (!response.ok) throw new Error("Sesión inválida o expirada");
  return response.json();
}
