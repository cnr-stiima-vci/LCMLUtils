# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcmlutils', '0002_auto_20170324_0900'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lccs3class',
            options={'verbose_name': 'lccs3 class', 'verbose_name_plural': 'lccs3 classes'},
        ),
        migrations.AddField(
            model_name='xsdvalidator',
            name='link',
            field=models.CharField(max_length=128, null=True, verbose_name='link', blank=True),
        ),
        migrations.AddField(
            model_name='xsdvalidator',
            name='link_type',
            field=models.CharField(max_length=64, null=True, verbose_name='link type'),
        ),
    ]
