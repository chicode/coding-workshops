# Generated by Django 2.1.1 on 2018-10-24 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0017_workshop_source_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='source_url',
            field=models.URLField(blank=True, max_length=300),
        ),
    ]
