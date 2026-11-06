import { useState, useEffect, createContext } from "react";
import { setToken, getToken, removeToken } from "../api/token";
import { useUser } from "../hooks/useUser";

// 1. Crear el contexto
export const AuthContext = createContext({
  auth: undefined, // undefined = aún no sabemos | null = sin sesión | {token, me} = con sesión
  login: async () => null,
  logout: () => null,
});

// 2. Crear el provider
export function AuthProvider({ children }) {
  const [auth, setAuth] = useState(undefined);
  const { getMe } = useUser();

  // Al cargar la app se recupera la sesión guardada (persistencia tras recargar)
  useEffect(() => {
    const token = getToken();
    if (!token) {
      setAuth(null);
    } else {
      login(token).catch(() => setAuth(null));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const login = async (token) => {
    setToken(token);
    try {
      const me = await getMe(token);
      setAuth({ token, me });
    } catch (error) {
      // Token inválido o vencido: se limpia para no quedar en un estado a medias
      removeToken();
      setAuth(null);
      throw error;
    }
  };

  const logout = () => {
    removeToken();
    setAuth(null);
  };

  // Evita el "flash" de la pantalla de login mientras se valida el token guardado
  if (auth === undefined) return null;

  return (
    <AuthContext.Provider value={{ auth, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
