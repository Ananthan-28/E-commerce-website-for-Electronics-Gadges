# Generated by Django 5.0.2 on 2024-04-21 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0014_alter_userdatamodel_user_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdatamodel',
            name='user_email',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='userdatamodel',
            name='user_name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='userdatamodel',
            name='user_phone',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
