from pathlib import Path

import environ
import rest_framework.permissions
from celery.schedules import crontab

# 初始化 environ
env = environ.Env(
    # 设置默认值
    DEBUG=(bool, True),
    ESI_SSO_CALLBACK_URL=(str, "http://localhost:8000/sso/callback"),
    ESI_USER_CONTACT_EMAIL=(str, "2434789129@qq.com"),
)

# 设置项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 设置环境变量文件路径
ENV_PATH = env.str('ENV_PATH', BASE_DIR / '.env')
environ.Env.read_env(ENV_PATH)

# 从环境变量中读取配置
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
SOCIAL_AUTH_EVEONLINE_KEY = env('SOCIAL_AUTH_EVEONLINE_KEY')
SOCIAL_AUTH_EVEONLINE_SECRET = env('SOCIAL_AUTH_EVEONLINE_SECRET')
ESI_SSO_CLIENT_ID = env('ESI_SSO_CLIENT_ID')
ESI_SSO_CLIENT_SECRET = env('ESI_SSO_CLIENT_SECRET')
ESI_SSO_CALLBACK_URL = env('ESI_SSO_CALLBACK_URL')
ESI_USER_CONTACT_EMAIL = env('ESI_USER_CONTACT_EMAIL')

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'esi',
    'rest_framework',
    'drf_spectacular',
    'titan_main',
]

SPECTACULAR_SETTINGS = {
    'TITLE': 'TITAN LEGION API',
    'DESCRIPTION': 'TITAN LEGION 的API文档',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

AUTHENTICATION_BACKENDS = [
    'social_core.backends.eveonline.EVEOnlineOAuth2',  # 修改OAuth2 中 REDIRECT_STATE 为 False
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = '/login/'  # 登录页面URL
LOGIN_REDIRECT_URL = '/'  # 登录成功后的重定向URL
LOGOUT_REDIRECT_URL = '/'  # 登出后的重定向URL

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'  # 登录成功后的重定向URL

CELERYBEAT_SCHEDULE = {
    'esi_cleanup_callbackredirect': {
        'task': 'esi.tasks.cleanup_callbackredirect',
        'schedule': crontab(hour='*/4'),
    },
    'esi_cleanup_token': {
        'task': 'esi.tasks.cleanup_token',
        'schedule': crontab(day_of_month='*/1'),
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'titan_legion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'static/templates'],
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

WSGI_APPLICATION = 'titan_legion.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
