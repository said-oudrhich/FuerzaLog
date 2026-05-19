# FuerzaLog

Aplicación web Django para registrar entrenamientos de gimnasio. Permite crear entrenamientos, añadir ejercicios con series (peso, repeticiones y tipo), gestionar rutinas y consultar el historial de cada ejercicio.

## Características

- Registro e inicio de sesión de usuarios
- Catálogo global de ejercicios gestionado por el administrador
- Ejercicios personalizados por usuario
- Búsqueda de ejercicios por nombre
- Rutinas con ejercicios y series objetivo (plantilla)
- Entrenamientos con ejercicios y series (peso, repeticiones y tipo)
- Historial de series por ejercicio
- Subida de imágenes
- Protección de datos: cada usuario solo ve y edita lo suyo
- Diseño adaptable con Bootstrap 5

## Modelo de datos

```
GrupoMuscular
Ejercicio  (global si admin, personal por usuario)

Rutina ── RutinaEjercicio ── SerieRutina   (plantilla)
Entrenamiento ── EntrenamientoEjercicio ── Serie  (entreno real)
```

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/said-oudrhich/FuerzaLog.git
cd FuerzaLog
```

2. Crear entorno virtual e instalar dependencias:
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

3. Aplicar migraciones:
```bash
python manage.py migrate
```

4. Crear superusuario:
```bash
python manage.py createsuperuser
```

5. Iniciar servidor:
```bash
python manage.py runserver
```

## Uso rápido

1. Regístrate o inicia sesión
2. Crea un **entrenamiento** desde el menú superior
3. Dentro del entrenamiento, añade ejercicios del catálogo
4. Para cada ejercicio añade series indicando tipo, peso y repeticiones
5. Consulta el historial de cualquier ejercicio en **Ejercicios > Ver historial**

## Tecnologías

- Python 3.x
- Django 5.x
- Bootstrap 5
- SQLite
