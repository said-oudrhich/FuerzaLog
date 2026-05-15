#!/bin/bash
set -e

python manage.py migrate --run-syncdb
python manage.py collectstatic --noinput
echo "Arrancando en puerto: ${PORT}"
exec gunicorn fuerzalog.wsgi --bind "0.0.0.0:${PORT}" --workers 2 --log-file - --access-logfile -
