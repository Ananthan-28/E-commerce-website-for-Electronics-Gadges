# Generated by Django 5.0.2 on 2024-05-13 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SellerApp', '0033_rename_seller_product_stock_productmodel_product_stock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productmodel',
            old_name='product_stock',
            new_name='seller_product_stock',
        ),
    ]
