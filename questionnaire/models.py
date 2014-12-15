from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from questionnaire import fields


STATUS_DRAFT = 1
STATUS_PUBLISHED = 2
STATUS_ARCHIVED = 3
STATUS_CHOICES = (
    (STATUS_DRAFT, 'Draft'),
    (STATUS_PUBLISHED, 'Published'),
    (STATUS_ARCHIVED, 'Archived'),
)


class StudyManager(models.Manager):
    pass


class Study(models.Model):
    pass


class FormManager(models.Manager):
    def published(self, user=None):
        if user is not None:
            return self.filters(status=STATUS_PUBLISHED)


class Form(models.Model):
    title = models.CharField(_('Title'), max_length=100)
    slug = models.SlugField(max_length=200, editable=False, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    version = models.CharField(max_length=20, null=True, blank=True)
    version_date = models.DateField(null=True, blank=True)
    revision_notes = models.CharField(max_length=200, null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES)

    objects = FormManager()

    class Meta:
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('add_questionnaire', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self)
            super(Form, self).save(*args, **kwargs)


class Field(models.Model):
    form = models.ForeignKey(Form, related_name='fields')
    name = models.CharField(max_length=20)
    number = models.CharField(max_length=10, null=True, blank=True)
    label = models.CharField(max_length=200)
    column = models.IntegerField(_('Column'))
    order = models.IntegerField(null=True, blank=True, editable=False)
    response_type = models.IntegerField(_('Response'), choices=fields.NAMES)
    response_choices = models.CharField(_('Choices'), max_length=200, null=True, blank=True,
                                        help_text='Comma separated list of options')
    help_text = models.CharField(max_length=200, null=True, blank=True)
    section = models.CharField(max_length=100, null=True, blank=True)
    required = models.BooleanField(default=True)

    class Meta:
        ordering = ('order',)
        verbose_name = 'Field'
        verbose_name_plural = 'Fields'

    def __unicode__(self):
        return self.label

    def get_choices(self):
        for choice in self.response_choices.split(','):
            yield choice, choice

    def save(self, *args, **kwargs):
        if self.response_type in fields.CHOICES + fields.MULTIPLE and self.response_choices is None:
            raise ValidationError("Please provide comma separated list of options")
        if self.order is None:
            self.order = self.form.fields.count()
        super(Field, self).save(*args, **kwargs)

    def insert(self, pk=None):
        if pk:
            field = self.form.fields.get(pk=pk)
            self.order = field.order
            fields_after = self.form.fields.filter(order__gte=field.order-1)
            fields_after.update(order=models.F("order") + 1)


    def delete(self, *args, **kwargs):
        fields_after = self.form.fields.filter(order__gte=self.order)
        fields_after.update(order=models.F("order") - 1)
        super(Field, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('edit_field', kwargs={'slug': self.form.slug, 'pk': self.pk})


class FieldConstraint(models.Model):
    pass


class FormEntry(models.Model):
    form = models.ForeignKey(Form, related_name='entries')
    entry_time = models.DateTimeField()
    user = models.ForeignKey(User, editable=False)

    class Meta:
        verbose_name = 'Form entry'
        verbose_name_plural = 'Form entries'

    def __unicode__(self):
        return self.form.title

    def get_absolute_url(self):
        return reverse('edit_questionnaire',
                       kwargs={'slug': self.form.slug, 'pk': self.pk}
        )


class FieldEntry(models.Model):
    entry = models.ForeignKey(FormEntry, related_name='fields')
    field_id = models.IntegerField()
    response = models.CharField(max_length=fields.FIELD_MAX_LENGTH, null=True, blank=True)

    class Meta:
        verbose_name = 'Field entry'
        verbose_name_plural = 'Field entries'


class Report(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, editable=False, unique=True)
