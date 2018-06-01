from .base import *  # noqa


# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

DATABASES = {
    'default': env.db('DATABASE_URL', default='mysql://root:root@localhost:3306/liBlog'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# Only debug
# ------------------------------------------------------------------------------
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
INSTALLED_APPS += [
    'debug_toolbar',
]
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]
