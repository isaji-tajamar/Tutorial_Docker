# README — Curso / Clase de Introducción a Docker

Este repositorio contiene los materiales de la clase de introducción a **Docker**, incluyendo guías de instalación, configuraciones iniciales y recursos complementarios. El objetivo es que cualquier estudiante pueda preparar su entorno de trabajo desde cero, especialmente si utiliza **Windows con WSL 2**.

---

## 1. Objetivo del repositorio

Este repositorio proporciona:

- Guías detalladas para instalar **WSL 2 + Ubuntu 22.04 LTS**, la base recomendada para entornos de desarrollo modernos.
- Instrucciones completas para instalar **Docker Engine** dentro de Ubuntu en WSL.
- Material adicional para comprender los fundamentos de Docker y preparar el entorno para prácticas y ejercicios.

Estas guías permiten que todos los estudiantes trabajen en un entorno homogéneo, evitando problemas típicos de Docker Desktop, dependencias rotas o configuraciones inconsistentes.

---

## 2. Guías de instalación incluidas

A continuación se encuentran los dos documentos principales que deberás revisar antes de comenzar la clase:

---

### Guía 1 — Instalación de Ubuntu 22.04 LTS en WSL 2

Esta guía explica paso a paso cómo:

- Activar WSL 2 en Windows  
- Instalar Ubuntu 22.04 LTS  
- Configurar correctamente la distribución  

**Guía:**  
[Instalación WSL con Ubuntu 22.04 LTS](guias_instalacion/instalacion_wsl_ubuntu_22_04.md)

---

### Guía 2 — Instalación de Docker en Ubuntu 22.04 (WSL)

Incluye:

- Instalación de Docker Engine y Docker CLI  
- Configuración de systemd en WSL  
- Permisos para ejecutar Docker sin sudo  
- Pruebas iniciales y primeros contenedores  
- Instalación opcional de Docker Compose  

**Guía:**  
[Instalación Docker en Ubuntu 22.04 LTS](guias_instalacion/instalacion_docker_wsl_ubuntu_22_04.md)

---

## 3. Requisitos previos para la clase

Antes de comenzar la sesión, asegúrate de:

- Tener **Windows 10/11** con soporte para WSL2  
- Haber seguido completamente ambas guías  
- Probar que Docker funciona ejecutando:

```bash
docker run hello-world
```

- Comprobar que Docker Compose está disponible:

```bash
docker compose version
```

Si ambos comandos funcionan, tu entorno está listo para la clase.
