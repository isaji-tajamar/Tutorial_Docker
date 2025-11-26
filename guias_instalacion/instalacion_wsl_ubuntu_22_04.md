# Instalación detallada de Ubuntu 22.04 LTS en WSL

## [Repositorio Completo](https://github.com/isaji-tajamar/Tutorial_Docker)

Este documento explica de manera **paso a paso y detallada** cómo instalar **Ubuntu 22.04 LTS** dentro de **Windows Subsystem for Linux (WSL 2)**.

---

# ¿Por qué Ubuntu 22.04 LTS?

Ubuntu 22.04 LTS es la versión más recomendada para proyectos de IA/Big Data porque:

- Tiene **compatibilidad total** con PyTorch, TensorFlow, JAX, CUDA, NumPy, Pandas, Spark, Hadoop y Airflow.
- Es **estable** y recibe soporte hasta 2027.
- Es la versión más probada en **WSL 2**, con compatibilidad con GPU a través de drivers NVIDIA.
- Tiene el ecosistema científico más maduro y fácil de instalar.

---

# 1. Verificación previa: ¿tienes WSL instalado?

Antes de instalar la distro, comprueba el estado de WSL:

```powershell
wsl --status
```

Si WSL no está instalado, verás mensajes indicando que faltan componentes. En ese caso, sigue los pasos siguientes.

---

# 2. Activar WSL 2 en Windows (instalación detallada)

WSL necesita dos características del sistema:

- **Windows Subsystem for Linux**
- **Virtual Machine Platform**

La forma más fácil y recomendada es usar:

```powershell
wsl --install
```

Este comando:

1. Activa automáticamente las características necesarias.
2. Instala WSL 2 (si no estaba instalado).
3. Descarga Ubuntu por defecto (puede ignorarse si luego instalas otra distribución).
4. Configura WSL 2 como versión por defecto.

### Si aparece un error

En caso de error, activa manualmente las características ejecutando:

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

Después, reinicia tu PC.

---

# 3. Ver distribuciones disponibles para instalar

```powershell
wsl --list --online
```

Ejemplo de salida:

```
NAME                FRIENDLY NAME
Ubuntu              Ubuntu (latest)
Ubuntu-22.04        Ubuntu 22.04 LTS
Ubuntu-24.04        Ubuntu 24.04 LTS
Debian              Debian GNU/Linux
kali-linux          Kali Linux
...
```

---

# 4. Instalar específicamente **Ubuntu 22.04 LTS**

Ejecuta:

```powershell
wsl --install -d Ubuntu-22.04
```

Esto hará tres cosas:

1. **Descargar la imagen oficial** desde Microsoft Store.
2. **Descomprimirla** dentro del almacenamiento de WSL.
3. **Configurar el entorno inicial**.

Cuando termine, verás un mensaje indicando que la instalación finalizó.

---

# 5. Primer inicio y configuración de Ubuntu 22.04

Cuando abras la distribución (desde el menú o ejecutando `ubuntu2204`), se configurará por primera vez:

1. Preparará el entorno de archivos interno.
2. Iniciará el entorno de usuario UNIX.
3. Te pedirá crear un usuario:

```
Enter new UNIX username: isaji
```

4. Finalmente te pedirá una contraseña UNIX (no se muestran caracteres al escribir):

```
New password:
Retype new password:
```

Este usuario será tu usuario principal dentro de Linux.

---

# 6. Actualizar completamente la distribución

Para tener tu Ubuntu optimizado y seguro, ejecuta:

```bash
sudo apt update
sudo apt upgrade -y
```

Esto:

- Actualiza índices de repositorios.
- Descarga paquetes nuevos.
- Instala versiones actualizadas del sistema.

---

# 7. Confirmar que estás usando Ubuntu 22.04 LTS

```bash
lsb_release -a
```

Debería mostrar:

```
Description: Ubuntu 22.04.* LTS
```

# 8. Comandos importantes de administración de WSL

## Ver distros instaladas
```powershell
wsl --list --verbose
```

## Establecer WSL 2 como predeterminado
```powershell
wsl --set-default-version 2
```

## Convertir Ubuntu 22.04 a WSL 2
```powershell
wsl --set-version Ubuntu-22.04 2
```

## Abrir la distro
```powershell
wsl
```

---

# 9. Desinstalar Ubuntu 22.04 (si fuese necesario)

```powershell
wsl --unregister Ubuntu-22.04
```

# 10. (Opcional) Instalar Docker
Si quieres seguir mi clase/presentación del lunes conmigo instala docker en tu máquina siguiendo esta guía: [instalación Docker en Ubuntu 22.04 LTS](instalacion_docker_wsl_ubuntu_22_04.md)

