"""
WSGI config for ferociousfitness project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

import dotenv

if os.path.exists(".env"):
    dotenv.load_dotenv(".env")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ferociousfitness.settings")

application = get_wsgi_application()
