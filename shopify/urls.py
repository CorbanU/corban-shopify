from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'', include('webhooks.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
