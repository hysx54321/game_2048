# Generated by Django 3.0.2 on 2020-01-19 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('two_zero_four_eight', '0002_auto_20200119_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_reconstruction',
            field=models.TextField(default=None, null=True, verbose_name='Game Reconstruction'),
        ),
    ]