## Ejercicios prácticos del curso (por apartados, fusionando conceptos)

> [!IMPORTANT] Reglas generales:
> En todos los ejercicios, documenta los comandos que uses y el resultado (captura o salida).

---

### Ejercicio 1, Imágenes + contenedores + capas (inspección y práctica)

**Objetivo:** entender “imagen vs contenedor”, capas y cómo se ejecuta algo real.

1. Descarga una imagen base y otra de aplicación:
   - `docker pull ubuntu:22.04`
   - `docker pull nginx:1.25`
2. Ejecuta un contenedor efímero y otro persistente:
   - `docker run --rm ubuntu:22.04 echo "hola"`
   - `docker run -d --name web nginx:1.25`
3. Inspecciona:
   - `docker image ls`
   - `docker ps`
   - `docker inspect web`
4. Demuestra la capa de escritura:
   - `docker exec -it web sh` (o `bash` si existe)
   - crea un archivo dentro
   - borra el contenedor y crea otro: verifica que el archivo no está

**Entregable:** explicación corta + comandos.

---

### Ejercicio 2, Persistencia: volúmenes y bind mounts (en un mismo ejercicio)

**Objetivo:** comprobar qué se pierde y qué se conserva.

1. Volumen:
   - crea volumen `datos_app`
   - monta en `/data` en un contenedor ubuntu
   - crea `archivo.txt` y comprueba que persiste tras borrar el contenedor
2. Bind mount:
   - crea una carpeta `./shared`
   - monta `./shared` en `/app`
   - crea un archivo desde el contenedor y comprueba que aparece en tu host
3. (Extra) monta en `:ro` y comprueba que no puedes escribir.

**Entregable:** diferencias prácticas entre volumen y bind mount.

---

### Ejercicio 3, Dockerfile + build + run (y buenas prácticas mínimas)

**Objetivo:** construir tu propia imagen y ejecutarla como contenedor.

1. Crea un proyecto mínimo (elige uno):
   - Opción A: FastAPI “Hello”
   - Opción B: Python script que imprima info del entorno
2. Crea Dockerfile con:
   - `FROM` con tag específico (ej: `python:3.11-slim`)
   - `WORKDIR`
   - `COPY`
   - `RUN` (instalar dependencias si aplica)
   - `EXPOSE` si es web
   - `CMD`
3. Build:
   - `docker build -t tuapp:1.0 .`
4. Run:
   - `docker run --rm tuapp:1.0`
   - si es web: `docker run --rm -p 8000:8000 tuapp:1.0`

**Entregable:** Dockerfile + explicación de cada línea.

---

### Ejercicio 4, Versionado y etiquetado + push/pull (sin entrar aún en privados)

**Objetivo:** usar tags y entender por qué importan.

1. Re-etiqueta tu imagen del ejercicio 4:
   - `tuapp:1.0.0`, `tuapp:1.0.1`, `tuapp:dev`
2. Lista imágenes y comprueba el “mismo ID” o diferencias según el caso:
   - `docker image ls`
3. Explica cuándo usarías:
   - SemVer (`1.2.3`)
   - entorno (`dev`, `prod`)
   - commit (`git-xxxxxx`)

**Entregable:** tabla de tags que has creado y qué significan.

---

### (OPCIONAL) Ejercicio 5, Docker Hub: publicar tu imagen (pública o privada) + recuperar en “limpio”

> [!IMPORTANT]
> Este ejercicio es **OPCIONAL PERO MUY RECOMENDABLE**

**Objetivo:** experimentar el flujo real de compartir imágenes.

1. Haz login:
   - `docker login`
2. Etiqueta tu imagen para Docker Hub:
   - `TUUSUARIO/tuapp:1.0.0`
3. Push:
   - `docker push TUUSUARIO/tuapp:1.0.0`
4. Simula “otro PC”:
   - borra la imagen local: `docker image rm ...`
   - pull de nuevo: `docker pull TUUSUARIO/tuapp:1.0.0`
   - ejecútala otra vez

**Entregable:** enlace al repo (si es público) o captura de Docker Hub.

---

### Ejercicio 6, Redes: aislar servicios y comunicar por hostname

**Objetivo:** entender redes bridge, DNS interno y exposición de puertos.

1. Crea una red:
   - `docker network create red_prueba`
2. Levanta 2 contenedores en esa red:
   - `nginx` llamado `web`
   - `alpine` para hacer requests
3. Desde alpine, haz `curl http://web` (por nombre).
4. Ahora publica `web` a tu host:
   - `-p 8080:80` y comprueba acceso desde navegador.

**Entregable:** explicación de “por nombre dentro de red” vs “por puerto en host”.

---