# Generated by Django 5.0.2 on 2024-04-06 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0007_useraddressdatamodel_phone_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddressdatamodel',
            name='address_name',
            field=models.TextField(max_length=50, null=True),
        ),
    ]
