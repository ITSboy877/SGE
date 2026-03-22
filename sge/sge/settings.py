from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-9he=*6k$fk6f9rrc)a7akv#1!()25wk)txx-+ze$&%n(to9zu5"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sge.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "core" / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ],
    },
}]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

JAZZMIN_SETTINGS = {
    "site_title": "SGE",
    "site_header": "SGE",
    "site_brand": "SGE",
    "site_logo": None,
    "site_icon": None,
    "welcome_sign": "Sistema de Gestão Escolar",
    "show_sidebar": True,
    "navigation_expanded": True,
    "theme": "cosmo",
    "order_with_respect_to": [
        "core.Turma",
        "core.Aluno",
        "core.Circulacao",
        "core.Ocorrencia",
        "core.Frequencia",
        "core.Notificacao",
        "core.Perfil",
    ],
}

JAZZMIN_UI_TWEAKS = {
    "sidebar": "sidebar-dark-primary",
    "navbar": "navbar-white navbar-light",
    "sidebar_nav_compact_style": True,
}