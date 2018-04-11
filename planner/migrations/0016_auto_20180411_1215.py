# Generated by Django 2.0.1 on 2018-04-11 10:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0015_auto_20180408_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garden',
            name='postal_code',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(9999), django.core.validators.MinValueValidator(1000)]),
        ),
    ]
