import routesClient from "./routes.client";
import routesAdmin from "./routes.admin";
import routesCommon from "./routes.common";

// La ruta comodín "*" (404) debe ir al final
export const routes = [...routesAdmin, ...routesClient, ...routesCommon];
