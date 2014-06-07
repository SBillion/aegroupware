import os.path
import locale

# Django settings for AEGroupware project.

DJANGO_ROOT = os.path.dirname(__file__).replace('\\','/')

DEBUG = True
TEMPLATE_DEBUG = DEBUG
EMAIL_DEBUG = True

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

ADMINS = (
  ('Admin', 'Admin@lol.com'),
)
MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'sqlite3',	# Use sqlite3 as backend
		'NAME': 'test.sqlite',	# Path to database file with sqlite3.
		'USER': '',		# Not used with sqlite3.
		'PASSWORD': '',		# Not used with sqlite3.
		'HOST': '',		# Not used with sqlite3.
		'PORT': '',		# Not used with sqlite3.
	}
}

# Login settings
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-FR'

#Set the locale
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(DJANGO_ROOT, 'static/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^bt0ul2!#5d3bkx5n-lww3^)7g!ybf(t#q)nj=q2n-5&sk068j'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
#	'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.auth',
	'django.core.context_processors.i18n',
	'django.core.context_processors.request',
	'django.core.context_processors.media',
	'zinnia.context_processors.media',
	'django_authopenid.context_processors.authopenid',
	'djangobb_forum.context_processors.forum_settings',
	'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
)

# To display error/warning messages like an invalid username/password in the login page
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

ROOT_URLCONF = 'src.urls'

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(DJANGO_ROOT, 'templates'),
)

# Haystack settings
HAYSTACK_SITECONF = 'search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_ROOT, 'djangobb_index')

# Account settings
ACCOUNT_ACTIVATION_DAYS = 10

#Cache settings
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

EMAIL_BACKEND = "mailer.backend.DbBackend"

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'supinfogroupproject@gmail.com'
EMAIL_HOST_PASSWORD = 'azerty123@'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


INSTALLED_APPS = (
	# Django depends
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.comments',
	# Uncomment the next line to enable the admin:
	'django.contrib.admin',
	# Uncomment the next line to enable admin documentation:
	#'django.contrib.admindocs',
	# AEGroupware apps
	'account',
	'portal',
	'planner',
	'product',
	'agency',
	# Zinnia blog
	'zinnia',
	'tagging',
	'mptt',
	'markdown',
	'registration',
	'djangobb_forum',
	'django_authopenid',
	'openid',
	'messages',
	'whoosh',
	'mailer',
	'notification',
)

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'account.backend.AuthBackend',)

