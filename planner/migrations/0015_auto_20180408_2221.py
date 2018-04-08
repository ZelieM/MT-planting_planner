# Generated by Django 2.0.1 on 2018-04-08 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0014_auto_20180407_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garden',
            name='activity_data_available_for_research',
            field=models.BooleanField(default=True, verbose_name="J'accepte que les données de mes récoltes soient accessibles pour la recherche universitaire"),
        ),
        migrations.AlterField(
            model_name='garden',
            name='details_available_for_research',
            field=models.BooleanField(default=True, verbose_name="J'accepte que les données de mon jardin soient accessibles pour la recherche universitaire"),
        ),
        migrations.AlterUniqueTogether(
            name='vegetable',
            unique_together={('name', 'variety', 'garden')},
        ),
    ]
