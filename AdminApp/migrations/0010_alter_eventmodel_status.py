# Generated by Django 5.0.2 on 2024-04-16 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0009_alter_eventmodel_event_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventmodel',
            name='status',
            field=models.CharField(default='Active', max_length=8),
        ),
    ]
