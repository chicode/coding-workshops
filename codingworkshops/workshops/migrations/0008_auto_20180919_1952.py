# Generated by Django 2.1.1 on 2018-09-19 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0007_auto_20180919_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direction',
            name='description',
            field=models.TextField(),
        ),
    ]