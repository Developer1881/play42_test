# Generated by Django 2.1.7 on 2019-02-26 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play42_proto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoubleBet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('probability1', models.FloatField(blank=True, default=None, null=True)),
                ('sum1', models.FloatField(blank=True, default=None, null=True)),
                ('probability2', models.FloatField(blank=True, default=None, null=True)),
                ('sum2', models.FloatField(blank=True, default=None, null=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TripleBet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('probability1', models.FloatField(blank=True, default=None, null=True)),
                ('sum1', models.FloatField(blank=True, default=None, null=True)),
                ('probability2', models.FloatField(blank=True, default=None, null=True)),
                ('sum2', models.FloatField(blank=True, default=None, null=True)),
                ('probability3', models.FloatField(blank=True, default=None, null=True)),
                ('sum3', models.FloatField(blank=True, default=None, null=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]