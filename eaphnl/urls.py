from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'playground.views.login', name='login'),
    url(r'^logout/$', 'playground.views.logout', name='logout'),
    url(r'^', include('questionnaire.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
