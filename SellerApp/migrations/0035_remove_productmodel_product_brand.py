# Generated by Django 5.0.2 on 2024-05-19 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SellerApp', '0034_rename_product_stock_productmodel_seller_product_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productmodel',
            name='product_brand',
        ),
    ]
