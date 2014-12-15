from django.conf.urls import patterns, include, url


urlpatterns = patterns("questionnaire.views",
    url(r"^$", "manage_forms", name="forms"),
    url(r"^form/$", "manage_form", name="add_form"),
    url(r"^form/(?P<pk>\d+)/$", "manage_form", name="update_form"),
    url(r"^form/(?P<pk>\d+)/delete/$", "manage_form_delete", name="delete_form"),
    url(r"(?P<slug>.*)/entries/$", "manage_entries", name="entries"),
    url(r"(?P<slug>.*)/entries/new-entry/$", "manage_entry", name="add_questionnaire"),
    url(r"(?P<slug>.*)/entries/(?P<pk>\d+)/$", "manage_entry", name="edit_questionnaire"),
    url(r"(?P<slug>.*)/entries/exports/$", "manage_exports", name="export_entries"),
    url(r"(?P<slug>.*)/fields/new-field/$", 'manage_form_field', name='add_field'),
    url(r"(?P<slug>.*)/fields/(?P<pk>\d+)/$", 'manage_form_field', name='edit_field'),
    url(r"(?P<slug>.*)/fields/(?P<pk>\d+)/delete/$", 'manage_form_field_delete', name='delete_field'),
    url(r"reports/$", 'manage_reports', name='reports'),
    url(r"accounts/new-user/$", 'create_user', name='create_user'),
    url(r"accounts/users/$", 'manage_users', name='manage_users'),
)