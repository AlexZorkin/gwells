# Generated by Django 2.1.4 on 2019-01-07 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0048_auto_20181231_2249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activitysubmission',
            old_name='avi',
            new_name='aquifer_vulnerability_index',
        ),
        migrations.RenameField(
            model_name='well',
            old_name='avi',
            new_name='aquifer_vulnerability_index',
        ),
    ]
