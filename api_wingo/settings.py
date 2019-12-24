import os
import datetime

#os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!==m_q+&@2sj8h(%%s*ny5&c)56a&3)iht(!u94k*0ks#0_k!n'
#SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '!==m_q+&@2sj8h(%%s*ny5&c)56a&3)iht(!u94k*0ks#0_k!n')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = bool( os.environ.get('DJANGO_DEBUG', False) )

ALLOWED_HOSTS = [
'163.172.182.218',
'localhost',
'127.0.0.1',
'51.15.91.183',
'68.168.213.77',
'hit.veritasoft.site',
'veritasoft.site',
'192.168.1.116',
'192.168.1.133'
]
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Third party apps
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'rest_auth',
    'rest_auth.registration',
    'corsheaders',
    'allauth',
    'allauth.account',
    'computed_property',
    # Internal Apps
    'apiwingo',
    # SSL SERVER
    'sslserver',

]

AUTH_USER_MODEL = 'apiwingo.User'
CELERY_BROKER_URL = 'amqp://localhost'

###################### EMAIL SETTINGS ##########################
#'kfhkquagnckcjvpj'
#587
#EMAIL_USE_SSL = True
EMAIL_USE_TLS = True
#EMAIL_TIMEOUT = 60
#EMAIL_SSL_KEYFILE =
#EMAIL_SSL_CERTFILE=
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'mail.veritasoft.site'
EMAIL_HOST_PASSWORD = 'Verit@2018'
EMAIL_HOST_USER = 'info@veritasoft.site'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
APP_HOST = 'http://localhost:4200'
#APP_HOST = 'http://163.172.182.218:8085'
################################################################



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ORIGIN_WHITELIST = (
    'google.com',
    'hostname.example.com',
    'veritasoft.site',
    '*.veritasoft.site',
    'localhost:8000',
    '127.0.0.1:9000',
    'localhost:4200',
    '127.0.0.1:4200',
    'localhost:3030',
    '127.0.0.1:8080',
    '127.0.0.1:8000',
    '127.0.0.1:8081',
    '51.15.91.183',
    '68.168.213.77',
    'hit.veritasoft.site:8000',
    'veritasoft.site:8000',
    '192.168.1.116:8080',
    '192.168.1.133:8080',
)
CORS_ORIGIN_REGEX_WHITELIST = (r'^(https?://)?(\w+\.)?google\.com$',
                               r'^(https?://)?(\w+\.)?veritasoft\.site$',
                               )
CORS_URLS_REGEX = r'^/api/.*$'
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'responseType',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)


ROOT_URLCONF = 'api_wingo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'api_wingo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {  # a default database must exist. this one will contain the django related data
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangodb',
        'USER': 'root',
        'PASSWORD': 'Gjc*27911972',
        'HOST': 'localhost', # Or an IP Address that your DB is hosted on
        #'PASSWORD': 'wingo*2018',
        #'HOST': '192.168.1.105', # Or an IP Address that your DB is hosted on
        #'PASSWORD': 'Gjc*27911972',
        #'HOST': '51.15.93.81', # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    },
    'wingo_data': {   # this is the legacy database
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wingodb',
        'USER': 'root',
        'PASSWORD': 'Gjc*27911972',
        'HOST': 'localhost', # Or an IP Address that your DB is hosted on
        #'PASSWORD': 'wingo*2018',
        #'HOST': '192.168.1.105', # Or an IP Address that your DB is hosted on
        #'PASSWORD': 'Gjc*27911972',
        #'HOST': '51.15.93.81', # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    },
}


DATABASE_ROUTERS = ['apiwingo.dbrouters.WingoDbRouter']

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

JWT_AUTH = {

    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': '!==m_q+&@2sj8h(%%s*ny5&c)56a&3)iht(!u94k*0ks#0_k!n',
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=1),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': None,

}



MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    # Now we add here our custom middleware
    'apiwingo.middleware.corsMiddleware'
)

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
       #'rest_framework.permissions.AllowAny',
       ##'rest_framework.permissions.IsAdminUser', #estaba comentado
       #'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
        #'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.TokenAuthentication',
        ##'apiwingo.auth.CustomAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES':  (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.AdminRenderer',
    ),
    'DEFAULT_CONTENT_NEGOTIATION_CLASSES': [
        'rest_framework.negotiation.DefaultContentNegotiation',
    ]

}

# Enables django-rest-auth to use JWT tokens instead of regular tokens.
REST_USE_JWT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
SITE_ID = 1


