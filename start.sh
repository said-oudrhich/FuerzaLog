#!/bin/bash
set -e

python manage.py migrate --run-syncdb
python manage.py collectstatic --noinput
exec gunicorn fuerzalog.wsgi --bind "0.0.0.0:${PORT:-8000}" --workers 2 --log-file -
