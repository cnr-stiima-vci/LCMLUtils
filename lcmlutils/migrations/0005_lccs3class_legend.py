# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcmlutils', '0004_lccs3legend'),
    ]

    operations = [
        migrations.AddField(
            model_name='lccs3class',
            name='legend',
            field=models.ForeignKey(default=None, to='lcmlutils.LCCS3Legend'),
        ),
    ]
