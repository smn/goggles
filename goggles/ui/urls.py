from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url('', include('goggles.warehouse.urls', namespace='warehouse')),
    url('', include('social.apps.django_app.urls', namespace='social'))
)
