# Biblioteca Universitaria — Django + React (JWT, API de terceros y SOAP)

Proyecto del RA2 (cierre Unidades 2 y 3). Continúa la Práctica 4: backend Django con JWT, ahora con
frontend en React, una API de terceros y un endpoint que consume un servicio SOAP con `zeep`.

```
backend/    Django + DRF + SimpleJWT + Swagger + zeep
frontend/   React 18 + Vite + Semantic UI + React Router v6 + Formik/Yup
scripts/    capturas.py (genera las capturas de evidencia con Playwright)
evidencia/  capturas del PDF
```

## 1. Backend (terminal 1)

```bash
cd backend
python -m venv venv
./venv/Scripts/activate            # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations users
python manage.py migrate
python manage.py createsuperuser   # opcional
python manage.py test              # opcional: pruebas automáticas
python manage.py runserver         # http://localhost:8000
```

Swagger: http://localhost:8000/swagger/

## 2. Frontend (terminal 2)

```bash
cd frontend
npm install
npm run dev                        # http://localhost:5173
```

El archivo `frontend/.env` apunta al backend (`VITE_BASE_API_URL=http://localhost:8000`).

## 3. Uso

1. Abre http://localhost:5173/register y crea una cuenta.
2. Inicia sesión en `/login`: se guarda el token y se redirige a `/dashboard`.
3. El Dashboard muestra tu nombre (AuthContext), el **clima actual** (API de terceros Open-Meteo, con `fetch`)
   y la **consulta de país por SOAP** (Django → zeep → CountryInfoService).

## Endpoints (prefijo `/api/v1/`)

| Método | Ruta | Descripción | Acceso |
|---|---|---|---|
| POST | `auth/register/` | Registro público de usuarios | Público |
| POST | `auth/token/` | Login (email + password) → `access` y `refresh` | Público |
| POST | `auth/token/refresh/` | Renueva el token de acceso | Público |
| GET | `auth/me/` | Datos del usuario logueado (web service propio protegido) | JWT |
| GET | `soap/country/?code=MX` | Consume el servicio SOAP con zeep | JWT |
| CRUD | `users/` | Administración de usuarios | Admin |

## Capturas automáticas (opcional)

Con ambos servidores corriendo y un usuario creado:

```bash
pip install playwright && playwright install chromium
python scripts/capturas.py correo@ejemplo.com TuContraseña#1
```

## Notas

- El servicio SOAP y la API del clima requieren conexión a internet.
- El token se guarda en `localStorage` (como en el manual); es práctico para la práctica, pero en producción
  convendría una cookie `HttpOnly` por el riesgo de XSS.
