# Generated by Django 4.1.5 on 2023-01-08 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_player_last_online'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='game',
            field=models.IntegerField(choices=[(0, 'TM2020'), (1, 'TM2'), (2, 'TMTURBO'), (3, 'TMUF')]),
        ),
        migrations.AlterField(
            model_name='playeraccount',
            name='game',
            field=models.IntegerField(choices=[(0, 'TM2020'), (1, 'TM2'), (2, 'TMTURBO'), (3, 'TMUF')]),
        ),
    ]
