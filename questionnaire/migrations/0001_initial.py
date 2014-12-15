# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('number', models.CharField(max_length=10, null=True, blank=True)),
                ('label', models.CharField(max_length=200)),
                ('column', models.IntegerField(verbose_name='Column')),
                ('order', models.IntegerField(null=True, editable=False, blank=True)),
                ('response_type', models.IntegerField(verbose_name='Response', choices=[(1, b'Integer'), (2, b'Decimal'), (3, b'Single line text'), (4, b'Multiple line text'), (5, b'Radio'), (6, b'Checkbox'), (7, b'Multiple checkbox'), (8, b'Single select'), (9, b'Multiple select'), (10, b'Date'), (11, b'Time'), (12, b'Date/time')])),
                ('response_choices', models.CharField(help_text=b'Comma separated list of options', max_length=200, null=True, verbose_name='Choices', blank=True)),
                ('help_text', models.CharField(max_length=200, null=True, blank=True)),
                ('section', models.CharField(max_length=100, null=True, blank=True)),
                ('required', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Field',
                'verbose_name_plural': 'Fields',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FieldEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_id', models.IntegerField()),
                ('response', models.CharField(max_length=2000)),
            ],
            options={
                'verbose_name': 'Field entry',
                'verbose_name_plural': 'Field entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, max_length=200, editable=False)),
                ('description', models.CharField(max_length=200, null=True, blank=True)),
                ('version', models.CharField(max_length=20, null=True, blank=True)),
                ('version_date', models.DateField(null=True, blank=True)),
                ('revision_notes', models.CharField(max_length=200, null=True, blank=True)),
                ('status', models.IntegerField(choices=[(1, b'Draft'), (2, b'Published'), (3, b'Archived')])),
            ],
            options={
                'verbose_name': 'Form',
                'verbose_name_plural': 'Forms',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FormEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_time', models.DateTimeField()),
                ('form', models.ForeignKey(related_name=b'entries', to='questionnaire.Form')),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Form entry',
                'verbose_name_plural': 'Form entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fieldentry',
            name='entry',
            field=models.ForeignKey(related_name=b'fields', to='questionnaire.FormEntry'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='form',
            field=models.ForeignKey(related_name=b'fields', to='questionnaire.Form'),
            preserve_default=True,
        ),
    ]
