# Generated by Django 2.0.5 on 2018-06-03 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platformactivity',
            name='user',
        ),
        migrations.AlterField(
            model_name='policy',
            name='identifier',
            field=models.CharField(default='', max_length=50, primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='PlatformActivity',
        ),
    ]
