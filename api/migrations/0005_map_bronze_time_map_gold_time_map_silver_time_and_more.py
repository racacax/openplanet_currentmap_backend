# Generated by Django 4.1.5 on 2023-01-06 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_playeraccount_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='bronze_time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='map',
            name='gold_time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='map',
            name='silver_time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='map',
            name='trackmaster_time',
            field=models.IntegerField(null=True),
        ),
    ]
