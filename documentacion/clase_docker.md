# Curso de Introducción a Docker

Este repositorio contiene el material para una clase/taller de **Introducción a Docker** orientado a desarrollo, IA y Big Data sobre **WSL 2 + Ubuntu 22.04**.

> [!WARNING]  
> Antes de esta clase, el alumnado debe haber seguido:
> - [Instalación WSL con Ubuntu 22.04 LTS](../guias_instalacion/instalacion_wsl_ubuntu_22_04.md)
> - [Instalación Docker en Ubuntu 22.04 LTS](../guias_instalacion/instalacion_docker_wsl_ubuntu_22_04.md)

---

## Índice

1. [Componentes de Docker: Docker Engine, CLI y API](#1-componentes-de-docker-docker-engine-cli-y-api)  
2. [Imágenes, contenedores y capas](#2-imágenes-contenedores-y-capas)  
3. [Volúmenes y bind mounts](#3-volúmenes-y-bind-mounts)  
4. [Dockerfiles: Anatomía y Sintaxis](#4-dockerfiles-anatomía-y-sintaxis)  
5. [Versionado y etiquetado](#5-versionado-y-etiquetado)  
6. [Docker Hub y repositorios privados](#6-docker-hub-y-repositorios-privados)  
7. [Redes](#7-redes)  
8. [Docker Compose](#8-docker-compose)  

---

## ¿Qué es docker?
Docker es una plataforma que permite crear, empaquetar y ejecutar aplicaciones dentro de contenedores ligeros y portables. Estos contenedores incluyen todo lo necesario para que la aplicación funcione (dependencias, librerías y configuración) garantizando entornos reproducibles, despliegues rápidos y un comportamiento consistente en cualquier sistema.

---

## 1. Componentes de Docker: Docker Engine, CLI y API

En este primer apartado, el objetivo es entender **cómo funciona Docker internamente**.

A alto nivel:

- El **daemon (Docker Engine)** es el *servicio* que hace todo el trabajo real.
- La **CLI (`docker`)** es el *programa de consola* que utilizas tú.
- La **Docker API** es el *lenguaje común* que conecta herramientas (CLI, GUIs, CI/CD) con el daemon.

---

### 1.1. Docker Engine (daemon)

El **Docker Engine** es el “motor” de Docker:

- Es un **servicio en segundo plano** (daemon) que se ejecuta en el sistema.
- Se encarga de:
  - Descargar y almacenar **imágenes**.
  - Crear, arrancar, parar y eliminar **contenedores**.
  - Gestionar **redes** y **volúmenes**.
  - Responder a las peticiones que llegan a través de la **Docker API**.

En Linux/WSL se controla con `systemd` como cualquier otro servicio:

```bash
# Ver el estado del servicio Docker
sudo systemctl status docker

# Arrancar Docker si está parado
sudo systemctl start docker

# Hacer que Docker se inicie automáticamente con el sistema
sudo systemctl enable docker
```

Si el daemon **no está en ejecución**, cualquier comando `docker ...` fallará con mensajes del tipo:

```text
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

Puntos importantes:

- Docker Engine es el **servidor**.
- Nada funciona sin él, aunque tengas instalada la CLI.
- Normalmente no lo manejas directamente, sino a través de la CLI o de otras herramientas.

---

### 1.2. Docker CLI (Command Line Interface)

La **Docker CLI** es el comando `docker` que ejecutas en la terminal.

Conceptos clave:

- La CLI es un **cliente** que se comunica con el daemon usando la **Docker API**.
- Cada vez que escribes un comando, la CLI:
  1. Interpreta los parámetros (`run`, `ps`, `-d`, `-p`, etc.).
  2. Construye una petición a la API de Docker.
  3. Envía esa petición al socket del daemon (`/var/run/docker.sock`).
  4. Recibe la respuesta y la muestra en pantalla.

Para ver la separación cliente/servidor podemos ejecutar el siguiente comando:

```bash
docker version
```

Salida (resumida):

```text
Client: Docker Engine - Community
 Version:           27.0.0
 ...

Server: Docker Engine - Community
 Engine:
  Version:          27.0.0
  ...
```

Comandos útiles para esta parte:

```bash
# Muestra información general del servidor Docker
docker info

# Lista contenedores en ejecución
docker ps

# Lista imágenes descargadas
docker images ls
```

---

### 1.3. Docker API

La **Docker API** es una API **HTTP** que expone el daemon. Es el “idioma” que entienden tanto la CLI como cualquier otra herramienta que quiera hablar con Docker.

Por defecto, en Linux/WSL se expone a través de un **socket UNIX**: `unix:///var/run/docker.sock`

Cuando ejecutas:

```bash
docker run hello-world
```

se producen internamente varias llamadas a la Docker API:

1. Comprobar si la imagen `hello-world` existe localmente.
2. Si no existe, descargarla desde el registro (Docker Hub por defecto).
3. Crear el contenedor (definir su configuración: comando, variables de entorno, volúmenes, puertos…).
4. Arrancarlo y adjuntar la salida.

Aunque normalmente **no llamamos directamente a la API**, podemos hacerlo para fines de debug o automatización avanzada. Ejemplo ilustrativo:

Podemos hacer ping a la API con el siguiente comando:
```bash
curl --unix-socket /var/run/docker.sock http://localhost/_ping
```

Si el daemon está activo, responderá con:

```text
OK
```

Esto demuestra que:

- El daemon escucha peticiones HTTP.
- La CLI no es mágica: es simplemente un wrapper para esta API.

---

### 1.4. Resumen visual

Puedes usar este esquema en la pizarra o en una diapositiva:

```text
+------------------------------+
|         Usuario / Dev        |
|  (teclado, terminal, IDE)    |
+---------------+--------------+
                |
                v
+------------------------------+
|         Docker CLI           |
|        (comando docker)      |
+---------------+--------------+
                |
                |  (Docker API - HTTP)
                v
+------------------------------+
|        Docker Engine         |
|           Daemon             |
+---------------+--------------+
                |
     ------------------------
     |          |           |
  Imágenes   Contenedores  Volúmenes / Redes
```

## 2. Imágenes, contenedores y capas

Este apartado es clave para entender qué es realmente un contenedor, cómo se crea a partir de una imagen y cómo funciona el sistema de capas de Docker.

---

### 2.1. ¿Qué es una imagen en Docker?

Una imagen de Docker es una plantilla inmutable, lista para usarse como base para crear contenedores. Es un conjunto de capas organizadas que contienen:
- Un sistema operativo mínimo
- Librerías y dependencias necesarias
- Código de aplicación
- Configuraciones por defecto
- Metadatos (comandos predeterminados, variables, puertos expuestos…)

No es un programa ejecutándose:
Es el “molde” del que se crean los contenedores.

#### 2.1.1 Una imagen tiene múltiples capas (layers), no es un archivo enorme sino un conjunto de capas apiladas.

Cada capa:
- Es inmutable
- Es compartida entre imágenes
- Representa un cambio incremental (por ejemplo, “instalar Python”, “copiar archivo”, etc.)

#### ¿Por qué esto es importante?
- Ahorra espacio (una capa usada por 10 imágenes ocupa espacio una sola vez)
- Acelera descargas (solo se descargan capas faltantes)
- Permite construir imágenes más rápido (cacheado de capas)

#### Ejemplos:

Descargar la imagen de ubuntu 22.04:
- **ubuntu** → nombre de la imagen  
- **22.04** → etiqueta (tag)

```bash
docker pull ubuntu:22.04
```

Ver imágenes locales:

```bash
docker image ls
```

Ver capas:

```bash
docker image inspect ubuntu:22.04
```

Ejemplo de salida:

```
"Layers": [
  "sha256:a1b2...",
  "sha256:f3d8...",
  "sha256:9c1e..."
]
```

---

### 2.2. ¿Qué es un contenedor?

Un **contenedor** es una **instancia en ejecución** de una imagen.

Puedes compararlo con:
- **Imagen** → clase (en programación)
- **Contenedor** → objeto (instancia)

#### 2.2.1 Crear y ejecutar un contenedor:

```bash
docker run ubuntu:22.04 echo "Hola Docker"
```

Docker hace:
1. Busca la imagen localmente
2. Si no existe → la descarga
3. Crea un contenedor basado en esa imagen
4. Ejecuta el comando indicado
5. El contenedor termina cuando el comando finaliza

#### 2.2.2 Un contenedor añade una capa de escritura (RW layer)

La imagen es inmutable, pero el contenedor sí puede cambiar cosas porque añade una capa de escritura temporal.

Esa capa permite:
```
- Escribir archivos
- Modificar configuraciones
- Instalar dependencias (aunque NO se guardan en la imagen)
- Crear logs temporales
```

Pero todo se pierde cuando el contenedor se elimina, a menos que se usen volúmenes o bind mounts (que se explicarán más adelante).

#### 2.2.3 Un contenedor tiene su propio runtime (entorno de ejecución)

Cada contenedor ejecuta:
- Su propio proceso principal (PID 1 dentro del contenedor)
- Su propio entorno de usuario (rootfs aislado)
- Su propia estructura de directorios independiente
- Sus propias librerías
- Su propio runtime (por ejemplo, Python dentro del contenedor, aunque no esté instalado en el host)

Este entorno de ejecución además está aislado del host (la máquina real).

Esto permite que:
```
- Los procesos dentro del contenedor no vean procesos del host.
- Cada contenedor tenga su propia IP interna y reglas de red.
- El sistema de archivos sea independiente del host.
```

#### 2.2.4 Un contenedor puede exponer puertos

Aunque está aislado, un contenedor puede exponer servicios al exterior:

```
docker run -d -p 8080:80 nginx
```
- Puerto 80 del contenedor
- Mapeado al puerto 8080 del host

El navegador puede acceder a: http://localhost:8080


Sin exponer puertos, el contenedor estaría totalmente aislado.

> [!IMPORTANT]
> Un contenedor no es una máquina virtual. Los contenedores comparten el kernel del host, lo que los hace extremadamente rápidos y eficientes.   
> **Diferencias:**
> | Docker                  | Máquina Virtual                 |
> | ----------------------- | ------------------------------- |
> | No tiene kernel propio  | Cada VM tiene su kernel         |
> | Aísla procesos          | Aísla sistemas completos        |
> | Arranca en milisegundos | Arranca en minutos              |
> | Ligero                  | Pesado                          |
> | Basado en procesos      | Basado en hardware virtualizado |


---

### 2.3. Diferencia clave: imagen vs contenedor

| Imagen | Contenedor |
|--------|------------|
| Plantilla inmutable | Instancia en ejecución |
| No cambia | Puede modificarse mientras corre |
| Se usa como base | Se crea y se elimina |
| Se almacena en capas | Tiene su propia capa de escritura |

### 2.4. Operaciones comunes con imágenes

```bash
docker pull nginx
docker image rm nginx
docker inspect python:3.11
```

---

### 2.5. Operaciones comunes con contenedores

```bash
docker run -d nginx
docker ps
docker stop <id>
docker rm <id>
```

---

## 3. Volúmenes y bind mounts

En Docker, si guardas datos “dentro” del contenedor, **se perderán** cuando elimines ese contenedor (porque esos cambios viven en su capa de escritura). Para persistir datos y/o compartir archivos entre tu máquina y un contenedor, usamos:

- **Volúmenes (volumes):** gestionados por Docker, recomendados para datos persistentes.
- **Bind mounts:** montan una carpeta/archivo del host dentro del contenedor, muy usados en desarrollo.

---

### 3.1. Problema que resolvemos: “se me borra todo”

Ejemplo típico:

```bash
docker run -it ubuntu:22.04 bash
echo "hola" > /tmp/dato.txt
exit
```

Ese archivo queda dentro del contenedor. Si borras el contenedor:

```bash
docker ps -a
docker rm <id_del_contenedor>
```

El archivo se pierde. Para evitarlo, usamos volúmenes o bind mounts.

---

### 3.2. Volúmenes (Volumes)

Un **volumen** es un espacio de almacenamiento **persistente** gestionado por Docker. No depende del ciclo de vida del contenedor:

- Si borras el contenedor, el volumen **puede seguir existiendo**.
- Puedes montar el mismo volumen en varios contenedores.
- Es la opción recomendada para bases de datos, uploads, cache, etc.

#### 3.2.1. Crear y listar volúmenes

```bash
docker volume create datos_demo
docker volume ls
```

Inspeccionar:

```bash
docker volume inspect datos_demo
```

#### 3.2.2. Montar un volumen en un contenedor

```bash
docker run -it --name cvol -v datos_demo:/data ubuntu:22.04 bash
```

Dentro del contenedor:

```bash
echo "persisto" > /data/archivo.txt
exit
```

Borra el contenedor:

```bash
docker rm cvol
```

Crea otro contenedor montando el mismo volumen:

```bash
docker run -it --name cvol2 -v datos_demo:/data ubuntu:22.04 bash
cat /data/archivo.txt
exit
```

Resultado: el archivo sigue ahí.

#### 3.2.3. Borrar volúmenes

Si un volumen ya no se usa:

```bash
docker volume rm datos_demo
```

Limpiar volúmenes huérfanos:

```bash
docker volume prune
```

> [!WARNING]   
> Ojo: `prune` borra lo que Docker considere “no usado”. Úsalo con cuidado.

---

### 3.3. Bind mounts

Un **bind mount** monta una ruta real de tu host dentro del contenedor.

- Tú eliges exactamente qué carpeta/archivo del host montar.
- Muy útil en desarrollo: editar código en tu host y que el contenedor lo lea al instante.
- El contenedor puede escribir en esa carpeta (según permisos y flags).

#### 3.3.1. Ejemplo rápido: montar la carpeta actual

En la carpeta donde estés (host):

```bash
docker run -it --name bind1 -v "$(pwd)":/app ubuntu:22.04 bash
```

Dentro del contenedor:

```bash
ls -la /app
```

Lo que tengas en tu carpeta local aparecerá dentro de `/app`.

#### 3.3.2. Caso típico de desarrollo (Python)

Estructura:

```
proyecto/
  app.py
```

`app.py`:

```python
print("Hola desde contenedor leyendo tu carpeta")
```

Ejecutar:

```bash
docker run --rm -v "$(pwd)":/app -w /app python:3.11 python app.py
```

- `-v "$(pwd)":/app` monta el proyecto
- `-w /app` define el working dir dentro del contenedor
- No instalas Python localmente: usas el del contenedor

---

### 3.4. Diferencias clave: volumen vs bind mount

| Aspecto | Volumen | Bind mount |
|---|---|---|
| Quién lo gestiona | Docker | Tú (ruta del host) |
| Uso típico | Datos persistentes (DB, uploads) | Desarrollo (código, configs) |
| Portabilidad | Alta | Depende de rutas del host |
| Riesgo | Menor (aislado) | Mayor (acceso directo al host) |

Regla práctica:
- **Producción / datos** → Volúmenes
- **Desarrollo / código** → Bind mounts

---

### 3.5. Lectura/escritura y modo “solo lectura”

Por defecto, el mount es RW. Para hacerlo solo lectura:

```bash
docker run --rm -v "$(pwd)":/app:ro ubuntu:22.04 ls /app
```

Esto evita que el contenedor modifique archivos del host.

---

### 3.7. Errores comunes

- “No veo archivos en /app”
  - Estás en otra carpeta del host
  - La ruta del mount está mal
- “Permission denied”
  - Permisos del filesystem del host o del usuario dentro del contenedor
- “Se me borró la base de datos”
  - No usaste volumen, o borraste volúmenes con `prune`

---

## 4. Dockerfiles: Anatomía y Sintaxis

En este apartado aprenderás a crear tus propias imágenes de forma **repetible** usando un **Dockerfile**. La idea clave es:

- **No** “instales cosas a mano” dentro de un contenedor y esperes que se conserven.
- En su lugar, define el entorno en un Dockerfile y construye una imagen con `docker build`.

Un Dockerfile es como una receta para construir una imagen. Docker lee el Dockerfile línea por línea y va creando la imagen por capas.

Cada instrucción importante (sobre todo RUN, COPY, ADD) suele generar una nueva capa. Eso tiene dos consecuencias:

- Caché: si una línea no cambia, Docker puede reutilizar esa capa y el build será más rápido.

- Tamaño: si haces cosas “innecesarias” en capas extra, la imagen puede crecer.

---

### 4.1. Estructura mínima de un Dockerfile

Ejemplo simple (Python):

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```

Construir:

```bash
docker build -t miapp:1.0 .
```

Ejecutar:

```bash
docker run --rm miapp:1.0
```

---

### 4.2. Anatomía: instrucciones más comunes

A continuación van las instrucciones más usadas y qué significa cada una.

#### 4.2.1. `FROM` (base image)

Define la imagen base:

```Dockerfile
FROM ubuntu:22.04
```

Buenas prácticas:
- Usa imágenes oficiales.
- Prefiere variantes ligeras cuando aplique (`-slim`, `alpine`), pero sin complicarte al inicio.
- Evita `latest` en proyectos serios: usa tags concretos.

---

#### 4.2.2. `WORKDIR` (directorio de trabajo)

Cambia (y crea si no existe) el directorio donde se ejecutarán instrucciones posteriores:

```Dockerfile
WORKDIR /app
```

Esto evita hacer `cd` y mejora la legibilidad.

---

#### 4.2.3. `COPY` y `ADD` (copiar archivos)

`COPY` es la opción recomendada en la mayoría de casos:

```Dockerfile
COPY . .
COPY requirements.txt .
```

`ADD` añade funcionalidades extra (auto-descompresión de tar, URLs), pero se recomienda evitarlo si no hace falta.

---

#### 4.2.4. `RUN` (ejecutar comandos durante el build)

Ejecuta comandos al construir la imagen (crea una capa):

```Dockerfile
RUN apt-get update && apt-get install -y curl
```

Buenas prácticas con `RUN`:
- Agrupa comandos en una sola instrucción para reducir capas.
- En Debian/Ubuntu, suele hacerse:
  - `apt-get update` + `apt-get install` en la misma capa
  - limpieza de caché para reducir tamaño

Ejemplo recomendado:

```Dockerfile
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
```

---

#### 4.2.5. `ENV` (variables de entorno)

Define variables disponibles en build y runtime:

```Dockerfile
ENV APP_ENV=prod
```

Nota de seguridad:
- No metas secretos (tokens, contraseñas) en `ENV` si la imagen se va a publicar.

---

#### 4.2.6. `EXPOSE` (documentar puertos)

Indica el puerto esperado de la aplicación:

```Dockerfile
EXPOSE 8080
```

> [!NOTE]  
> `EXPOSE` no publica puertos por sí mismo. Solo es una “pista”.  
> Para publicar puertos se usa `-p` en `docker run`.

---

#### 4.2.7. `CMD` vs `ENTRYPOINT` (qué se ejecuta al arrancar)

**`CMD`** define el comando por defecto. Puede ser sobrescrito fácilmente:

```Dockerfile
CMD ["python", "app.py"]
```

**`ENTRYPOINT`** define el ejecutable principal. Suele usarse cuando quieres que el contenedor se comporte “como un comando”.

Ejemplo típico:

```Dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]
```

Entonces:
- Por defecto ejecuta `python app.py`
- Pero podrías hacer: `docker run imagen script2.py` y ejecutaría `python script2.py`

Regla práctica:
- Para la mayoría de apps sencillas, `CMD` es suficiente.
- `ENTRYPOINT` se usa más en imágenes tipo “tooling” o cuando quieres un comportamiento muy fijo.

---

### 4.3. Construcción: `docker build`

Comando típico:

```bash
docker build -t miapp:1.0 .
```

- `-t` etiqueta la imagen
- `.` indica el contexto de build (archivos disponibles para `COPY`)

Ver imágenes:

```bash
docker image ls
```

---

### 4.4. Importante: el “contexto” de build y `.dockerignore`

Cuando haces `docker build .`, Docker envía al motor **todo el contenido de esa carpeta** como contexto. Si mandas cosas innecesarias (por ejemplo `node_modules`), el build será más lento y la imagen puede crecer.

Crea un `.dockerignore` para excluir:

Ejemplo:

```
.git
__pycache__/
*.pyc
.env
node_modules/
dist/
```

---

### 4.5. Ejemplo completo (Python) con dependencias

Estructura del proyecto:

```
miapp/
  app.py
  requirements.txt
  Dockerfile
```

`app.py`:

```python
import requests
print("Docker + Python OK")
```

`requirements.txt`:

```
requests==2.31.0
```

`Dockerfile`:

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

Build y run:

```bash
docker build -t miapp:1.0 .
docker run --rm miapp:1.0
```

---

### 4.6. Ejemplo web mínimo (Flask) con puertos

Estructura:

```
flaskapp/
  app.py
  requirements.txt
  Dockerfile
```

`app.py`:

```python
from flask import Flask
app = Flask(__name__)

@app.get("/")
def home():
    return "Hola desde Flask en Docker"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

`requirements.txt`:

```
flask==3.0.0
```

`Dockerfile`:

```Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
```

Build:

```bash
docker build -t flaskapp:1.0 .
```

Run publicando el puerto:

```bash
docker run --rm -p 5000:5000 flaskapp:1.0
```

Abrir:

```
http://localhost:5000
```

---

### 4.7. Errores comunes

- “`COPY` no encuentra archivos”
  - Estás construyendo desde la carpeta incorrecta
  - El archivo no está en el **contexto** (`docker build .`)
- “La app web no carga”
  - No has puesto `host="0.0.0.0"` dentro de la app
  - No has publicado puertos con `-p`
- “La imagen pesa mucho”
  - Falta `--no-cache-dir` en pip
  - Faltan limpiezas en `apt`
  - Estás copiando cosas innecesarias (usa `.dockerignore`)

---


## 5. Versionado y etiquetado

En Docker, el **versionado** normalmente se gestiona mediante **tags** de imágenes. Un tag es una etiqueta que apunta a una versión concreta de una imagen.

Formato general:

```
nombre:tag
```

Ejemplos:

- `nginx:1.25`
- `python:3.11-slim`
- `miapp:1.0`
- `miapp:1.0.3`

> [!TIP]
> Un tag no es “la imagen”, es un **alias** que apunta a una imagen concreta.

---

### 5.1. ¿Qué es un tag?

Un tag es una forma humana de referirte a una imagen. Docker lo usa para que puedas:

- Identificar versiones
- Publicar y descargar versiones concretas
- Mantener varias variantes (dev, prod, slim, alpine, etc.)

Ejemplo:

```bash
docker pull python:3.11
docker pull python:3.12
```

Son dos versiones diferentes del mismo repositorio `python`.

---

### 5.2. ¿Qué pasa si no pongo tag?

Si no pones tag, se usa `latest` por defecto.

```bash
docker pull ubuntu
# equivale a
docker pull ubuntu:latest
```

Buenas prácticas:
- En proyectos serios evita depender de `latest`.
- Usa tags específicos (ej: `1.0.3`, `3.11-slim`, etc.) para builds reproducibles.

---

### 5.3. Etiquetar imágenes locales: `docker tag`

Puedes “ponerle otro nombre/tag” a una imagen existente:

```bash
docker tag miapp:1.0 miapp:1.0.1
```

También es obligatorio cuando quieres subir una imagen a tu usuario/organización:

```bash
docker tag miapp:1.0 TUUSUARIO/miapp:1.0
```

Ver imágenes:

```bash
docker image ls
```

---

### 5.4. Buenas prácticas de etiquetado

- Evita `latest` para producción.
- Publica siempre un tag inmutable: `1.2.3`.
- Si usas tags por entorno (`prod`), que sea adicional: `prod` + `1.2.3`.
- Mantén consistencia: decide un estándar (SemVer, commit, fecha) y úsalo siempre.
- Para imágenes base: fija versión y variante (ej: `python:3.11-slim`).

---

### 5.5. Ejemplo práctico completo (build + tags)

Supón que has construido tu app:

```bash
docker build -t TUUSUARIO/miapp:1.0.0 .
```

Crear un tag adicional “prod”:

```bash
docker tag TUUSUARIO/miapp:1.0.0 TUUSUARIO/miapp:prod
```

Subir ambos tags al registry:

```bash
docker push TUUSUARIO/miapp:1.0.0
docker push TUUSUARIO/miapp:prod
```

---

## 6. Docker Hub y repositorios privados

En este apartado aprenderás qué es un **registry**, cómo funciona **Docker Hub**, y cómo **subir y descargar** imágenes (públicas y privadas). Esto es esencial para poder compartir aplicaciones, desplegar en servidores y trabajar en equipo.

---

### 6.1. Conceptos clave: Registry vs Repository

- **Registry (registro):** servicio donde se almacenan imágenes.
  - Ejemplos: **Docker Hub**, GitHub Container Registry (GHCR), Azure Container Registry (ACR).
- **Repository (repositorio):** “carpeta” dentro de un registry donde viven las versiones (tags) de una imagen.
  - Ejemplo: `nginx` es un repo en Docker Hub.
  - Ejemplo: `tuusuario/miapp` sería tu repo personal.

Una imagen se suele nombrar como:

```
<registry>/<namespace>/<repo>:<tag>
```

En Docker Hub, el `registry` suele omitirse (por defecto es Docker Hub):

- `nginx:latest`
- `python:3.11`
- `tuusuario/miapp:1.0`

---

### 6.2. Docker Hub: qué es y qué ofrece

**Docker Hub** es el registry público más común. Desde ahí puedes:

- **Descargar** imágenes oficiales (nginx, redis, postgres, python…)
- Usar imágenes de la comunidad (con cuidado y criterio)
- **Publicar** tus propias imágenes (públicas o privadas, según tu plan)
- Mantener un repositorio con múltiples versiones mediante **tags**

---

### 6.3. Buscar y descargar imágenes (pull)

Descargar una imagen es hacer un **pull**:

```bash
docker pull nginx:latest
docker pull python:3.11
docker pull alpine:3.20
```

Ver tus imágenes locales:

```bash
docker image ls
```

Si ejecutas un contenedor con una imagen que no tienes, Docker hace el pull automáticamente:

```bash
docker run --rm hello-world
```

---

### 6.4. Autenticación: docker login (recomendado con token)

Para subir imágenes a tu cuenta (push) o descargar privadas, necesitas autenticarte:

> [!WARNING]
> Para iniciar sesión necesitas una cuenta en **[Docker Hub](https://hub.docker.com/)**.

```bash
docker login
```

- Usuario: tu usuario de Docker Hub
- Contraseña: lo habitual es usar un **token de acceso** (Personal Access Token) desde la configuración de Docker Hub

Comprobar que estás autenticado suele ser tan simple como intentar un `docker push` (si falla por permisos, normalmente es login).

Cerrar sesión:

```bash
docker logout
```

---

### 6.5. Subir tu primera imagen a Docker Hub (push)

**Idea:** nunca vas a poder subir al repo `nginx` (no es tuyo). Lo que haces es:
1) Tener una imagen local (por ejemplo `nginx`)
2) Re-etiquetarla a tu espacio (`tuusuario/...`)
3) Hacer `push`

#### Paso 1: Obtener una imagen local

```bash
docker pull nginx:latest
```

#### Paso 2: Re-etiquetar (tag) a tu repositorio

Sustituye `TUUSUARIO` por tu usuario real:

```bash
docker tag nginx:latest TUUSUARIO/mi-nginx:1.0
```

Comprueba:

```bash
docker image ls
```

Deberías ver algo como:
- `nginx:latest`
- `TUUSUARIO/mi-nginx:1.0`

#### Paso 3: Subir (push)

```bash
docker push TUUSUARIO/mi-nginx:1.0
```

#### Paso 4: Verificar descargando desde “cero”

Borra la imagen local re-etiquetada y vuelve a descargar:

```bash
docker image rm TUUSUARIO/mi-nginx:1.0
docker pull TUUSUARIO/mi-nginx:1.0
```

---

### 6.6. Repositorios privados: qué son y cómo se usan

Un **repositorio privado** en Docker Hub es un repositorio que:
- No es visible públicamente
- Requiere estar autenticado y tener permisos para hacer `pull`

Flujo típico:
1) Creas un repo privado en Docker Hub (por ejemplo `TUUSUARIO/mi-nginx-privado`)
2) Haces `tag` y `push` a ese repo
3) Cualquier `pull` exige `docker login`

#### Ejemplo con repo privado

```bash
docker tag nginx:latest TUUSUARIO/mi-nginx-privado:1.0
docker push TUUSUARIO/mi-nginx-privado:1.0
```

Probar que es privado:
- Si haces `docker logout` y luego intentas:
  ```bash
  docker pull TUUSUARIO/mi-nginx-privado:1.0
  ```
  debería fallar por falta de permisos (lo cual es lo esperado)

---

### 6.7. Permisos y colaboración (muy importante en equipos)

En repos privados, lo habitual es:
- Compartir acceso con miembros del equipo (según lo que permita el plan/organización)
- Usar tokens específicos (rotables) en CI/CD
- Evitar credenciales personales en servidores compartidos

---

### 6.8. Buenas prácticas al publicar imágenes

- **No subas secretos** dentro de imágenes:
  - Nunca claves en `ENV` dentro del Dockerfile si vas a publicar
  - No metas `.env`, llaves SSH, tokens, etc.
- Usa `.dockerignore` para excluir:
  - `node_modules/`, `.git/`, `.env`, archivos pesados, etc.
- Publica con **tags claros**, por ejemplo:
  - `1.0`, `1.1`, `1.1.3`, `prod`, `dev` (según política)
- Prefiere tags **inmutables** para despliegues (ej: `1.2.3`), y usa `latest` solo como conveniencia.

---

## 7. Redes

En Docker, la red es lo que permite que:

- Un contenedor se comunique con Internet (por ejemplo, para descargar paquetes).
- Un contenedor se comunique con otro (por ejemplo, una API con una base de datos).
- Tu host acceda a un servicio dentro del contenedor (por ejemplo, abrir Nginx en el navegador).

Docker crea redes virtuales para conectar contenedores entre sí sin necesidad de exponer todo al exterior.

---

### 7.1. Conceptos básicos

#### 7.1.1. Contenedor aislado, red controlada
Por defecto, un contenedor tiene su propia pila de red (IP interna, interfaz, etc.). No es una máquina completa, pero se comporta como un entorno aislado.

Puedes ver la IP interna de un contenedor con:

```bash
docker inspect <id_o_nombre> | grep -i "IPAddress"
```

---

### 7.2. Tipos de red principales en Docker

#### 7.2.1. `bridge` (la más común)
Es la red por defecto en Docker. Ideal para:

- Desarrollar en local
- Conectar varios contenedores en el mismo host

Docker crea un bridge (puente) en el que se conecta tu máquina real por defecto y asigna IPs internas. Los contenedores en el mismo bridge pueden comunicarse.

Ver redes:

```bash
docker network ls
```

Ver detalles:

```bash
docker network inspect bridge
```

#### 7.2.2. `host` (compartir red del host)
El contenedor usa la red del host directamente.

- Menos aislamiento
- Útil en casos específicos (monitorización, rendimiento, algunos servicios)

Ejemplo:

```bash
docker run --rm --network host nginx
```

#### 7.2.3. `none` (sin red)
El contenedor no tiene conectividad de red.

```bash
docker run --rm --network none alpine
```

---

### 7.3. Publicación de puertos: `-p`

Importante: los contenedores no publican puertos por defecto.

- Si quieres acceder desde el host (navegador, curl, etc.), necesitas `-p`.

Ejemplo:

```bash
docker run -d --name web -p 8080:80 nginx
```

- `80` es el puerto dentro del contenedor
- `8080` es el puerto en tu host

Probar:

```bash
curl http://localhost:8080
```

> [!NOTE]
> Sin `-p`, el contenedor podría estar funcionando, pero no podrías acceder desde fuera.

---

### 7.4. Redes definidas por el usuario (recomendadas)

Aunque existe la red `bridge` por defecto, lo mejor para proyectos es crear una red propia, porque:

- Los contenedores pueden resolverse por nombre automáticamente (DNS interno).
- Separas proyectos (menos conflictos).
- Tu arquitectura queda más clara.

Crear una red:

```bash
docker network create red_clase
```

Verla:

```bash
docker network ls
```

---

### 7.5. Comunicación entre contenedores por nombre (demo típica)

Vamos a levantar un contenedor Nginx y otro Alpine en la misma red y hacer que se comuniquen.

1) Crear red:

```bash
docker network create red_clase
```

2) Levantar Nginx en esa red:

```bash
docker run -d --name web --network red_clase nginx
```

3) Levantar Alpine y acceder al contenedor `web` por nombre:

```bash
docker run --rm -it --network red_clase alpine sh
```

Dentro de Alpine:

```sh
apk add --no-cache curl
curl http://web
```

Esto funciona porque Docker, en redes creadas por el usuario, añade un DNS interno que resuelve `web` → IP del contenedor.

---

### 7.6. Conectar y desconectar contenedores de redes

Conectar un contenedor a una red adicional:

```bash
docker network connect red_clase <contenedor>
```

Desconectar:

```bash
docker network disconnect red_clase <contenedor>
```

---

### 7.7. Ejemplo práctico real: App + Base de datos

En un escenario típico:

- Un contenedor ejecuta la API (o backend)
- Otro contenedor ejecuta PostgreSQL/MySQL
- Ambos están en la misma red privada
- Solo expones al host lo necesario (por ejemplo, el puerto de la API)

Ejemplo conceptual:

```bash
docker network create red_app

docker run -d --name db --network red_app -e POSTGRES_PASSWORD=pass postgres:16

docker run -d --name api --network red_app -e DB_HOST=db miapi:1.0
```

- `DB_HOST=db` funciona porque Docker resuelve el nombre `db` dentro de la red `red_app`.
- No necesitas publicar el puerto de la base de datos si solo la usa la API.

---

## 8. Docker Compose

Docker Compose sirve para definir y ejecutar **aplicaciones multi-contenedor** usando un archivo `docker-compose.yml`. En vez de lanzar contenedores con comandos largos (`docker run ...`), describes:

- Qué servicios existen (app, db, redis…)
- Qué imágenes usan o cómo se construyen
- Puertos, variables de entorno
- Volúmenes para persistencia
- Redes para comunicación interna

Y lo levantas todo con un solo comando.

---

### 8.1. ¿Por qué usar Compose?

Sin Compose, levantar una app real implica muchos comandos:

- Crear red
- Crear volumen
- Levantar base de datos con variables
- Levantar backend apuntando a la DB
- Publicar puertos
- Asegurar que estén en la misma red

Con Compose, lo defines una vez y puedes repetirlo siempre.

---

### 8.2. Archivo `docker-compose.yml`: estructura básica

Un Compose típico tiene estas secciones:

- `services`: contenedores que vas a ejecutar
- `volumes`: volúmenes declarados
- `networks`: redes declaradas (opcional, Compose crea una por defecto)

Ejemplo mínimo con un servicio:

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
```

Levantar:

```bash
docker compose up -d
```

Parar y borrar contenedores/red por defecto:

```bash
docker compose down
```

---

### 8.3. Servicios: `image` vs `build`

#### 8.3.1. Usando una imagen existente

```yaml
services:
  web:
    image: nginx:1.25
    ports:
      - "8080:80"
```

#### 8.3.2. Construyendo desde un Dockerfile

Estructura:

```
miapp/
  Dockerfile
  app.py
  docker-compose.yml
```

Compose:

```yaml
services:
  app:
    build: .
    ports:
      - "5000:5000"
```

Build + run:

```bash
docker compose up -d --build
```

---

### 8.4. Variables de entorno

Puedes definir variables con `environment`:

```yaml
services:
  api:
    image: miapi:1.0
    environment:
      - APP_ENV=prod
      - LOG_LEVEL=info
```

O usar un archivo `.env` (muy común):

`.env`:

```
POSTGRES_PASSWORD=pass
```

Compose:

```yaml
services:
  db:
    image: postgres:16
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
```

> Buen hábito: no subir `.env` a git si contiene secretos.

---

### 8.5. Volúmenes en Compose (persistencia)

Ejemplo con PostgreSQL:

```yaml
services:
  db:
    image: postgres:16
    environment:
      - POSTGRES_PASSWORD=pass
    volumes:
      - datos_pg:/var/lib/postgresql/data

volumes:
  datos_pg:
```

Aquí `datos_pg` es un volumen administrado por Docker. Si bajas los contenedores, el volumen puede permanecer (según el comando usado).

---

### 8.6. Bind mounts en Compose (desarrollo)

Muy usados para montar tu código local dentro del contenedor y evitar reconstruir en cada cambio.

Ejemplo típico Python:

```yaml
services:
  app:
    image: python:3.11
    working_dir: /app
    volumes:
      - ./:/app
    command: python app.py
```

Esto permite editar `app.py` en tu host y ejecutarlo en el contenedor.

---

### 8.7. Redes en Compose (crear tu propia red)

Por defecto, Docker Compose crea automáticamente una red (normalmente llamada algo como `<proyecto>_default`) y conecta ahí todos los servicios. Esto permite que los contenedores se comuniquen por **nombre de servicio** (DNS interno), por ejemplo `db`, `api`, etc.

Aun así, en proyectos reales es muy útil **definir tus propias redes**, por ejemplo para:

- Separar tráfico interno (backend ↔ base de datos) del tráfico público (backend ↔ navegador)
- Aislar servicios y mejorar seguridad
- Reutilizar una red concreta o controlar nombres y estructura

---

#### 8.7.1. Crear una red personalizada (la forma más común)

Define la red en el bloque `networks:` y asigna los servicios a esa red.

Ejemplo: una red interna llamada `red_app`:

```yaml
services:
  db:
    image: postgres:16
    environment:
      - POSTGRES_PASSWORD=pass
    networks:
      - red_app

  api:
    build: .
    environment:
      - DB_HOST=db
    depends_on:
      - db
    networks:
      - red_app

networks:
  red_app:
```

Qué ocurre aquí:
- Compose crea la red `red_app` al hacer `docker compose up`
- Ambos servicios quedan dentro de esa red
- `db` funciona como hostname accesible desde `api` porque **el nombre del servicio es el nombre DNS**

---

#### 8.7.2. Separar redes: pública y privada (patrón típico)

En arquitecturas reales, lo más habitual es:
- Red **privada**: db solo accesible por api
- Red **pública**: api accesible desde el host (por puertos)

```yaml
services:
  db:
    image: postgres:16
    environment:
      - POSTGRES_PASSWORD=pass
    networks:
      - red_privada

  api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DB_HOST=db
    depends_on:
      - db
    networks:
      - red_privada
      - red_publica

networks:
  red_privada:
  red_publica:
```

Ventaja:
- `db` no está en la red pública, por tanto queda más aislada
- `api` se comunica con `db` por `red_privada` y además expone servicio al host por `red_publica`

---

#### 8.7.3. Poner nombre fijo a la red (name) para identificarla mejor

Por defecto, Compose añade el prefijo del proyecto. Si quieres un nombre exacto:

```yaml
networks:
  red_app:
    name: red_app_clase
```

Ahora Docker creará la red con el nombre real `red_app_clase`.

---

#### 8.7.4. Usar una red ya existente (external)

Si quieres que el compose use una red creada previamente con Docker:

1) Crear red manualmente:

```bash
docker network create red_compartida
```

2) Declararla como externa:

```yaml
services:
  api:
    build: .
    networks:
      - red_compartida

networks:
  red_compartida:
    external: true
```

Esto es útil si:
- Varios `docker-compose.yml` deben compartir red
- Quieres conectar contenedores que no levanta el mismo compose

---


> [!IMPORTANT]  
> `depends_on` solo garantiza que Docker **inicie** el contenedor `db` antes que `api`, pero no garantiza que Postgres esté listo para aceptar conexiones.
> Para escenarios reales, lo habitual es:
> - Añadir `healthcheck` en la base de datos
> - O que la API reintente conexión (retry)


---

### 8.8. Comandos esenciales de Docker Compose

Levantar (foreground):

```bash
docker compose up
```

Levantar (background):

```bash
docker compose up -d
```

Reconstruir imágenes:

```bash
docker compose up -d --build
```

Ver servicios y estado:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs
docker compose logs -f
```

Ejecutar comandos dentro de un servicio:

```bash
docker compose exec <servicio> bash
```

Parar y borrar contenedores/red:

```bash
docker compose down
```

Borrar también volúmenes (cuidado):

```bash
docker compose down -v
```

---
