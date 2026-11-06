import { useAuth } from "../../hooks/useAuth";
import { WeatherWidget } from "../../components/WeatherWidget";
import { SoapWidget } from "../../components/SoapWidget";

export function Dashboard() {
  const { auth } = useAuth();
  const user = auth.me;
  const fullName = `${user.first_name} ${user.last_name}`.trim() || user.username;

  return (
    <div className="dashboard">
      <div className="dashboard__welcome">
        <h2>Bienvenido, {fullName}</h2>
        <p>
          {user.email}
          {user.matricula ? ` · Matrícula ${user.matricula}` : ""}
        </p>
      </div>
      <div className="dashboard__grid">
        <WeatherWidget />
        <SoapWidget />
      </div>
    </div>
  );
}
