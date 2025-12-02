## Ejercicio final (integrador): Docker Compose tipo demo (Postgres + API + Web)

**Objetivo:** crear una solución multi-servicio similar a la demo del repositorio, aplicando TODO:
- Dockerfile (para API y web)
- variables de entorno
- redes (privada + pública)
- volumen para Postgres
- endpoints GET (Obligatorio) y POST (Opcional)

### Requisitos mínimos
1. Servicios:
   - `db` (postgres)
   - `api` (FastAPI o similar)
   - `web` (Nginx o web simple estática)
2. Persistencia:
   - volumen para `/var/lib/postgresql/data`
3. Redes:
   - `red_privada`: `api` ↔ `db`
   - `red_publica`: `web` ↔ `api` + exposición al host
4. API:
   - `GET /tu-endpoint`
   - `POST /tu-endpoint`
5. Web:
   - Página con botón “cargar datos”
   - Formulario simple para crear un registro (POST) y refrescar lista
   - Nginx con proxy `/api/` -> `api:8000/` (Mirar demo)

### Comandos esperados
- Arranque:
  - `docker compose up -d --build`
- Logs:
  - `docker compose logs -f`
- Parada:
  - `docker compose down`
- Limpieza completa:
  - `docker compose down -v`

### Entregable
- `docker-compose.yml`
- `api/Dockerfile` + código API
- `web/Dockerfile` + `index.html` + `nginx.conf`
- Un mini README de 10-15 líneas con:
  - cómo levantarlo
  - URLs
  - cómo probar POST con curl