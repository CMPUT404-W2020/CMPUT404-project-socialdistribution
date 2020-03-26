release: python3 manage.py makemigrations sd
release: python3 manage.py migrate auth
release: python3 manage.py migrate --run-syncdb
web: python3 manage.py runserver "0.0.0.0:$PORT"
web: gunicorn social_distribution.wsgi:application --log-file -
