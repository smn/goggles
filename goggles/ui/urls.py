from django.conf.urls import patterns, include, url
from django.contrib import admin

from goggles.ui import views


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url('^$', views.social_login),
    url('', include('social.apps.django_app.urls', namespace='social'))
)
