from django.conf.urls import patterns, include, url
from django.contrib import admin
from weixininterface.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wechat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^weixin/', weixininterface.as_view(), name='interface'),
    url(r'^admin/', include(admin.site.urls,)),
    url(r'^ranking/', ranking_handler.as_view(), name='ranking'),
)
