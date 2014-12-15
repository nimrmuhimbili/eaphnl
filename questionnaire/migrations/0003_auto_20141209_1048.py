# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0002_auto_20141209_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldentry',
            name='response',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
    ]
