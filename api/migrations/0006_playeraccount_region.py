# Generated by Django 4.1.5 on 2023-01-06 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_map_bronze_time_map_gold_time_map_silver_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='playeraccount',
            name='region',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
