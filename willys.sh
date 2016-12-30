#!/bin/bash

source venv/bin/activate

case "$1" in
    develop)
        python manage.py runserver
        ;;
    migrate)
        python manage.py migrate production
        ;;
    deploy)
        pip install -r requirements.txt && python manage.py bower && python manage.py collectstatic --noinput --clear && supervisorctl restart uwsgi-willys
        ;;
  *)
        echo "Usage: willys.sh {develop|deploy|migrate}" >&2
        exit 1
        ;;
esac

exit 0
