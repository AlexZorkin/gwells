# Generated by Django 2.2.7 on 2019-11-21 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aquifers', '0024_waterrightslicence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aquiferresource',
            name='section',
            field=models.ForeignKey(db_column='aquifer_resource_section_code', help_text='The section (category) of this resource.', on_delete=django.db.models.deletion.PROTECT, to='aquifers.AquiferResourceSection', verbose_name='Aquifer Resource Section'),
        ),
        migrations.AlterField(
            model_name='waterrightslicence',
            name='purpose',
            field=models.ForeignKey(blank=True, db_column='water_rights_purpose_code', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='licences', to='aquifers.WaterRightsPurpose', verbose_name='Water Rights Purpose Reference'),
        ),
    ]