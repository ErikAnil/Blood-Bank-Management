# Generated by Django 4.2.10 on 2024-03-30 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_feedback_doner_feedback_did'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='did',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='stock',
            name='qty',
            field=models.IntegerField(default=0),
        ),
    ]
