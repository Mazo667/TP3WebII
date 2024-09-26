# Aplicación de Blog en Django

Esta es una aplicación de blog simple construida con Django. Permite a los usuarios crear, editar, eliminar y ver publicaciones de blog. Los usuarios también pueden registrarse e iniciar sesión para gestionar sus publicaciones.

## Tabla de Contenidos

- [Características](#características)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Guía para Comenzar](#guía-para-comenzar)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración del Entorno](#configuración-del-entorno)
- [Configuración de Ajustes de Correo Electrónico](#configuración-de-ajustes-de-correo-electrónico)
- [Ejecutando la Aplicación](#ejecutando-la-aplicación)

## Características

- Autenticación de usuarios (registro, inicio de sesión, cierre de sesión).
- Crear, leer, actualizar y eliminar publicaciones de blog.
- Sistema de etiquetas para las publicaciones.
- Estado de publicación y borrador para las publicaciones.
- Diseño responsivo utilizando Bootstrap.

## Tecnologías Utilizadas

- Django
- Python
- SQLite
- Bootstrap (para el estilo del frontend)

## Guía para Comenzar

### Requisitos Previos

Asegúrate de tener instalado lo siguiente:

- Python 3.x
- pip (gestor de paquetes de Python)
- Virtualenv (opcional pero recomendado)

### Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tuusuario/django-blog.git
   cd django-blog
    ```

2. Crea un entorno virtual (opcional pero recomendado):
    ```bash
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. Instala los paquetes requeridos:
    ```bash
    pip install -r requirements.txt
    ```

### Configuración del Entorno

1. Crea un archivo '.env' en la raíz de tu directorio del proyecto para almacenar variables de entorno y completa los siguientes campos:<br>
    <span>EMAIL_HOST_USER=tu_email@gmail.com<br>
    EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxx<br>
    DEFAULT_FROM_EMAIL=Mi Blog <tu_email@gmail.com></span>

### Ejecutando la Aplicación

1. Aplica las migraciones para configurar tu base de datos:
    ```bash
    python manage.py migrate
    ```

2. Crea un superusuario para acceder al panel administrativo:
    ```bash
    python manage.py createsuperuser
    ```

3. Ejecuta el servidor de desarrollo:
    ```bash
    python manage.py runserver
    ```

4. Abre tu navegador y navega a http://127.0.0.1:8000 para acceder a la aplicación.
