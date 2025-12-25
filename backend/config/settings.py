import os
from pathlib import Path
from decouple import config
from datetime import timedelta
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# [보안] 시크릿 키는 환경변수에서 가져오되, 없으면 기본값 사용 (에러 방지)
SECRET_KEY = config("SECRET_KEY", default="django-insecure-fallback-key-123")

# [중요] 배포 환경에서는 False, 개발 환경에서는 True
DEBUG = config("DEBUG", default=True, cast=bool)

# --- [이 부분을 제가 드리는 코드로 완전히 교체하세요] ---
if not DEBUG:
    # Render 배포 주소를 강제로 박아 넣습니다. 
    # 오타 방지를 위해 .onrender.com을 포함한 모든 주소를 허용합니다.
    ALLOWED_HOSTS = [
        'ohjigo-library.onrender.com',
        'ohjigo-library-library.onrender.com',
        'localhost',
        '127.0.0.1',
        '.onrender.com',  # 모든 Render 서브도메인 허용
    ]
else:
    # 개발 모드일 때는 모든 호스트 허용 (가장 편함)
    ALLOWED_HOSTS = ['*']
# ---------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "corsheaders",
    "common",
    "members",
    "library",
    "manager",
    'import_export',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", # 정적 파일용
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# [중요] CORS 설정 - 프론트엔드에서 접속 가능하게 함
CORS_ALLOW_ALL_ORIGINS = True # 일단 모든 접속 허용 (배포 성공 확인용)

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, '..', 'frontend', 'dist')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database 설정
db_url = config("DATABASE_URL", default=None)

if db_url:
    DATABASES = {
        "default": dj_database_url.config(
            default=db_url,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication', 
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    'TOKEN_OBTAIN_SERIALIZER': 'members.serializers.CustomTokenObtainPairSerializer',
    
    # 모델에서 USERNAME_FIELD로 지정한 필드명을 적습니다.
    'USER_ID_FIELD': 'sid', 
    'USER_ID_CLAIM': 'user_id',

    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

AUTH_USER_MODEL = 'members.Member'

LANGUAGE_CODE = "ko-kr" # 한국어 설정
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"