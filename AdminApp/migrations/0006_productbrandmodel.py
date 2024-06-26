# Generated by Django 5.0.2 on 2024-03-16 07:50

import AdminApp.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0005_delete_brandmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductBrandModel',
            fields=[
                ('brand_id', models.AutoField(primary_key=True, serialize=False)),
                ('brand_name', models.TextField(max_length=20)),
                ('brand_image', models.ImageField(upload_to=AdminApp.models.upload_to)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminApp.productcategorymodel')),
            ],
            options={
                'db_table': 'Brand Model',
            },
        ),
    ]
