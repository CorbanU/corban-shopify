from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin


urlpatterns = [
    url(r'', include('shopify.webhook.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

admin.site.site_header = admin.site.site_title = 'Corban Shopify'
