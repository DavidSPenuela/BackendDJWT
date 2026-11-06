import { Link } from "react-router-dom";

export function Error404() {
  return (
    <div style={{ textAlign: "center", padding: "80px 20px" }}>
      <h1>404</h1>
      <p>La página que buscas no existe.</p>
      <Link to="/">Volver al inicio</Link>
    </div>
  );
}
