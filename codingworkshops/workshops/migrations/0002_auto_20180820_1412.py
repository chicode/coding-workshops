# Generated by Django 2.1 on 2018-08-20 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='description',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]