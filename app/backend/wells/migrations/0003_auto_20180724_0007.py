# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-24 00:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('wells', '0002_auto_20180713_1641'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activitysubmission',
            old_name='well_tag_number',
            new_name='well',
        ),
        migrations.AlterField(
            model_name='activitysubmission',
            name='driller_responsible',
            field=models.ForeignKey(blank=True, db_column='driller_responsible_guid', null=True, on_delete=django.db.models.deletion.PROTECT,
                                    to='registries.Person', verbose_name='Person Responsible for Drilling'),
        ),
        migrations.AlterField(
            model_name='activitysubmission',
            name='work_end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Work End Date'),
        ),
        migrations.AlterField(
            model_name='activitysubmission',
            name='work_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Work Start Date'),
        ),
        migrations.AlterField(
            model_name='well',
            name='owner_province_state',
            field=models.ForeignKey(blank=True, db_column='province_state_code', null=True, on_delete=django.db.models.deletion.CASCADE, to='gwells.ProvinceStateCode', verbose_name='Province'),
        ),
    ]
