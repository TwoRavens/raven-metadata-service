# Generated by Django 2.0.3 on 2018-03-08 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preprocess_jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preprocessjob',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='preprocessjob',
            name='preprocess_file',
            field=models.FileField(blank=True, help_text='Summary metadata created by preprocess', upload_to='preprocess_file/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='preprocessjob',
            name='schema_version',
            field=models.CharField(default='beta', max_length=100),
        ),
        migrations.AlterField(
            model_name='preprocessjob',
            name='source_file',
            field=models.FileField(blank=True, help_text='Source file for preprocess', upload_to='source_file/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='preprocessjob',
            name='state',
            field=models.CharField(choices=[('RECEIVED', 'RECEIVED'), ('PENDING', 'PENDING'), ('DATA_RETRIEVED', 'DATA_RETRIEVED'), ('PREPROCESS_STARTED', 'PREPROCESS_STARTED'), ('SUCCESS', 'SUCCESS'), ('FAILURE', 'FAILURE')], default='RECEIVED', max_length=100),
        ),
    ]