# Generated by Django 2.0.3 on 2018-07-13 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preprocess_jobs', '0002_auto_20180502_1430'),
        ('dataverse_connect', '0006_dataversefileinfo_dataset_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataversefileinfo',
            name='persistent_id',
            field=models.CharField(default=None, max_length=255, verbose_name='persistentId'),
        ),
        migrations.AlterField(
            model_name='dataversefileinfo',
            name='datafile_id',
            field=models.IntegerField(default=-1, verbose_name='Datafile Id'),
        ),
        migrations.AlterUniqueTogether(
            name='dataversefileinfo',
            unique_together={('dataverse', 'datafile_id', 'preprocess_job', 'persistent_id')},
        ),
    ]
