# Generated by Django 4.1.5 on 2023-01-06 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_playeraccount_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='last_online',
            field=models.DateTimeField(null=True),
        ),
    ]
