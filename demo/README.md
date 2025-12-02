# Demo Docker Compose: Postgres + FastAPI + Web (Nginx)

Esta demo despliega una aplicación multi-contenedor con **Docker Compose** formada por:

- **Postgres**: base de datos (persistente con volumen)
- **FastAPI**: API que lee/escribe en Postgres
- **Nginx (web)**: servidor web simple que sirve un `index.html` y consume la API

El objetivo es practicar:
- redes en Compose (comunicación por nombre de servicio)
- variables de entorno
- volúmenes (persistencia)
- reverse proxy básico (Nginx -> FastAPI)

---

## Arquitectura

```text
Navegador
   |
   | http://localhost:8080
   v
[ web (nginx) ]  -- /api/* -->  [ api (fastapi) ]  -->  [ db (postgres) ]
       |                 (red_publica + red_privada)        (red_privada)
       |
   sirve index.html
```

- La web se publica al host en el puerto **8080**.
- La API se publica al host en el puerto **8000**.
- La base de datos **no** se publica (solo accesible dentro de la red privada).
- Nginx hace de puente: `GET /api/notes` -> `http://api:8000/notes`.

---

## Estructura del proyecto

```text
compose-demo/
  docker-compose.yml
  api/
    Dockerfile
    requirements.txt
    main.py
  web/
    Dockerfile
    index.html
    nginx.conf
```

---

## Requisitos

- Docker instalado
- Docker Compose v2 (se usa como `docker compose ...`)

Si estás en **WSL 2 + Ubuntu 22.04**, asegúrate de tener Docker funcionando:

```bash
sudo systemctl status docker
```

---

## Puertos

- Web (Nginx): `http://localhost:8080`
- API (FastAPI): `http://localhost:8000`
  - Health: `http://localhost:8000/health`
  - Notes: `http://localhost:8000/notes`

---

## Cómo arrancar la demo

Desde la carpeta raíz del proyecto (`compose-demo/`):

```bash
docker compose up -d --build
```

Qué hace este comando:
- Construye las imágenes de `api` y `web` a partir de sus Dockerfiles
- Descarga `postgres:16` si no existe
- Crea redes y volumen si no existen
- Levanta los 3 servicios en segundo plano

Comprobar estado:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs
docker compose logs -f
```

---

## Cómo probarla

1) Abre la web:

- `http://localhost:8080`

2) Pulsa **“Cargar notas”**  
La web hará un `fetch("/api/notes")` hacia Nginx, y Nginx lo reenviará a FastAPI.

3) Prueba la API directamente:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/notes
```

---

## Persistencia (volumen de Postgres)

La base de datos usa un volumen llamado `pgdata`:

- Si paras y vuelves a levantar, los datos siguen.
- Si borras el volumen, se pierden.

Bajar servicios (manteniendo datos):

```bash
docker compose down
```

Bajar y borrar datos de Postgres (cuidado):

```bash
docker compose down -v
```

---

## Qué está pasando “por dentro” (redes y DNS)

En el `docker-compose.yml` hay dos redes:

- `red_privada`: comunicación interna entre `api` y `db`
- `red_publica`: exposición de `web` y `api` hacia el host

Puntos clave:
- Dentro de la red, los servicios se resuelven por nombre:
  - `db` es el hostname de Postgres
  - `api` es el hostname de FastAPI
- La API se conecta a Postgres con `DB_HOST=db`
- Nginx redirige `/api/` a `http://api:8000/`

---

## Limpieza y reinicio rápido

Parar contenedores (sin borrar):

```bash
docker compose stop
```

Arrancar de nuevo:

```bash
docker compose start
```

Recrear todo “limpio” (manteniendo volumen si no usas `-v`):

```bash
docker compose down
docker compose up -d --build
```

---

## Problemas comunes

### La web no carga datos (lista vacía o error)
- Comprueba logs de la API:
  ```bash
  docker compose logs -f api
  ```
- Comprueba que Nginx está haciendo proxy:
  ```bash
  docker compose logs -f web
  ```

### La API falla al conectar con Postgres
Esto puede pasar si Postgres aún no está listo cuando arranca la API (aunque `depends_on` inicie antes el contenedor, no garantiza “ready”).

Soluciones típicas:
- Reintentar conexión en la API (retry)
- Añadir `healthcheck` al servicio `db` y usar condiciones

> [!IMPORTANT]
> En el archivo [docker-compose.yml](docker-compose.yml) hay un bloque comentado con el healthcheck implementado para ver las diferencias. Es probable que el error solo aparezca cuando hagas el primer docker compose up ya que la base de datos tarda más en iniciar la primera vez.

---

## Referencia rápida de comandos

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f
docker compose down
docker compose down -v
```
