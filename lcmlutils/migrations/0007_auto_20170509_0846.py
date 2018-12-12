# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcmlutils', '0006_auto_20170411_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='lccs3legend',
            name='link',
            field=models.CharField(max_length=128, null=True, verbose_name='link', blank=True),
        ),
        migrations.AddField(
            model_name='lccs3legend',
            name='link_type',
            field=models.CharField(max_length=64, null=True, verbose_name='link type'),
        ),
    ]
