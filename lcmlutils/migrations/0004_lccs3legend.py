# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcmlutils', '0003_auto_20170411_0548'),
    ]

    operations = [
        migrations.CreateModel(
            name='LCCS3Legend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='legend name')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('active', models.BooleanField(default=False, verbose_name='active')),
            ],
            options={
                'db_table': 'lcmlutils_lccs3legends',
                'verbose_name': 'lccs3 legend',
                'verbose_name_plural': 'lccs3 legends',
            },
        ),
    ]
