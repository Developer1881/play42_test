# Generated by Django 2.1.7 on 2019-02-27 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play42_proto', '0006_nbet_published_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='nbet',
            name='avg_bet',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='nbet',
            name='coeficient_profit',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='nbet',
            name='final_company_profit',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='nbet',
            name='total_bet',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]