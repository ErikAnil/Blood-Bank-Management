# Generated by Django 3.2.25 on 2024-04-10 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_bloodrequest_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloodrequest',
            name='city',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='city',
        ),
    ]
