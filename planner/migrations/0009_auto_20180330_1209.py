# Generated by Django 2.0.1 on 2018-03-30 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('planner', '0008_harvest'),
    ]

    operations = [
        migrations.CreateModel(
            name='HarvestDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('harvest_date', models.DateField()),
                ('kg_produced', models.IntegerField(blank=True, default=0)),
                ('total_selling_price', models.IntegerField(blank=True, default=0)),
                ('executor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='harvest',
            name='historyitem_ptr',
        ),
        migrations.DeleteModel(
            name='Harvest',
        ),
        migrations.AddField(
            model_name='cultivatedarea',
            name='harvest_details',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='planner.HarvestDetails'),
        ),
    ]