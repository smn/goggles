from django.conf.urls import patterns, url

from goggles.warehouse import views


urlpatterns = patterns(
    '',
    url('^login/$', views.login, name='login'),
    url('^logout/$', views.logout, name='logout'),
    url('^job/(?P<pk>\d+)/$', views.job, name='job'),
    url('^job/(?P<pk>\d+)/edit/$', views.job_edit, name='edit_job'),
    url('^$', views.dashboard, name='dashboard'),
)
