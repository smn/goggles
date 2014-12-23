from django.conf.urls import patterns, url

from goggles.warehouse import views


urlpatterns = patterns(
    '',
    url('^login/$', views.login, name='login'),
    url('^logout/$', views.logout, name='logout'),

    url('^$', views.dashboard, name='dashboard'),

    url('^job/new/$', views.job_new, name='job_new'),
    url('^job/(?P<pk>\d+)/$', views.job, name='job'),
    url('^job/(?P<pk>\d+)/edit/$', views.job_edit, name='job_edit'),

    url('^profile/new/$', views.profile_new, name='profile_new'),
    url('^profile/(?P<pk>\d+)/$', views.profile, name='profile'),

    url('^conversation/(?P<pk>\d+)/$', views.conversation, name='conversation')
)
