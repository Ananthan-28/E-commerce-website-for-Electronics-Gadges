# Generated by Django 5.0.2 on 2024-03-25 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0008_eventmodel_event_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventmodel',
            name='event_img',
            field=models.ImageField(upload_to='events'),
        ),
    ]
