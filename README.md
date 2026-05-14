# FuerzaLog

Aplicación web Django para registrar entrenamientos de gimnasio al estilo de la app Hevy. Permite crear workouts, añadir ejercicios con series individuales (peso, repeticiones y tipo), gestionar rutinas de entrenamiento y consultar el historial de cada ejercicio.

## Características

- Registro e inicio de sesión de usuarios
- Catálogo global de ejercicios gestionado por el administrador
- Ejercicios personalizados por usuario
- Búsqueda de ejercicios por nombre
- Rutinas con ejercicios y series objetivo (plantilla)
- Workouts reales con ejercicios y series individuales (peso, reps, tipo)
- Historial de series por ejercicio
- Protección de datos: cada usuario solo ve y edita lo suyo
- Diseño responsive con Bootstrap 5

## Modelo de datos

```
GrupoMuscular
Ejercicio  (global si usuario=null, personal si usuario=<user>)

Rutina ── RutinaEjercicio ── SerieRutina   (plantilla)
Workout ── WorkoutEjercicio ── Serie        (registro real)
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

3. Aplicar migraciones y cargar datos iniciales:
```bash
python manage.py migrate
python manage.py loaddata entrenamientos/fixtures/datos_iniciales.json
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
2. Crea un **Workout** desde el botón "+ Workout" del navbar
3. Dentro del workout, añade ejercicios del catálogo
4. Para cada ejercicio añade series indicando tipo, peso y repeticiones
5. Consulta el historial de cualquier ejercicio en **Ejercicios → Ver historial**

## Tecnologías

- Python 3.13
- Django 6.x
- Bootstrap 5
- SQLite

## Despliegue

PythonAnywhere: https://said-oudrhich.pythonanywhere.com

## Autor

Said Oudrhich
