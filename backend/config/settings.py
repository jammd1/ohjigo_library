import os
from pathlib import Path
from decouple import config
from django.core.exceptions import ImproperlyConfigured
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

if not DEBUG:
    # [수정] Render 주소를 환경 변수에 넣거나 직접 추가하세요.
    # 쉼표로 구분: "ohjigo-library.onrender.com, localhost"
    host_string = config('ALLOWED_HOSTS', default='localhost') 
    ALLOWED_HOSTS = [h.strip() for h in host_string.split(',') if h.strip()]
    
    # Render 도메인을 명시적으로 추가 (안전빵)
    ALLOWED_HOSTS.append('.onrender.com') 
else:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Application definition
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
    "corsheaders", # 잘 들어있습니다.
    "common",
    "members",
    "library",
    "manager",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", # [추장] 정적 파일 배포를 위해 추가 추천
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware", # CommonMiddleware보다 위에 있어야 함 (잘 되어있음)
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# [수정] 배포된 프론트엔드(Vercel) 주소를 추가하세요.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://your-frontend-name.vercel.app", # 내 Vercel 주소 입력!
]

# [추가] 배포 환경에서는 모든 오리진 허용을 한시적으로 켜서 테스트 가능
# CORS_ALLOW_ALL_ORIGINS = True 

ROOT_URLCONF = "config.urls"

# ... (TEMPLATES, WSGI_APPLICATION 등은 동일)

# [수정] 정적 파일 설정 (Render 배포 시 필수)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # 배포 시 파일이 모이는 곳