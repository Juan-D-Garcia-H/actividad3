# Actividad 3 - Automatización de Base de Datos con Python

## 📌 Descripción

Este script automatiza la creación y el poblado de una tabla MySQL usando **SQLAlchemy** y **Faker**.  
Genera **100,000 registros** en una tabla llamada `personas_juan` (cambia `juan` por tu nombre).

**Características principales:**

- Conexión segura usando variables de entorno (`.env`)
- Creación automática de la tabla si no existe
- Generación de datos realistas con Faker (nombres, emails, direcciones, etc.)
- Inserción por lotes para optimizar rendimiento (5,000 registros por lote)
- Datos localizados para Colombia (ciudades, teléfonos, direcciones)
- Manejo de errores y validación de conexión

## 🛠 Requisitos previos

- **Python 3.10 o superior**
- **MySQL** instalado y corriendo
- **DBeaver** (opcional, para verificación visual)
- **Git** (opcional, para clonar el repositorio)

## 📦 Instalación y Configuración

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/Juan-D-Garcia-H/actividad3.git
cd actividad3
```
