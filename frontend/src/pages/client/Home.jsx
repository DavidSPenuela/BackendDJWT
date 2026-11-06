import { Link } from "react-router-dom";
import { Button } from "semantic-ui-react";
import { useAuth } from "../../hooks/useAuth";

export function Home() {
  const { auth } = useAuth();

  return (
    <div className="home">
      <h1>Biblioteca Universitaria</h1>
      <p>Consulta tu cuenta, el clima del día y datos de países desde un solo lugar.</p>
      <div>
        {auth ? (
          <Button as={Link} to="/dashboard" size="large" primary content="Ir al Dashboard" />
        ) : (
          <>
            <Button as={Link} to="/login" size="large" primary content="Iniciar sesión" />
            <Button as={Link} to="/register" size="large" content="Registrarse" />
          </>
        )}
      </div>
    </div>
  );
}
