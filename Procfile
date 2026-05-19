web: python manage.py migrate && gunicorn fuerzalog.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 1 --access-logfile - --error-logfile -
