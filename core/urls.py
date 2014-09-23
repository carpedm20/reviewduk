from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reviewduk.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^carpedm20/', include('reviewduk.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^r/get/(?P<count>\d+)$', views.get_review, name='get_review'),
    url(r'^r/cached/(?P<count>\d+)$', views.get_cached_prediction, name='get_cached_prediction'),
    url(r'^r/predict$', views.get_prediction, name='get_prediction'),
)
