web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn fuerzalog.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 1 --access-logfile - --error-logfile -
