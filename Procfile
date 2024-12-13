release: python manage.py collectstatic --noinput && python manage.py upload_static_to_s3 && python manage.py upload_media_to_s3
web: gunicorn ferociousfitness.wsgi