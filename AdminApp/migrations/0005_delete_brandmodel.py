# Generated by Django 5.0.2 on 2024-03-11 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0004_brandmodel'),
        ('SellerApp', '0006_alter_audiospecificationmodel_product_brand_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BrandModel',
        ),
    ]
