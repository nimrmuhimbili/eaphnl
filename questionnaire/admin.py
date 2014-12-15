from django.contrib import admin

from questionnaire.models import Form, Field


class FieldInline(admin.TabularInline):
    model = Field


class FormAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Form Information', {'fields':
                                  ('title', 'description',
                                   ('version', 'version_date', 'revision_notes'),
                                  'status')}),
    )
    inlines = (FieldInline,)
    list_display = ('title', 'version', 'version_date', 'status')



admin.site.register(Form, FormAdmin)