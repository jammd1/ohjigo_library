import os
from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

# --- [여기서부터 수정] ---
if not DEBUG:
    # 환경 변수('ALLOWED_HOSTS')가 없더라도 아래 주소들은 무조건 허용합니다.
    ALLOWED_HOSTS = [
        'ohjigo-library.onrender.com',
        'ohjigo-library-library.onrender.com', # Render 서비스 이름 기준 주소
        'localhost',
        '127.0.0.1',
    ]
    
    # 추가로 .onrender.com으로 끝나는 모든 서브도메인을 허용 (안전 장치)
    ALLOWED_HOSTS.append('.onrender.com')
else:
    # 개발 환경(로컬) 설정
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
# --- [여기까지 수정] ---

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
    "corsheaders", 
    "common",
    "members",
    "library",
    "manager",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware", 
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# [중요] 내 Vercel 프론트엔드 주소를 여기에 넣으세요!
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://your-frontend-name.vercel.app", # <-- 실제 Vercel 주소로 변경
]

# (이후 ROOT_URLCONF, TEMPLATES 등 기존 코드는 그대로 유지하세요)

ROOT_URLCONF = "config.urls"

# ... (TEMPLATES, WSGI_APPLICATION 등은 동일)

# [수정] 정적 파일 설정 (Render 배포 시 필수)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # 배포 시 파일이 모이는 곳