# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-13 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bcgs_numbers',
            options={},
        ),
        migrations.AlterField(
            model_name='bcgs_numbers',
            name='bcgs_id',
            field=models.BigIntegerField(editable=False, primary_key=True, serialize=False),
        ),
    ]
