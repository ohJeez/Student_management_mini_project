"""
Django settings for EduPortal.
Reads sensitive values from environment variables (Railway injects them automatically).
"""
import os
from pathlib import Path
import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ──────────────────────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY', default='replace-this-with-a-secure-key')
DEBUG      = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

# ── Applications ──────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'student',
    'accounts.apps.AccountsConfig',
    'blog',
]

# ── Middleware ────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',          # ← WhiteNoise (static files)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'

# ── Database ──────────────────────────────────────────────────────────────────
# Railway automatically sets DATABASE_URL.
# Falls back to local SQLite for development (if DATABASE_URL is not set).
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,        # persistent connections (performance)
        conn_health_checks=True,
    )
}

# ── Password hashing ──────────────────────────────────────────────────────────
# Argon2 is the primary hasher (strongest). Existing PBKDF2 hashes are
# automatically upgraded to Argon2 on the user's next login.
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# ── Password validators ───────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {'max_similarity': 0.6},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ── Internationalisation ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Asia/Kolkata'   # IST – adjust to your timezone
USE_I18N      = True
USE_TZ        = True

# ── Static files ──────────────────────────────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'   # collectstatic output dir (Railway)

# WhiteNoise: serve compressed static files with long cache headers
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── Media files (user uploads) ────────────────────────────────────────────────
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ── Primary key field ─────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Authentication redirects ──────────────────────────────────────────────────
LOGIN_URL            = '/accounts/login/'
LOGIN_REDIRECT_URL   = '/students/'
LOGOUT_REDIRECT_URL  = '/accounts/login/'

# ── Messages ──────────────────────────────────────────────────────────────────
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# ── Session security ──────────────────────────────────────────────────────────
SESSION_COOKIE_AGE           = 60 * 60 * 8   # 8 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
