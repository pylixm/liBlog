from .base import *  # noqa

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])
# END SITE CONFIGURATION

DATABASES = {
    'default': env.db('DATABASE_URL', default='mysql://root:root@db:3306/liblog'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


INSTALLED_APPS += ['gunicorn', ]

