from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reviewduk.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('core.urls', namespace='core')),
    url(r'^admin/', include(admin.site.urls)),
)
