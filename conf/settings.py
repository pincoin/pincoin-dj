import json
from pathlib import Path

from . import BASE_DIR

# Build paths inside the project like this: BASE_DIR / 'subdir'.
secret_file = BASE_DIR / 'conf' / 'secret.json'

with open(secret_file) as f:
    secrets = json.loads(f.read())

SECRET_KEY = secrets['secretKey']
DEBUG = secrets['debug']
ALLOWED_HOSTS = secrets['allowedHosts']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]
INSTALLED_APPS += [
    'mptt',
    'treebeard',
    'taggit',
    'easy_thumbnails',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.naver',
]

INSTALLED_APPS += [
    'common',
    'member',
    'shop',
    'organization',
    'blog',
    'book',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # i18n
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_otp.middleware.OTPMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'conf.wsgi.application'

DATABASES = {
    'default': secrets['database']['default'],
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Django 기본값
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth
)

CACHES = {
    'default': secrets['caches']['default']
}

if not DEBUG:
    # HTTPS 설정
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    CSRF_COOKIE_SAMESITE = 'Strict'

    # HSTS 설정
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    # 세션 설정
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_SAVE_EVERY_REQUEST = True
    SESSION_COOKIE_AGE = 90 * 60
    SESSION_COOKIE_SAMESITE = 'Strict'

LANGUAGE_CODE = 'ko-kr'
LOCALE_PATHS = (BASE_DIR / 'locale',)
USE_I18N = True
USE_L10N = True

# 모든 Amazon RDS DB 인스턴스는 UTC/GMT 시간이 기본값
# DB 인스턴스의 DB 파라미터 그룹에서 time_zone 파라미터를 "Asia/Seoul"으로 설정
TIME_ZONE = 'Asia/Seoul'
USE_TZ = True
USE_THOUSAND_SEPARATOR = True

STATIC_URL = '/assets/'
STATIC_ROOT = BASE_DIR / 'assets/'
STATICFILES_DIRS = []

# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'assets/')
# STATICFILES_DIRS = []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARN',
        },
    }
}

# Django allauth
SITE_ID = 1
