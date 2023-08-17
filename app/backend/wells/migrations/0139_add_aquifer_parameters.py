# Generated by Django 2.2.28 on 2023-03-18 21:17

from django.db import migrations, models
from django.utils.timezone import utc
import django.db.models.deletion
import django.utils.timezone
import gwells.db_comments.model_mixins
import wells.data_migrations
import datetime
import uuid

MIGRATE_HYDRAULIC_TABLE_INFO = """
    INSERT INTO aquifer_parameters (
        aquifer_parameters_guid,
        well_tag_number,
        storativity,
        transmissivity,
        hydraulic_conductivity,
        specific_yield,
        test_duration,
        comments,
        create_user,
        update_user,
        create_date,
        update_date
    )
    SELECT
        public.uuid_generate_v4() AS aquifer_parameters_guid,
        w.well_tag_number,
        w.storativity,
        w.transmissivity,
        w.hydraulic_conductivity,
        w.specific_yield,
        w.testing_duration,
        w.testing_method,
        'WELLS',
        'WELLS',
        now(),
        now()
    FROM
        well w
    WHERE
        w.storativity IS NOT NULL
        OR w.transmissivity IS NOT NULL
        OR w.hydraulic_conductivity IS NOT NULL
        OR w.specific_yield IS NOT NULL
        OR w.testing_duration IS NOT NULL
        OR w.testing_method IS NOT NULL;
"""

REVERSE_MIGRATE_HYDRAULIC_TABLE_INFO = """
    DROP TABLE aquifer_parameters;
    DROP TABLE pumping_test_description_code;
    DROP TABLE analysis_method_code;
"""

CREATE_EXPORT_AQUIFER_PARAMETERS_VIEW_V1_SQL = """
DROP VIEW IF EXISTS export_aquifer_parameters_v1_view;
CREATE OR REPLACE view export_aquifer_parameters_v1_view as
SELECT
  ap.well_tag_number,
  ap.testing_number,
  ap.start_date_pumping_test,
  tt.description AS pumping_test_description,
  ap.test_duration,
  be.description AS boundary_effect,
  ap.storativity,
  ap.transmissivity,
  ap.hydraulic_conductivity,
  ap.specific_yield,
  ap.specific_capacity,
  am.description AS analysis_method,
  ap.comments
FROM
  aquifer_parameters AS ap
LEFT JOIN
  pumping_test_description_code AS tt ON ap.pumping_test_description_code = tt.pumping_test_description_code
LEFT JOIN
  boundary_effect_code AS be ON ap.boundary_effect_code = be.boundary_effect_code
LEFT JOIN
  analysis_method_code AS am ON ap.analysis_method_code = am.analysis_method_code
INNER JOIN
  well ON ap.well_tag_number = well.well_tag_number
WHERE
  well.well_publication_status_code = 'Published' OR well.well_publication_status_code IS NULL
ORDER BY
  ap.testing_number;
"""

REVERSE_CREATE_EXPORT_AQUIFER_PARAMETERS_VIEW_V1_SQL = """
DROP VIEW IF EXISTS export_aquifer_parameters_v1_view;
"""

class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0138_add_conductor_casing_option'),
    ]

    operations = [
        migrations.CreateModel(
            name='PumpingTestDescriptionCode',
            fields=[
                ('create_user', models.CharField(max_length=60)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_user', models.CharField(max_length=60)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('display_order', models.PositiveIntegerField()),
                ('effective_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('expiry_date', models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc))),
                ('pumping_test_description_code', models.CharField(db_column='pumping_test_description_code', editable=False, max_length=50, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'pumping_test_description_code',
                'ordering': ['display_order', 'description'],
            },
            bases=(models.Model, gwells.db_comments.model_mixins.DBComments),
        ),
        migrations.CreateModel(
            name='AnalysisMethodCode',
            fields=[
                ('create_user', models.CharField(max_length=60)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_user', models.CharField(max_length=60)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('display_order', models.PositiveIntegerField()),
                ('effective_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('expiry_date', models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc))),
                ('analysis_method_code', models.CharField(db_column='analysis_method_code', editable=False, max_length=50, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'analysis_method_code',
                'ordering': ['display_order', 'description'],
            },
            bases=(models.Model, gwells.db_comments.model_mixins.DBComments),
        ),
        migrations.CreateModel(
            name='AquiferParameters',
            fields=[
                ('testing_number', models.AutoField(primary_key=True, serialize=False, verbose_name='Testing Number')),
                ('aquifer_parameters_guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=False, serialize=False)),
                ('activity_submission', models.ForeignKey(blank=True, db_column='filing_number', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='aquifer_parameters_set', to='wells.ActivitySubmission')),
                ('well', models.ForeignKey(blank=True, db_column='well_tag_number', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='aquifer_parameters_set', to='wells.Well')),
                ('start_date_pumping_test', models.DateField(null=True, verbose_name='Start date of pumping test')),
                ('pumping_test_description', models.ForeignKey(blank=True, db_column='pumping_test_description_code', null='True', on_delete=django.db.models.deletion.PROTECT, to='wells.PumpingTestDescriptionCode', verbose_name='Testing Description')),
                ('test_duration', models.PositiveIntegerField(blank=True, null=True)),
                ('boundary_effect', models.ForeignKey(blank=True, db_column='boundary_effect_code', null=True, on_delete=django.db.models.deletion.PROTECT, to='wells.BoundaryEffectCode', verbose_name='Boundary Effect')),
                ('storativity', models.DecimalField(blank=True, decimal_places=7, max_digits=8, null=True, verbose_name='Storativity')),
                ('transmissivity', models.DecimalField(blank=True, decimal_places=10, max_digits=30, null=True, verbose_name='Transmissivity')),
                ('hydraulic_conductivity', models.TextField(blank=True, max_length=100, null=True, verbose_name='Hydraulic Conductivity')),
                ('specific_yield', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Specific Yield')),
                ('specific_capacity', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Specific Yield')),
                ('analysis_method', models.ForeignKey(blank=True, db_column='analysis_method_code', null='True', on_delete=django.db.models.deletion.PROTECT, to='wells.AnalysisMethodCode', verbose_name='Analysis Method')),
                ('comments', models.TextField(blank=True, max_length=350, null=True, verbose_name='Testing Comments')),
                ('create_user', models.CharField(max_length=60)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_user', models.CharField(max_length=60)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'aquifer_parameters',
                'ordering': ['start_date_pumping_test'],
            },
            bases=(models.Model, gwells.db_comments.model_mixins.DBComments),
        ),
        migrations.AddField(
            model_name='fieldsprovided',
            name='aquifer_parameters_set',
            field=models.BooleanField(default=False),
        ),
        migrations.RunSQL(
          MIGRATE_HYDRAULIC_TABLE_INFO,
          REVERSE_MIGRATE_HYDRAULIC_TABLE_INFO
        ),
        migrations.RunPython(
            code=wells.data_migrations.load_pumping_test_description_codes,
            reverse_code=wells.data_migrations.unload_pumping_test_description_codes
        ),
        migrations.RunPython(
            code=wells.data_migrations.load_analysis_method_codes,
            reverse_code=wells.data_migrations.unload_analysis_method_codes
        ),
        migrations.RunSQL(
          CREATE_EXPORT_AQUIFER_PARAMETERS_VIEW_V1_SQL,
          REVERSE_CREATE_EXPORT_AQUIFER_PARAMETERS_VIEW_V1_SQL
        )
    ]
