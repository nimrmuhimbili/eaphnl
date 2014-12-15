from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'eaphnl.views.login', name='login'),
    url(r'^logout/$', 'eaphnl.views.logout', name='logout'),
    url(r'^', include('questionnaire.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
