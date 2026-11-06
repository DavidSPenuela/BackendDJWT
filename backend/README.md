# API Biblioteca Universitaria (Django + DRF + JWT)

Backend de la Práctica 4, Unidad 3. Gestión de usuarios con login por **email**, campo extra **matrícula**,
autenticación con **JWT** y documentación con **Swagger**.

## Instalación (Windows / PowerShell)

```bash
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
python manage.py makemigrations users
python manage.py migrate
python manage.py createsuperuser   # pide email, username y contraseña
python manage.py runserver
```

En Linux/macOS activa el entorno con `source venv/bin/activate`.

## URLs

| Recurso | URL |
|---|---|
| Swagger | http://127.0.0.1:8000/swagger/ |
| ReDoc | http://127.0.0.1:8000/redoc/ |
| Admin | http://127.0.0.1:8000/admin/ |

## Endpoints (prefijo `/api/v1/`)

| Método | Ruta | Descripción | Acceso |
|---|---|---|---|
| POST | `auth/token/` | Obtiene `access` y `refresh` (body: `email`, `password`) | Público |
| POST | `auth/token/refresh/` | Renueva el token de acceso | Público |
| POST | `auth/register/` | Registro público de usuarios | Público |
| GET | `auth/me/` | Datos personales del usuario del token | Autenticado |
| GET | `soap/country/?code=MX` | Consulta SOAP con zeep (CountryInfoService) | Autenticado |
| GET/POST | `users/` | Listar / crear usuarios | Admin |
| GET/PUT/PATCH/DELETE | `users/{id}/` | Detalle / editar / eliminar | Admin |

## Pruebas automáticas

```bash
python manage.py test
```

## Seguridad (correcciones respecto al manual)

1. `password` es `write_only` en el serializer: el hash nunca aparece en ninguna respuesta (incluido `auth/me/`).
2. La contraseña solo se cambia si llega en la petición (lógica en `serializer.update`); ya no se copia la del usuario que hace la petición.
