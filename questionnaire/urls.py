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
    url(r"(?P<slug>.*)/entries/imports/$", "manage_imports", name="import_entries"),
    url(r"(?P<slug>.*)/fields/new-field/$", 'manage_form_field', name='add_field'),
    url(r"(?P<slug>.*)/fields/(?P<pk>\d+)/$", 'manage_form_field', name='edit_field'),
    url(r"(?P<slug>.*)/fields/(?P<pk>\d+)/delete/$", 'manage_form_field_delete', name='delete_field'),
    url(r"entries/search/$", "search_entry", name="search_entry"),
    url(r"reports/$", 'manage_reports', name='reports'),
    url(r"accounts/users/new-user/$", 'manage_user', name='create_user'),
    url(r"accounts/users/(?P<pk>\d+)/edit/$", 'manage_user', name='edit_user'),
    url(r"accounts/users/(?P<pk>\d+)/delete/$", 'manage_user_delete', name='delete_user'),
    url(r"accounts/users/$", 'manage_users', name='manage_users'),
)