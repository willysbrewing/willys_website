#!/bin/bash

source venv/bin/activate

case "$1" in
    develop)
        echo "not yet"
        ;;
    migrate)
        python manage.py migrate production
        ;;
    deploy)
        pip install -r requirements.txt && python manage.py collectstatic && supervisorctl restart uwsgi-willys
        ;;
  *)
        echo "Usage: willys.sh {develop|deploy|migrate}" >&2
        exit 1
        ;;
esac

exit 0
