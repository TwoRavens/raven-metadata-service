# Generated by Django 2.0.3 on 2018-04-02 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MetadataUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('version_number', models.IntegerField(default=2)),
                ('update_json', jsonfield.fields.JSONField()),
                ('metadata_file', models.FileField(blank=True, help_text='Summary metadata created by preprocess', upload_to='preprocess_file/%Y/%m/%d/')),
                ('note', models.TextField(blank=True)),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='PreprocessJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('is_metadata_public', models.BooleanField(default=True)),
                ('state', models.CharField(choices=[('RECEIVED', 'RECEIVED'), ('PENDING', 'PENDING'), ('DATA_RETRIEVED', 'DATA_RETRIEVED'), ('PREPROCESS_STARTED', 'PREPROCESS_STARTED'), ('SUCCESS', 'SUCCESS'), ('FAILURE', 'FAILURE')], default='RECEIVED', max_length=100)),
                ('task_id', models.CharField(blank=True, max_length=255, verbose_name='queue task id (e.g. celery id)')),
                ('source_file_url', models.URLField(blank=True, verbose_name='direct download url (optional)')),
                ('source_file', models.FileField(blank=True, help_text='Source file for preprocess', upload_to='source_file/%Y/%m/%d/')),
                ('preprocess_file', models.FileField(blank=True, help_text='Summary metadata created by preprocess', upload_to='preprocess_file/%Y/%m/%d/')),
                ('schema_version', models.CharField(default='beta', max_length=100)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('user_message', models.TextField(blank=True, help_text='May be used for error messages, etc')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_preprocess_job', 'View Preprocess Job'),),
            },
        ),
        migrations.AddField(
            model_name='metadataupdate',
            name='orig_metadata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orig_metadata', to='preprocess_jobs.PreprocessJob'),
        ),
        migrations.AddField(
            model_name='metadataupdate',
            name='previous_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='prev_metadata', to='preprocess_jobs.MetadataUpdate'),
        ),
    ]
