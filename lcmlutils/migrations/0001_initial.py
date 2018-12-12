# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='XSDValidator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='validator name')),
                ('xsd_text', models.TextField(null=True, verbose_name='sld text', blank=True)),
                ('active', models.BooleanField(default=False, verbose_name='active')),
            ],
            options={
                'db_table': 'lcmlutils_xsdvalidators',
            },
        ),
    ]
