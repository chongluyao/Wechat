# -*- coding: UTF-8 -*-
"""
Django settings for wechat project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os import environ
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qv*bq(wgj$o*s@b=o3bt9x@$=0l5idxjxkz%u6yq9bc29q$lu4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'weixininterface',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'wechat.urls'

WSGI_APPLICATION = 'wechat.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases\

if 'SERVER_SOFTWARE' in os.environ:
    from sae.const import (
        MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
    )
else:
    MYSQL_DB = 'weixin'
    MYSQL_USER = 'root'
    MYSQL_PASS = ''
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = '3308'

DATABASES = {
    'default':{
        'ENGINE':   'django.db.backends.mysql',
        'NAME':      MYSQL_DB,
        'USER':      MYSQL_USER,
        'PASSWORD':  MYSQL_PASS,
        'HOST':      MYSQL_HOST,
        'PORT':      MYSQL_PORT,
    }
}


#debug = not environ.get("thsswelearn/4","")
#debug = ('SERVER_SOFTWARE' in os.environ)
#debug = False
#debug = True
# if debug:
#     #LOCAL 当代码运行在本地的时候，链接本地数据库，自行配置
#     DOMAIN = 'http://localhost:8000'
#     CACHES_BACKEND = 'django.core.cache.memcached.MemcachedCache'
#     MYSQL_DB = 'weixin'
#     MYSQL_USER = 'root'
#     MYSQL_PASS = '19950311cly'
#     MYSQL_HOST_M = 'localhost'
#     MYSQL_HOST_S = '127.0.0.1'
#     MYSQL_PORT = '3306'
# else:
# #SAE 当代码运行在云平台的时候，链接云数据库，链接用的参数都在sae.const里面
#     import sae.const
#     MYSQL_DB = sae.const.MYSQL_DB
#     MYSQL_USER = sae.const.MYSQL_USER
#     MYSQL_PASS = sae.const.MYSQL_PASS
#     MYSQL_HOST_M = sae.const.MYSQL_HOST
#     MYSQL_HOST_S = sae.const.MYSQL_HOST_S
#     MYSQL_PORT = sae.const.MYSQL_PORT
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': MYSQL_DB,
#         'USER': MYSQL_USER,
#         'PASSWORD': MYSQL_PASS,
#         'HOST': MYSQL_HOST_M,
#         'PORT': MYSQL_PORT,
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'weixininterface/static').replace('\\', '/'),)
#weixininterface settings

WEIXIN_TOKEN = 'wechat_token'

#cly
#WEIXIN_APPID = 'wxebd2821dd8acc2d3'
#WEIXIN_SECRET = 'e5747e6c7f31a2c2eb10b69d475e195f'

WEIXIN_APPID = 'wx0f9f5491705f15ca'

WEIXIN_SECRET = '1324da84f8aa35bbb33a1f7ad23c3e3a'