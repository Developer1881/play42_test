# Generated by Django 2.1.7 on 2019-02-26 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play42_proto', '0002_doublebet_triplebet'),
    ]

    operations = [
        migrations.AddField(
            model_name='doublebet',
            name='player1_win1',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='doublebet',
            name='player1_win2',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='doublebet',
            name='player2_win1',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='doublebet',
            name='player2_win2',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
