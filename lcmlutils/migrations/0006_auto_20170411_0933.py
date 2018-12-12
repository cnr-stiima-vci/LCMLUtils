# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcmlutils', '0005_lccs3class_legend'),
    ]

    operations = [
        migrations.AddField(
            model_name='lccs3legend',
            name='xml_text',
            field=models.TextField(default=b'', verbose_name='XML text'),
        ),
        migrations.AlterField(
            model_name='lccs3class',
            name='name',
            field=models.CharField(unique=True, max_length=255, verbose_name='class name'),
        ),
    ]
