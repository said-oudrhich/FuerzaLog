# FuerzaLog

Aplicación web Django para registrar entrenamientos de gimnasio, seguir el progreso físico y gestionar rutinas de forma segura mediante autenticación de usuarios.

## Características

- Registro y autenticación de usuarios
- CRUD completo de entrenamientos y rutinas
- Upload de imágenes para cada entrenamiento
- Búsqueda de entrenamientos por título
- Diseño responsive con Bootstrap 5
- Protección de datos por usuario

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/said-oudrhich/FuerzaLog.git
cd FuerzaLog
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar base de datos:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Crear superusuario:
```bash
python manage.py createsuperuser
```

6. Iniciar servidor:
```bash
python manage.py runserver
```

## Tecnologías

- Django 4.x
- Bootstrap 5
- SQLite / PostgreSQL
- Python 3.x

## Despliegue

PythonAnywhere: https://said-oudrhich.pythonanywhere.com

## Autor

Said Oudrhich
