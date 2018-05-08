# Generated by Django 2.0.3 on 2018-05-01 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataverse_connect', '0002_auto_20180430_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataversefileinfo',
            name='dataset_id',
            field=models.IntegerField(default=-1, verbose_name='Dataverse dataset Id'),
        ),
        migrations.AlterField(
            model_name='registereddataverse',
            name='url_scheme',
            field=models.CharField(blank=True, help_text='Created on save. Used for API formatting', max_length=10),
        ),
    ]