# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcmlutils', '0008_load_initial_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lccs3legend',
            name='xml_text',
            field=models.TextField(verbose_name='XML text', default=''),
        ),
    ]
