# Generated by Django 2.0.5 on 2018-06-03 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180603_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policy',
            name='max_operator_distance',
            field=models.FloatField(default=0.0),
        ),
    ]