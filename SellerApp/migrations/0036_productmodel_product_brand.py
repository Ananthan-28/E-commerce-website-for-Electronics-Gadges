# Generated by Django 5.0.2 on 2024-05-19 11:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0012_alter_productcategorymodel_category_image'),
        ('SellerApp', '0035_remove_productmodel_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='product_brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminApp.productbrandmodel'),
        ),
    ]
