# Generated by Django 2.0.1 on 2018-03-19 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0002_auto_20180316_1626'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='culturaloperation',
            name='is_initial',
        ),
    ]
