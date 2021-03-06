# Generated by Django 2.0.3 on 2018-04-30 19:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('preprocess_jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataverseFileInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('datafile_id', models.IntegerField(verbose_name='Datafile Id')),
                ('dataverse_doi', models.CharField(blank=True, max_length=255, verbose_name='DOI')),
                ('formatted_citation', models.TextField(blank=True)),
                ('jsonld_citation', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredDataverse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('dataverse_url', models.URLField(help_text='Example: "https://dataverse.harvard.edu"', unique=True)),
                ('network_location', models.CharField(blank=True, help_text='Created on save. Used for matching', max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True, help_text='optional')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='dataversefileinfo',
            name='dataverse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataverse_connect.RegisteredDataverse'),
        ),
        migrations.AddField(
            model_name='dataversefileinfo',
            name='preprocess_job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preprocess_jobs.PreprocessJob'),
        ),
        migrations.AlterUniqueTogether(
            name='dataversefileinfo',
            unique_together={('dataverse', 'datafile_id', 'preprocess_job')},
        ),
    ]
