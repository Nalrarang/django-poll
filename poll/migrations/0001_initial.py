# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('phonenumber', models.CharField(max_length=11)),
                ('survey', models.TextField()),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
