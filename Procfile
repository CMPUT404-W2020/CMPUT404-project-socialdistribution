release: python3 manage.py makemigrations admin
release: python3 manage.py makemigrations auth
release: python3 manage.py makemigrations contenttypes
release: python3 manage.py makemigrations sessions
release: python3 manage.py makemigrations messages
release: python3 manage.py makemigrations staticfiles
release: python3 manage.py makemigrations corsheaders
release: python3 manage.py makemigrations sdConfig
release: python3 manage.py makemigrations sd
release: python3 manage.py makemigrations rest_framework
release: python3 manage.py makemigrations
release: python3 manage.py migrate auth
release: python3 manage.py migrate
release: python3 manage.py migrate --run-syncdb
web: python3 manage.py runserver "0.0.0.0:$PORT"
web: gunicorn social_distribution.wsgi:application --log-file -
