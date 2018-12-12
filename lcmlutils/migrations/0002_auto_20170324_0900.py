# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcmlutils', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LCCS3Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='validator name')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('xml_text', models.TextField(verbose_name='XML text')),
                ('active', models.BooleanField(default=False, verbose_name='active')),
            ],
            options={
                'db_table': 'lcmlutils_lccs3classes',
            },
        ),
        migrations.AlterField(
            model_name='xsdvalidator',
            name='xsd_text',
            field=models.TextField(null=True, verbose_name='XSD text', blank=True),
        ),
        migrations.AddField(
            model_name='lccs3class',
            name='validator',
            field=models.ForeignKey(to='lcmlutils.XSDValidator'),
        ),
    ]
