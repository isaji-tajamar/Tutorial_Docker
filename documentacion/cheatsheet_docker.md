# Docker Cheatsheet (Completa)

## Índice
1. [Ayuda y versión](#1-ayuda-y-versión)
2. [Imágenes](#2-imágenes)
3. [Contenedores](#3-contenedores)
4. [Puertos y exposición](#4-puertos-y-exposición)
5. [Volúmenes y bind mounts (persistencia)](#5-volúmenes-y-bind-mounts-persistencia)
6. [Redes](#6-redes)
7. [Dockerfile y build](#7-dockerfile-y-build)
8. [Docker Compose (resumen práctico)](#8-docker-compose-resumen-práctico)
9. [Docker Hub y registries](#9-docker-hub-y-registries)
10. [Limpieza y mantenimiento](#10-limpieza-y-mantenimiento)
11. [Trucos útiles](#11-trucos-útiles)
12. [Plantillas rápidas](#12-plantillas-rápidas)


## 1) Ayuda y versión
```
docker --version
docker version
docker info
docker help
docker <comando> --help
```

## 2) Imágenes

### Buscar, descargar, listar
```
docker search nginx
docker pull nginx:latest
docker images
docker image ls
docker image ls -a
```

### Detalles, historial, capas
```
docker inspect nginx:latest
docker history nginx:latest
```

### Etiquetar y renombrar
```
docker tag nginx:latest miusuario/nginx:1.0
```

### Eliminar
```
docker rmi nginx:latest
docker image rm nginx:latest
docker image prune                  # imágenes dangling
docker image prune -a               # imágenes no usadas
```

### Guardar y cargar (offline)
```
docker save -o nginx.tar nginx:latest
docker load -i nginx.tar
```

## 3) Contenedores

### Ejecutar (run)
```
docker run nginx
docker run -it ubuntu bash
docker run -d nginx
docker run --name web -d -p 8080:80 nginx
docker run --rm -it ubuntu bash
docker run -e ENV=prod ubuntu env
```

### Listar
```
docker ps
docker ps -a
docker ps -q
docker ps -aq
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Iniciar, parar, reiniciar
```
docker start web
docker stop web
docker restart web
docker kill web
```

### Logs y métricas
```
docker logs web
docker logs -f web
docker logs --tail 100 web
docker stats
docker top web
```

### Ejecutar comandos dentro (exec)
```
docker exec -it web sh
docker exec -it web bash
docker exec web ls -la /usr/share/nginx/html
```

### Inspección
```
docker inspect web
docker inspect --format='{{.State.Status}}' web
docker port web
docker diff web
```

### Copiar archivos
```
docker cp local.txt web:/tmp/local.txt
docker cp web:/var/log/nginx/access.log ./access.log
```

### Renombrar
```
docker rename web web_prod
```

### Eliminar
```
docker rm web                     # contenedor parado
docker rm -f web                  # forzar
docker container prune            # elimina parados
```

### Exportar e importar contenedores (filesystem)
```
docker export web > web.tar
docker import web.tar miimagen:webfs
```

## 4) Puertos y exposición

### Publicar puertos
```
docker run -d -p 8080:80 nginx              # host:contenedor
docker run -d -p 127.0.0.1:8080:80 nginx    # solo localhost
docker run -d -P nginx                      # puertos aleatorios
```

### Ver mapeos
```
docker ps
docker port <contenedor>
```

## 5) Volúmenes y bind mounts (persistencia)

### Volúmenes (recomendado)
```
docker volume ls
docker volume create datos_db
docker volume inspect datos_db
docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=pass -v datos_db:/var/lib/mysql mysql:8
docker volume rm datos_db
docker volume prune
```

### Bind mounts (host -> contenedor)
```
docker run -it --rm -v /ruta/host:/app ubuntu bash
docker run -it --rm -v "$(pwd)":/app ubuntu bash
```

### Modo lectura/escritura
```
docker run -it --rm -v "$(pwd)":/app:ro ubuntu bash   # solo lectura
docker run -it --rm -v "$(pwd)":/app:rw ubuntu bash   # lectura/escritura
```

## 6) Redes

### Listar y crear
```
docker network ls
docker network create mi_red
docker network inspect mi_red
```

### Conectar contenedores a una red
```
docker run -d --name db --network mi_red postgres:16
docker run -d --name app --network mi_red -p 8080:8080 miapp:latest
```

### Conectar/desconectar contenedores existentes
```
docker network connect mi_red web
docker network disconnect mi_red web
```

### Eliminar
```
docker network rm mi_red
docker network prune
```

### Tipos comunes
- bridge: por defecto local, para contenedores en una misma máquina.
- host: usa la red del host (Linux).
- none: sin red.

## 7) Dockerfile y build

### Build básico
```
docker build -t miapp:1.0 .
docker build -t miapp:1.0 -f Dockerfile .
```

### Build sin cache o con progreso
```
docker build --no-cache -t miapp:1.0 .
docker build --progress=plain -t miapp:1.0 .
```

### Build args
```
docker build --build-arg ENV=prod -t miapp:prod .
```

### Ver builder y cache (BuildKit)
```
docker builder ls
docker builder prune
```

## 8) Docker Compose (resumen práctico)

### Comandos habituales
```
docker compose version
docker compose up
docker compose up -d
docker compose down
docker compose down -v                 # elimina volúmenes declarados
docker compose ps
docker compose logs
docker compose logs -f
docker compose restart
docker compose pull
docker compose build
docker compose exec <servicio> sh
docker compose run --rm <servicio> <cmd>
```

### Usar otro fichero
```
docker compose -f docker-compose.yml up -d
docker compose -f docker-compose.prod.yml up -d
```

### Variables de entorno
```
docker compose --env-file .env up -d
```

## 9) Docker Hub y registries

### Login/logout
```
docker login
docker logout
```

### Publicar imagen (push)
```
docker tag miapp:1.0 miusuario/miapp:1.0
docker push miusuario/miapp:1.0
```

### Descargar (pull)
```
docker pull miusuario/miapp:1.0
```

## 10) Limpieza y mantenimiento

### Uso de disco
```
docker system df
```

### Limpieza general
```
docker system prune               # contenedores parados, redes no usadas, cache
docker system prune -a            # también imágenes no usadas
docker system prune --volumes     # incluye volúmenes no usados
```

### Prunes específicos
```
docker container prune
docker image prune
docker network prune
docker volume prune
docker builder prune
```

## 11) Trucos útiles

### Entrar en un contenedor con shell disponible
```
docker exec -it <contenedor> sh
docker exec -it <contenedor> bash
```

### Parar y borrar todo (cuidado)
```
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
```

### Borrar todas las imágenes (cuidado)
```
docker rmi -f $(docker images -q)
```

## 12) Plantillas rápidas

### Web Nginx
```
docker run -d --name web -p 8080:80 nginx
```

### Ubuntu interactivo
```
docker run -it --rm ubuntu bash
```

### Postgres con volumen
```
docker volume create pgdata
docker run -d --name pg -e POSTGRES_PASSWORD=pass -p 5432:5432 -v pgdata:/var/lib/postgresql/data postgres:16
```

### MySQL con volumen
```
docker volume create mysqldata
docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=pass -p 3306:3306 -v mysqldata:/var/lib/mysql mysql:8
```
