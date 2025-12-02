# README — Curso / Clase de Introducción a Docker

Este repositorio contiene los materiales de la clase de introducción a **Docker**, incluyendo guías de instalación, documentación teórica y una **demo práctica** con Docker Compose. El objetivo es que cualquier estudiante pueda preparar su entorno desde cero, especialmente en **Windows con WSL 2 + Ubuntu 22.04 LTS**.

- Todo lo referente a **teoría/clase** está en la carpeta: `documentacion/`
- Todo lo referente a la **demo** está en la carpeta: `demo/`

---

## 1. Objetivo del repositorio

Este repositorio proporciona:

- Guías detalladas para instalar **WSL 2 + Ubuntu 22.04 LTS** (entorno base recomendado).
- Instrucciones completas para instalar **Docker Engine** dentro de Ubuntu en WSL.
- Documentación para comprender los conceptos clave de Docker (imágenes, contenedores, redes, volúmenes, compose, etc.).
- Una demo completa para practicar Docker Compose con una arquitectura realista.

Estas guías permiten que todo el alumnado trabaje en un entorno homogéneo, evitando problemas típicos de Docker Desktop, dependencias rotas o configuraciones inconsistentes.

---

## 2. Guías de instalación incluidas

Antes de la clase, revisa y completa estas guías:

### Guía 1 — Instalación de Ubuntu 22.04 LTS en WSL 2

- Activar WSL 2 en Windows
- Instalar Ubuntu 22.04 LTS
- Configurar correctamente la distribución

**Guía:**  
[Instalación WSL con Ubuntu 22.04 LTS](guias_instalacion/instalacion_wsl_ubuntu_22_04.md)

### Guía 2 — Instalación de Docker en Ubuntu 22.04 (WSL)

Incluye:

- Instalación de Docker Engine y Docker CLI
- Configuración de systemd en WSL
- Permisos para ejecutar Docker sin sudo
- Pruebas iniciales y primeros contenedores
- Instalación y verificación de Docker Compose

**Guía:**  
[Instalación Docker en Ubuntu 22.04 LTS](guias_instalacion/instalacion_docker_wsl_ubuntu_22_04.md)

---

## 3. Requisitos previos para la clase

Antes de comenzar la sesión, asegúrate de:

- Tener **Windows 10/11** con soporte para WSL 2
- Haber seguido completamente ambas guías de instalación
- Probar que Docker funciona ejecutando:

```bash
docker run hello-world
```

- Comprobar que Docker Compose está disponible:

```bash
docker compose version
```

Si ambos comandos funcionan, tu entorno está listo para la clase.

---

## 4. Documentación de la clase (teoría)

En la carpeta `documentacion/` encontrarás los materiales teóricos y apuntes para la clase (componentes, imágenes, contenedores, redes, volúmenes, dockerfiles, compose, etc.). En este caso está todo en el archivo [clase_docker.md](documentacion/clase_docker.md). También encontrarás una cheatsheet con comandos de docker.

---

## 5. Demo práctica con Docker Compose — `demo/`

En la carpeta `demo/` hay una demo completa que despliega una aplicación multi-contenedor:

- **Postgres** (BBDD persistente con volumen)
- **FastAPI** (API conectada a Postgres)
- **Nginx** (servidor web simple que sirve un frontend y hace proxy a la API)

### 5.1. Qué se practica con la demo

- Redes en Compose (comunicación por nombre de servicio)
- Variables de entorno
- Volúmenes (persistencia)
- Reverse proxy (Nginx -> FastAPI)
- Endpoints GET/POST con integración real con BBDD

Para más información consulta el [README de la demo](demo/README.md).
