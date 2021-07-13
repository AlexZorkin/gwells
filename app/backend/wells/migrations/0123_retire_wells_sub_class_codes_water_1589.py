# Generated by Django 2.2.18 on 2021-02-17 22:10

from django.db import migrations

# What are we doing in this migration?:
#   As per WATER-1589 JIRA ticket, we:
#   - create a new Not Applicable for WATR_SPPLY well_sublclass_code
#   - retire well_subclass_code = 'SPECIAL' AND well_class_code = 'GEOTECH'
#       well_subclass_code = 'DOMESTIC' AND well_class_code = 'WATR_SPPLY'
#       well_subclass_code = 'NON_DOMEST' AND well_class_code = 'WATR_SPPLY'
#       by altering the expiry_date to pgsql now()
#   - update the activity_submission records where well_subclass_code is DOMESTIC OR NON_DOMEST and class code is WATR_SPPLY to WATR_SPPLY/NA
#   - update the well records where well_subclass_code is DOMESTIC OR NON_DOMEST and class code is WATR_SPPLY to WATR_SPPLY/NA
#
#   While running this migration I found that the fixtures run after the migration
#       This causes issues cause our code table data for well class codes and well subclass codes aren't present
#   3 well subclass codes have orphaned parent well class code records (ie. there's no well class code for these and its null) (new ticket to be created for a cleanup on that)
#   - Adjusted the fixtures to not create the code table values for well class code and well subclass code, this is done in the migration
#
# Manual Testing Instructions: (automating this as a test doesn't seem straight foward):
#   Developer review steps:
#   1. pull code, ensuring you're starting from a fresh database
#       to do this, ensure that you do not have a volume for postgres (docker volume ls | grep gwells_pgdata-volume) should return no rows then run docker volume rm gwells_pgdata-volume
#       if this is a problem (volume in use) run docker-compose down then delete the volume docker volume rm gwells_pgdata-volume
#   2. run docker-compose up
#   3. once the backend container is running, connect to the database and run the following sql commands:
#
#       -- are the subclass codes expired?
#       select count(*) as subclass_codes_expired from well_subclass_code where expiry_date < now() and update_user = 'WATER-1589';
#
#       -- is our new subclass_code present?
#       select count(*) as new_subclass_present from well_subclass_code where create_date > '2021-01-01' and create_user = 'WATER-1589';
#
#       -- get wells with the expired subclass guids (track the resulting count)
#       select count(*) from well where well_subclass_guid in ('5a3147d8-47e7-11e7-a919-92ebcb67fe33',
#           '5a313ffe-47e7-11e7-a919-92ebcb67fe33',
#           '5a3141c0-47e7-11e7-a919-92ebcb67fe33');
#
#       -- run the update (track the resulting count):
#       UPDATE well
#     SET well_subclass_guid = (SELECT well_subclass_guid FROM well_subclass_code WHERE well_subclass_code = 'NA' AND well_class_code = 'WATR_SPPLY' LIMIT 1),
#         well_class_code = 'WATR_SPPLY',
#         update_user = 'WATER-1589',
#         update_date = now()
#     WHERE well_subclass_guid in (SELECT well_subclass_guid FROM well_subclass_code
#         WHERE (well_subclass_code = 'DOMESTIC' AND well_class_code = 'WATR_SPPLY')
#         OR (well_subclass_code = 'NON_DOMEST' AND well_class_code = 'WATR_SPPLY'));
#
#       --  ensure that the well records have been changed and do not have well_subclass guids from expired subclass codes (track the resulting count)
#       select count(*) from well where well_subclass_guid in ('5a3147d8-47e7-11e7-a919-92ebcb67fe33',
#           '5a313ffe-47e7-11e7-a919-92ebcb67fe33',
#           '5a3141c0-47e7-11e7-a919-92ebcb67fe33');
#
#       -- ensure that we now have well records with our new subclass guid (track this result)
#       select count(*) from well where well_subclass_guid = 'ce97445a-664e-44f1-a096-95c97ffd084e' and update_user = 'WATER-1589';
#
#       -- finally, run this select where we double check we still have wells records that were not changed (not in)
#       select * from well where well_subclass_guid not in ('5a3147d8-47e7-11e7-a919-92ebcb67fe33',
#           '5a313ffe-47e7-11e7-a919-92ebcb67fe33',
#           '5a3141c0-47e7-11e7-a919-92ebcb67fe33')
#   That's the end of the proofing

USER = 'WATER-1589'
ETL_USER = 'ETL_USER'
WELLS_USER = 'WELLS_USER'
NA_WATR_SPPLY_WELL_SUBCLASS_CODE_UUID = 'ce97445a-664e-44f1-a096-95c97ffd084e'
DEFAULT_NEVER_EXPIRES_DATE = '9999-12-31 23:59:59.999999+00'

# insert well class codes if they're not present
CREATE_IF_NOT_EXISTS_WELL_CODES = f"""
    INSERT INTO well_class_code(create_user, create_date, update_user, update_date, well_class_code, description, display_order, effective_date, expiry_date)
        SELECT '{ETL_USER}', '2019-02-12 01:00:00+00', '{ETL_USER}', '2019-02-12 01:00:00+00', 'UNK', 'Unknown', 19, '2019-02-12 01:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}'
    WHERE NOT EXISTS (SELECT 1 FROM well_class_code WHERE well_class_code = 'UNK');
    
    INSERT INTO well_class_code(create_user, create_date, update_user, update_date, well_class_code, description, display_order, effective_date, expiry_date)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', 'WATR_SPPLY', 'Water Supply', 2, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}'
    WHERE NOT EXISTS (SELECT 1 FROM well_class_code WHERE well_class_code = 'WATR_SPPLY');
    
    INSERT INTO well_class_code(create_user, create_date, update_user, update_date, well_class_code, description, display_order, effective_date, expiry_date)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', 'MONITOR', 'Monitoring', 4, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}'
    WHERE NOT EXISTS (SELECT 1 FROM well_class_code WHERE well_class_code = 'MONITOR');

    INSERT INTO well_class_code(create_user, create_date, update_user, update_date, well_class_code, description, display_order, effective_date, expiry_date)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', 'INJECTION', 'Injection', 6, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}'
    WHERE NOT EXISTS (SELECT 1 FROM well_class_code WHERE well_class_code = 'INJECTION');

    INSERT INTO well_class_code(create_user, create_date, update_user, update_date, well_class_code, description, display_order, effective_date, expiry_date)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', 'GEOTECH', 'Geotechnical', 8, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}'
    WHERE NOT EXISTS (SELECT 1 FROM well_class_code WHERE well_class_code = 'GEOTECH');
    
    INSERT INTO well_class_code(create_user, create_date, update_user, update_date, well_class_code, description, display_order, effective_date, expiry_date)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', 'RECHARGE', 'Recharge', 12, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}'
    WHERE NOT EXISTS (SELECT 1 FROM well_class_code WHERE well_class_code = 'RECHARGE');

    INSERT INTO well_class_code(create_user, create_date, update_user, update_date, well_class_code, description, display_order, effective_date, expiry_date)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', 'REMEDIATE', 'Remediation', 14, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}'
    WHERE NOT EXISTS (SELECT 1 FROM well_class_code WHERE well_class_code = 'REMEDIATE');

    INSERT INTO well_class_code(create_user, create_date, update_user, update_date, well_class_code, description, display_order, effective_date, expiry_date)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', 'CLS_LP_GEO', 'Closed Loop Geo', 16, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}'
    WHERE NOT EXISTS (SELECT 1 FROM well_class_code WHERE well_class_code = 'CLS_LP_GEO');

    INSERT INTO well_class_code(create_user, create_date, update_user, update_date, well_class_code, description, display_order, effective_date, expiry_date)
        SELECT '{WELLS_USER}', '2017-07-01 08:00:00+00', '{WELLS_USER}', '2017-07-01 08:00:00+00', 'DEW_DRA', 'Dewatering/drainage', 20, '2020-01-01 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}'
    WHERE NOT EXISTS (SELECT 1 FROM well_class_code WHERE well_class_code = 'DEW_DRA');
    
    INSERT INTO well_class_code(create_user, create_date, update_user, update_date, well_class_code, description, display_order, effective_date, expiry_date)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', 'DEWATERING', 'Dewatering', 10, '2018-05-17 00:00:00+00', '2020-07-28 00:00:00+00'
    WHERE NOT EXISTS (SELECT 1 FROM well_class_code WHERE well_class_code = 'DEWATERING');
    
    INSERT INTO well_class_code(create_user, create_date, update_user, update_date, well_class_code, description, display_order, effective_date, expiry_date)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', 'DRAINAGE', 'Drainage', 10, '2018-05-17 00:00:00+00', '2020-07-28 00:00:00+00'
    WHERE NOT EXISTS (SELECT 1 FROM well_class_code WHERE well_class_code = 'DRAINAGE');    
"""

# insert well subclass codes if they're not present
CREATE_IF_NOT_EXISTS_WELL_SUBCLASS_CODES = f"""
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '5a3152c8-47e7-11e7-a919-92ebcb67fe33', 'BOREHOLE', 'Borehole', 100, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', NULL
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'BOREHOLE' AND well_class_code IS NULL);
    
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '5a315476-47e7-11e7-a919-92ebcb67fe33', 'DOMESTIC', 'Domestic', 100, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', NULL
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'DOMESTIC' AND well_class_code IS NULL);
    
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '5a31562e-47e7-11e7-a919-92ebcb67fe33', 'TEST_PIT', 'Test Pit', 100, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', NULL
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'TEST_PIT' AND well_class_code IS NULL);

    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '5a31460c-47e7-11e7-a919-92ebcb67fe33', 'TEMPORARY', 'Temporary', 100, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', 'MONITOR'
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'TEMPORARY' AND well_class_code = 'MONITOR');
    
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '930540ee-4802-11e7-a919-92ebcb67fe33', 'PERMANENT', 'Permanent', 100, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', 'MONITOR'
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'PERMANENT' AND well_class_code = 'MONITOR');
    
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '5a315106-47e7-11e7-a919-92ebcb67fe33', 'BOREHOLE', 'Borehole', 100, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', 'GEOTECH'
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'BOREHOLE' AND well_class_code = 'GEOTECH');
    
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '93053fd6-4802-11e7-a919-92ebcb67fe33', 'TEST_PIT', 'Test Pit', 100, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', 'GEOTECH'
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'TEST_PIT' AND well_class_code = 'GEOTECH');
    
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '5a3147d8-47e7-11e7-a919-92ebcb67fe33', 'SPECIAL', 'Special', 100, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', 'GEOTECH'
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'SPECIAL' AND well_class_code = 'GEOTECH');
    
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '5a313ffe-47e7-11e7-a919-92ebcb67fe33', 'DOMESTIC', 'Domestic', 100, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', 'WATR_SPPLY'
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'DOMESTIC' AND well_class_code = 'WATR_SPPLY');
    
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '5a3141c0-47e7-11e7-a919-92ebcb67fe33', 'NON_DOMEST', 'Non Domestic', 100, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', 'WATR_SPPLY'
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'NON_DOMEST' AND well_class_code = 'WATR_SPPLY');
    
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '93053cc0-4802-11e7-a919-92ebcb67fe33', 'PERMANENT', 'Permanent', 100, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', 'INJECTION'
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'PERMANENT' AND well_class_code = 'INJECTION');
    
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '5a314404-47e7-11e7-a919-92ebcb67fe33', 'TEMPORARY', 'Temporary', 100, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', 'DEWATERING'
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'TEMPORARY' AND well_class_code = 'DEWATERING');
    
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '5a314ee0-47e7-11e7-a919-92ebcb67fe33', 'PERMANENT', 'Permanent', 100, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', 'DEWATERING'
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'PERMANENT' AND well_class_code = 'DEWATERING');
    
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '3fa278b0-4ca1-11e7-b114-b2f933d5fe66', 'PERMANENT', 'Permanent', 100, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', 'REMEDIATE'
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'PERMANENT' AND well_class_code = 'REMEDIATE');
    
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '3fa27b8a-4ca1-11e7-b114-b2f933d5fe66', 'PERMANENT', 'Permanent', 100, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', 'DRAINAGE'
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'PERMANENT' AND well_class_code = 'DRAINAGE');
    
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{ETL_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '3fa27c98-4ca1-11e7-b114-b2f933d5fe66', 'NA', 'Not Applicable', 100, '2018-05-17 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', 'CLS_LP_GEO'
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'NA' AND well_class_code = 'CLS_LP_GEO');

    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{WELLS_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '46300f40-fc6b-4c77-a58e-74472cd69f5d', 'PERMANENT', 'Permanent', 100, '2020-01-01 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', 'DEW_DRA'
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'PERMANENT' AND well_class_code = 'DEW_DRA');
    
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, well_subclass_guid, well_subclass_code, description, display_order, effective_date, expiry_date, well_class_code)
        SELECT '{WELLS_USER}', '2017-07-01 08:00:00+00', '{ETL_USER}', '2017-07-01 08:00:00+00', '6f124222-ab9e-43c7-89e4-a2b8673611cf', 'TEMPORARY', 'Temporary', 100, '2020-01-01 00:00:00+00', '{DEFAULT_NEVER_EXPIRES_DATE}', 'DEW_DRA'
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'TEMPORARY' AND well_class_code = 'DEW_DRA');    
"""

# create our new well sublcass code named NA for WATR_SPPLY if it's not present
CREATE_NA_WATR_SPPLY_WELL_SUBCLASS_CODE = f"""
    INSERT INTO well_subclass_code(create_user, create_date, update_user, update_date, display_order, effective_date, expiry_date, well_subclass_guid, well_subclass_code, description, well_class_code)
        SELECT '{USER}', now(), '{USER}', now(), 100, now(), '9999-12-31 23:59:59.999999', '{NA_WATR_SPPLY_WELL_SUBCLASS_CODE_UUID}', 'NA', 'Not Applicable', 'WATR_SPPLY'
    WHERE NOT EXISTS (SELECT 1 FROM well_subclass_code WHERE well_subclass_code = 'NA' AND well_class_code = 'WATR_SPPLY');
"""

# retire the 3 well subclass codes
UPDATE_RETIRE_WELL_SUBCLASS_CODES = f"""
    UPDATE well_subclass_code 
    SET expiry_date = now(),
        update_user = '{USER}',
        update_date = now()
    WHERE (well_subclass_code = 'SPECIAL' AND well_class_code = 'GEOTECH')
        OR (well_subclass_code = 'DOMESTIC' AND well_class_code = 'WATR_SPPLY')
        OR (well_subclass_code = 'NON_DOMEST' AND well_class_code = 'WATR_SPPLY');
"""

# update the submission records for retired subclass code WATR_SPPLY/DOMESTIC and WATR_SPPLY/NON_DOMEST, setting them to our new WATR_SPPLY/NA code
UPDATE_SUBMISSIONS_RETIRE_SUBCLASS_CODES_DOM_NON_WATR_SPPLY = f"""
    UPDATE activity_submission
    SET well_subclass_guid = (SELECT well_subclass_guid FROM well_subclass_code WHERE well_subclass_code = 'NA' AND well_class_code = 'WATR_SPPLY' LIMIT 1),
        well_class_code = 'WATR_SPPLY',
        update_user = '{USER}',
        update_date = now()    
    WHERE well_subclass_guid in (SELECT well_subclass_guid FROM well_subclass_code
        WHERE (well_subclass_code = 'DOMESTIC' AND well_class_code = 'WATR_SPPLY')
        OR (well_subclass_code = 'NON_DOMEST' AND well_class_code = 'WATR_SPPLY'));
"""

# update the well records for retired subclass code WATR_SPPLY/DOMESTIC and WATR_SPPLY/NON_DOMEST, setting them to our new WATR_SPPLY/NA code
UPDATE_WELLS_RETIRE_SUBCLASS_CODES_DOM_NON_WATR_SPPLY = f"""
    UPDATE well
    SET well_subclass_guid = (SELECT well_subclass_guid FROM well_subclass_code WHERE well_subclass_code = 'NA' AND well_class_code = 'WATR_SPPLY' LIMIT 1),
        well_class_code = 'WATR_SPPLY',
        update_user = '{USER}',
        update_date = now()
    WHERE well_subclass_guid in (SELECT well_subclass_guid FROM well_subclass_code
        WHERE (well_subclass_code = 'DOMESTIC' AND well_class_code = 'WATR_SPPLY')
        OR (well_subclass_code = 'NON_DOMEST' AND well_class_code = 'WATR_SPPLY'));
"""


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0122_remove_well_licenced_status'),
    ]

    operations = [
        migrations.RunSQL(CREATE_IF_NOT_EXISTS_WELL_CODES),
        migrations.RunSQL(CREATE_IF_NOT_EXISTS_WELL_SUBCLASS_CODES),
        migrations.RunSQL(CREATE_NA_WATR_SPPLY_WELL_SUBCLASS_CODE),
        migrations.RunSQL(UPDATE_RETIRE_WELL_SUBCLASS_CODES),
        migrations.RunSQL(UPDATE_SUBMISSIONS_RETIRE_SUBCLASS_CODES_DOM_NON_WATR_SPPLY),
        migrations.RunSQL(UPDATE_WELLS_RETIRE_SUBCLASS_CODES_DOM_NON_WATR_SPPLY)
    ]
