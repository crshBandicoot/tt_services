# Generated by Django 4.0.6 on 2022-07-11 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='location',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
