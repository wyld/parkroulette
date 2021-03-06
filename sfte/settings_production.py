from settings import MIDDLEWARE_CLASSES, INSTALLED_APPS

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar',)
INTERNAL_IPS = ('217.12.211.117', '107.3.149.69')

GEOIP_DEBUG = False

DEBUG = False
ALLOWED_HOSTS = ['www.parkroulette.com', 'parkroulette.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'parkroulette2012',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
    }
}

ENABLE_ANALYTICS = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'addresses': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'paths': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'tickets': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
}