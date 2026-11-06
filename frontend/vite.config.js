import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// El puerto 5173 es el que está permitido en CORS_ALLOWED_ORIGINS del backend
export default defineConfig({
  plugins: [react()],
  server: { port: 5173 },
});
