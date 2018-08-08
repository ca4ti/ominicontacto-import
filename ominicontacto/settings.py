# -*- coding: utf-8 -*-

"""
Django settings for ominicontacto project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import subprocess

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 's1+*bfrvb@=k@c&9=pm!0sijjewneu5p5rojil#q+!a2y&as-4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'configuracion_telefonia_app',
    'crispy_forms',
    'compressor',
    'defender',
    'formtools',
    'ominicontacto_app',
    'reciclado_app',
    'reportes_app',
    'simple_history',
    'widget_tweaks',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'defender.middleware.FailedLoginMiddleware',
]


# django-compressor settings
COMPRESS_OFFLINE = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

ROOT_URLCONF = 'ominicontacto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [os.path.join(os.path.dirname(__file__),'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ominicontacto.wsgi.application'

# Password hashers available
# https://docs.djangoproject.com/en/1.9/topics/auth/passwords/

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 600
SESSION_SAVE_EVERY_REQUEST = True
# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Cordoba'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

# STATICFILES_DIRS = [
#   os.path.join(BASE_DIR, "static"),
# ]

AUTH_USER_MODEL = 'ominicontacto_app.User'

TEST_RUNNER = "tests.tests.ManagedModelTestRunner"
OML_TESTING_MODE = False

LOGIN_REDIRECT_URL = 'index'

OL_SIP_LIMITE_INFERIOR = 1000
OL_SIP_LIMITE_SUPERIOR = 3000


OL_NRO_TELEFONO_LARGO_MIN = 5
"""Largo minimo permitido de nros telefonicos"""

OL_NRO_TELEFONO_LARGO_MAX = 15
"""Largo maximo permitido de nros telefonicos"""

OL_MAX_CANTIDAD_CONTACTOS = 60000
"""Límite de contactos que pueden ser importados a la base de datos."""

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

OML_DUMP_HTTP_AMI_RESPONSES = False

# ==============================================================================
# Settings de DEPLOY (para ser customizados en distintos deploys)
#     Nota: Los settings que siguen, pueden (y algunos DEBEN) ser modificados
#        en los distintos ambientes / deploys
# ==============================================================================

# ==============================================================================
# DEPLOY -> IP OMNILEADS
# ==============================================================================

OML_OMNILEADS_IP = None
"""IP donde se encuentra kamailio-debian

Ejemplo:
    OML_OMNILEADS_IP = "172.16.20.241"
"""

# ==============================================================================
# DEPLOY -> Asterisk
# ==============================================================================

# parametros de conexion con base de datos mysql de asterisk
DATABASE_MYSQL_ASTERISK = {
    'BASE': None,
    'HOST': None,
    'USER': None,
    'PASSWORD': None,
}

OML_ASTERISK_HOSTNAME = None
OML_ASTERISK_REMOTEPATH = None
OML_SIP_FILENAME = None
OML_QUEUES_FILENAME = None
OML_BACKLIST_REMOTEPATH = None
OML_GLOBALS_VARIABLES_FILENAME = None
OML_RUTAS_SALIENTES_FILENAME = None
"""Path completo (absoluto) al archivo donde se debe generar queues

Ejemplos:

.. code-block:: python

    OML_ASTERISK_HOSTNAME = "root@192.168.1.23"
    OML_ASTERISK_REMOTEPATH = "/etc/asterisk/"
    OML_SIP_FILENAME = "/etc/asterisk/sip_fts.conf"
    OML_QUEUES_FILENAME = "/etc/asterisk/queues_fts.conf"
    OML_BACKLIST_REMOTEPATH  = "/var/spool/asterisk/"
    OML_GLOBALS_VARIABLES_FILENAME = "/etc/asterisk/extensions_fts_globals.conf"
    OML_RUTAS_SALIENTES_FILENAME = "/etc/asterisk/oml_extensions_outr.conf"
"""

OML_RELOAD_CMD = None
"""Comando a ejecutar para hacer reload de Asterisk

Ejemplo:

.. code-block:: python

    OML_RELOAD_CMD = ["/usr/bin/asterisk", "-x", "reload"]
"""

ASTERISK = {
    'USERNAME': None,  # Usuario para AMI
    'PASSWORD': None,  # Password para usuario para AMI
    'HTTP_AMI_URL': None,
    # URL usado por Daemon p/acceder a Asterisk AMI via HTTP
    # Ej:
    #    "http://1.2.3.4:7088"
}

TMPL_OML_AUDIO_CONVERSOR = None
"""Comando para convertir audios (wav a gsm)

Ejemplos:

.. code-block:: python

    TMPL_OML_AUDIO_CONVERSOR = ["sox", "<INPUT_FILE>", "<OUTPUT_FILE>"]

Para transformar WAV (cualquier formato) -> WAV (compatible con Asterisk):

.. code-block:: python

    TMPL_OML_AUDIO_CONVERSOR = ["sox", "-t", "wav", "<INPUT_FILE>",
        "-r", "8k", "-c", "1", "-e", "signed-integer",
        "-t", "wav", "<OUTPUT_FILE>"
    ]

"""

TMPL_OML_AUDIO_CONVERSOR_EXTENSION = None
"""Extension a usar para archivo generado por `TMPL_OML_AUDIO_CONVERSOR`

Ejemplo: `.wav` (con el . incluido):  el archivo `<OUTPUT_FILE>`
tendra la extension `.wav`
"""

OML_AUDIO_PATH_ASTERISK = None
"""Directory donde se guardan los audios de asterisk en el server de asterisk

Ejemplo:
    OML_WOMBAT_FILENAME = "/var/lib/asterisk/sounds/oml/"
"""

# ==============================================================================
# DEPLOY -> KAMAILIO
# ==============================================================================

OML_KAMAILIO_IP = None
"""IP donde se encuentra kamailio-debian

Ejemplo:
    OML_KAMAILIO_IP = "172.16.20.219/255.255.255.255"
"""

# ==============================================================================
# URL DE GRABACIONES DE ELASTIX
# ==============================================================================

OML_GRABACIONES_URL = None
"""Url de donde buscar las grabaciones de las llamadas

Ejemplo:
    OML_GRABACIONES_URL = "http://172.16.20.222/grabaciones"
"""

# ==============================================================================
# URL DE SUPERVISION
# ==============================================================================

OML_SUPERVISION_URL = None
"""Url de donde se encuentra la supervision

Ejemplo:
    OML_SUPERVISION_URL = "http://172.16.20.222:8090/Omnisup/index.php"
"""

# ==============================================================================
# WOMBAT Config
# ==============================================================================

OML_WOMBAT_URL = None
"""Url de discador de Wombat

Ejemplo:
    OML_WOMBAT_URL = "http://172.16.20.222/wombat"
"""


OML_WOMBAT_FILENAME = None
"""Directory donde se guardan los json de config de wombat

Ejemplo:
    OML_WOMBAT_FILENAME = "/home/freetech/"
"""

OML_WOMBAT_USER = None
OML_WOMBAT_PASSWORD = None
"""
User y password por el cual se conectan con la api de WOMBAT DIALER
Ejemplo:
    OML_WOMBAT_USER = "user_test"
    OML_WOMBAT_PASSWORD = "user123"
"""

CALIFICACION_REAGENDA = None

# ==============================================================================
# Import de `oml_settings_local`
# ==============================================================================

try:
    from oml_settings_local import *
    # definir LOCAL_APPS en oml_settings_local, para insertar plugins de django que
    # sólo serán usados en ambientes de desarrollo y de testing, si no se tienen plugins
    # dejar LOCAL_APPS = []
    INSTALLED_APPS += LOCAL_APPS

    if DJANGO_DEBUG_TOOLBAR:
        MIDDLEWARE_CLASSES += [
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        ]
except ImportError as e:
    print "# "
    print "# ERROR"
    print "# "
    print "#   No se pudo importar el modulo"
    print "#       `oml_settings_local`"
    print "# "
    raise Exception("No se pudo importar oml_settings_local")

# ~~~~~ Check OML_ASTERISK_HOSTNAME

assert OML_ASTERISK_HOSTNAME is not None, \
    "Falta definir setting para OML_ASTERISK_HOSTNAME"

# ~~~~~ Check OML_ASTERISK_REMOTEPATH

assert OML_ASTERISK_REMOTEPATH is not None, \
    "Falta definir setting para OML_ASTERISK_REMOTEPATH"

# ~~~~~ Check OML_SIP_FILENAME

assert OML_SIP_FILENAME is not None, \
    "Falta definir setting para OML_SIP_FILENAME"

# ~~~~~ Check OML_QUEUES_FILENAME

assert OML_QUEUES_FILENAME is not None, \
    "Falta definir setting para OML_QUEUES_FILENAME"

# ~~~~~ Check ASTERISK

for key in ('BASE', 'PASSWORD', 'HOST', 'USER'):
    assert key in DATABASE_MYSQL_ASTERISK, \
        "Falta key '{0}' en configuracion de la base de datos de ASTERISK".\
        format(key)
    assert DATABASE_MYSQL_ASTERISK[key] is not None, \
        "Falta key '{0}' en configuracion de la base de datos ASTERISK".\
        format(key)

for key in ('USERNAME', 'PASSWORD', 'HTTP_AMI_URL'):
    assert key in ASTERISK, \
        "Falta key '{0}' en configuracion de ASTERISK".\
        format(key)
    assert ASTERISK[key] is not None, \
        "Falta key '{0}' en configuracion de ASTERISK".\
        format(key)

# ~~~~~ Check OML_RELOAD_CMD

assert OML_RELOAD_CMD is not None, \
    "Falta definir setting para OML_RELOAD_CMD"


# ~~~~~ Check OML_GRABACIONES_URL

assert OML_GRABACIONES_URL is not None, \
    "Falta definir setting para OML_GRABACIONES_URL"

# ~~~~~ Check OML_GRABACIONES_URL

assert OML_SUPERVISION_URL is not None, \
    "Falta definir setting para OML_SUPERVISION_URL"

# ~~~~~ Check OML_KAMAILIO_IP

assert OML_KAMAILIO_IP is not None, \
    "Falta definir setting para OML_KAMAILIO_IP"

# ~~~~~ Check OML_WOMBAT_URL

assert OML_WOMBAT_URL is not None, \
    "Falta definir setting para OML_WOMBAT_URL"

# ~~~~~ Check OML_WOMBAT_FILENAME

assert OML_WOMBAT_FILENAME is not None, \
    "Falta definir setting para OML_WOMBAT_FILENAME"

# ~~~~~ Check OML_RUTAS_SALIENTES_FILENAME

assert OML_RUTAS_SALIENTES_FILENAME is not None, \
    "Falta definir setting para OML_RUTAS_SALIENTES_FILENAME"

# ~~~~~ Check OML_WOMBAT_USER

assert OML_WOMBAT_USER is not None, \
    "Falta definir setting para OML_WOMBAT_USER"

# ~~~~~ Check OML_WOMBAT_PASSWORD

assert OML_WOMBAT_PASSWORD is not None, \
    "Falta definir setting para OML_WOMBAT_PASSWORD"


# ~~~~~ Check OML_OMNILEADS_IP

assert OML_OMNILEADS_IP is not None, \
    "Falta definir setting para OML_OMNILEADS_IP"


# ~~~~~ Check OML_BACKLIST_REMOTEPATH

assert OML_BACKLIST_REMOTEPATH is not None, \
    "Falta definir setting para OML_BACKLIST_REMOTEPATH"


# ~~~~~ Check OML_GLOBALS_VARIABLES_FILENAME

assert OML_GLOBALS_VARIABLES_FILENAME is not None, \
    "Falta definir setting para OML_GLOBALS_VARIABLES_FILENAME"

# ~~~~~ Check TMPL_OML_AUDIO_CONVERSOR

assert TMPL_OML_AUDIO_CONVERSOR is not None, \
    "Falta definir setting para TMPL_OML_AUDIO_CONVERSOR"

assert "<INPUT_FILE>" in TMPL_OML_AUDIO_CONVERSOR, \
    "Falta definir <INPUT_FILE> en TMPL_OML_AUDIO_CONVERSOR"

assert "<OUTPUT_FILE>" in TMPL_OML_AUDIO_CONVERSOR, \
    "Falta definir <OUTPUT_FILE> en TMPL_OML_AUDIO_CONVERSOR"

# 3 elementos como minimo: (1) comando (2/3) INPUT/OUTPUT
assert len(TMPL_OML_AUDIO_CONVERSOR) >= 3, \
    "TMPL_OML_AUDIO_CONVERSOR debe tener al menos 3 elementos"

ret = subprocess.call('which {0} > /dev/null 2> /dev/null'.format(
    TMPL_OML_AUDIO_CONVERSOR[0]), shell=True)

assert ret == 0, "No se ha encontrado el ejecutable configurado " +\
    "en TMPL_OML_AUDIO_CONVERSOR: '{0}'".format(TMPL_OML_AUDIO_CONVERSOR[0])

# ~~~~~ Check TMPL_OML_AUDIO_CONVERSOR

assert TMPL_OML_AUDIO_CONVERSOR_EXTENSION is not None, \
    "Falta definir setting para TMPL_OML_AUDIO_CONVERSOR"

# ~~~~~ Check ASTERISK_AUDIO_PATH

assert ASTERISK_AUDIO_PATH is not None, \
    "Falta definir setting para ASTERISK_AUDIO_PATH"

# ~~~~~ Check OML_AUDIO_FOLDER

assert OML_AUDIO_FOLDER is not None, \
    "Falta definir setting para OML_AUDIO_FOLDER"

# Una vez que tengo ASTERISK_AUDIO_PATH y OML_AUDIO_FOLDER puedo calcular OML_AUDIO_PATH_ASTERISK
OML_AUDIO_PATH_ASTERISK = ASTERISK_AUDIO_PATH + OML_AUDIO_FOLDER

# ~~~~~ Check CALIFICACION_REAGENDA

assert CALIFICACION_REAGENDA is not None, \
    "Falta definir setting para CALIFICACION_REAGENDA"
