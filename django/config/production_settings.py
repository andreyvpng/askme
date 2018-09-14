from config.common_settings import *

DEBUG = False

assert SECRET_KEY is not None, (
    'Please provide DJANGO_SECRET_KEY '
    'environment variable with a value')

ALLOWED_HOSTS += [
    os.getenv('DJANGO_ALLOWED_HOSTS'),
]
