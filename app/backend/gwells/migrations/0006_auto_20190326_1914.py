# Generated by Django 2.1.7 on 2019-03-26 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gwells', '0005_auto_20190309_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lithologycolourcode',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Colour Description'),
        ),
        migrations.AlterField(
            model_name='lithologyhardnesscode',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Hardness'),
        ),
        migrations.AlterField(
            model_name='lithologymaterialcode',
            name='description',
            field=models.CharField(max_length=255, verbose_name='Material Description'),
        ),
    ]