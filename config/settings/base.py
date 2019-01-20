# -*- coding:utf-8 -*-
import environ
import sys
import os

ROOT_DIR = environ.Path(__file__) - 3  # (liBlog/liBlog/settings/base.py - 3 = liBlog/)
APPS_DIR = ROOT_DIR.path('liBlog')
# sys.path.insert(0, APPS_DIR)

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(ROOT_DIR.path('.env'))
    print('Loading : {}'.format(env_file))
    env.read_env(env_file)
    print('The .env file has been loaded. See base.py for more information')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='=-mjt^rhlo5v(e^6xu_s@6c0h!bxc*h0vm(8=^4!ufe+upb-&#')


# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.gis',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
]
THIRD_PARTY_APPS = [
    'crispy_forms',  # Form layouts
    'mdeditor',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.weibo',
    'allauth.socialaccount.providers.github',

    'django_markdown2',
    'liBlog.comments.apps.CommentsConfig',
    'django_comments_xtd',
    'django_comments',

    'haystack',

]

# Apps specific for this project go here.
LOCAL_APPS = [
    # custom users app
    'liBlog.users.apps.UsersConfig',
    # Your stuff: custom apps go here
    'liBlog.blogs.apps.BlogsConfig',
    'liBlog.visitor.apps.VisitorConfig',
    'liBlog.tutorial.apps.TutorialConfig',
]
# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # 国际化
    'liBlog.visitor.middleware.VisitorTrackingMiddleware',
]

# ------------------------------------------------------------------------------
# URL Configuration
ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'


# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',

                # Your stuff: custom template context processors go here
            ],
        },
    },
]


# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db('DATABASE_URL', default='mysql://root:Root1024@localhost:3306/blog'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------
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

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'  # 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'zh-cn'  # 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

LANGUAGES = (
    ('en', ('English')),
    ('zh-hans', ('中文简体')),
    ('zh-hant', ('中文繁體')),
)
#翻译文件所在目录，需要手工创建
LOCALE_PATHS = (
    os.path.join(str(APPS_DIR.path('static')), 'locale'),
)

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'


# MDEditor settings
# ------------------------------------------------------------------------------
MDEDITOR_CONFIGS = {
    'default': {
        'width': '90%',
        'heigth': 500,
        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                    "h1", "h2", "h3", "h5", "h6", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime",
                    "emoji", "html-entities", "pagebreak", "goto-line", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"],
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
        'image_floder': 'editor',
        'theme': 'default',  # dark / default
        'preview_theme': 'default',  # dark / default
        'editor_theme': 'default',  # pastel-on-dark / default
        'toolbar_autofixed': True,
        'search_replace': True,
        'emoji': True,
        'tex': True,
        'flow_chart': True,
        'sequence': True
        }
}


# LOG CONFIGURATION
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s - [%(asctime)s] [%(module)s %(filename)s %(funcName)s %(lineno)d %(pathname)s]'\
                      ' - %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'liBlog.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'propagate': True,
        #     'level': 'DEBUG',
        # },

    }
}



# django admin configration
# ------------------------------------------------------------------------------
ADMIN_URL = r'^admin/'

# django-compressor
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['compressor']
STATICFILES_FINDERS += ['compressor.finders.CompressorFinder']
COMPRESS_CSS_HASHING_METHOD = 'hash'

# blog configration
# ------------------------------------------------------------------------------
SITE = {
    'title': "Pylixm'Wiki",
    'sub_title': """自感不善于写作，但总感觉要记录下自己这段时光。已近而立之年，
    自己却仍然混沌。那便用这“烂笔头”理顺这混沌年华吧！-- 2015-11-28 北京""",
    'publish_time': '2018-05-14 20:00:00',
    'last_publish_time': '2018-08-02 00:00:00',
    'keyswords': 'python django devops 运维 运维开发 salt saltstack docker 自动化',
    'description': 'python django devops 运维 运维开发 salt saltstack docker 自动化',
    'author': 'Pylixm',
    'author_avatar': '/static/imgs/avatar.jpg',
    'contact': [{
        'name': '微博',
        'url': 'https://weibo.com/u/2258086637',
        'icon': 'fa fa-weibo'
    }, {
        'name': 'Github',
        'url': 'https://github.com/pylixm',
        'icon': 'fa fa-github'
    }, {
        'name': 'segmentfault',
        'url': 'https://segmentfault.com/u/pylixm'
    }, {
        'name': 'Google',
        'url': 'https://plus.google.com/u/0/111595735719900628845',
        'icon': 'fa fa-google-plus-circle'
    }],
    'links': [{
        'name': '',
        'url': ''
    }]

}
# post的md文档路径
POST_SOURCE_PATH = os.path.join(str(ROOT_DIR), 'source')
PAGENUM = 15
# 标签云大小设置
TAG_LEVEL_1 = 2
TAG_LEVEL_2 = 3
TAG_LEVEL_3 = 5
TAG_SIDE_SHOW_NUM = 3

# 评论APP
COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_MAX_THREAD_LEVEL = 2  # 设置评论深度
COMMENTS_XTD_CONFIRM_EMAIL = False  # 是否开启邮件
COMMENT_MAX_LENGTH = 500

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.qq.com"
EMAIL_PORT = env.str('EMAIL_PORT', default='25')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default="20894205@qq.com")
# 注意测试为邮箱服务器生成的key, 不是邮箱密码
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default="")
EMAIL_SUBJECT_PREFIX = u'django'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_VERIFICATION = True


# COMMENTS_XTD_MODEL = 'django_comments_xtd.models.XtdComment'
COMMENTS_XTD_FORM_CLASS = 'liBlog.comments.forms.LiCommentForm'


# allauth configration
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
      'django.contrib.auth.backends.ModelBackend',
      'allauth.account.auth_backends.AuthenticationBackend',
)
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
# LOGIN_REDIRECT_URL = 'users:redirect'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'account_login'

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
            # 'repo',
            # 'read:org',
        ],
    }
}


# 全文搜索
# ------------------------------
HAYSTACK_CONNECTIONS = {
    'default': {
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'ENGINE': 'liBlog.blogs.backend.whoosh_backend_cn.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}
#设置每页显示的数目，默认为20，可以自己修改
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 15
#自动更新索引
#HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'