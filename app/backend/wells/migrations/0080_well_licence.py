# Generated by Django 2.2.1 on 2019-05-08 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aquifers', '0021_auto_20190502_0551'),
        ('wells', '0001_squashed_0079_auto_20190506_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='well',
            name='licence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wells', to='aquifers.WaterRightsLicence'),
        ),
    ]