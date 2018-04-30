# Generated by Django 2.0.3 on 2018-04-30 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataverse_connect', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataversefileinfo',
            options={'verbose_name': 'Dataverse File Information', 'verbose_name_plural': 'Dataverse File Information'},
        ),
        migrations.AddField(
            model_name='registereddataverse',
            name='url_scheme',
            field=models.CharField(blank=True, help_text='Used for API formatting', max_length=10),
        ),
    ]
