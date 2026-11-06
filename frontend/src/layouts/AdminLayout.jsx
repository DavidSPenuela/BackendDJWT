import { Navigate } from "react-router-dom";
import { Button } from "semantic-ui-react";
import { useAuth } from "../hooks/useAuth";

// Layout protegido: sin sesión redirige a /login
export function AdminLayout({ children }) {
  const { auth, logout } = useAuth();
  if (!auth) return <Navigate to="/login" replace />;

  return (
    <div className="admin-layout">
      <div className="admin-layout__bar">
        <span>Biblioteca Universitaria</span>
        <Button size="small" basic inverted content="Cerrar sesión" onClick={logout} />
      </div>
      <div className="admin-layout__content">{children}</div>
    </div>
  );
}
