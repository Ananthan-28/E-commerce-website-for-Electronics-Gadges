# Generated by Django 5.0.2 on 2024-03-05 18:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AdminApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerDataModel',
            fields=[
                ('seller_id', models.AutoField(primary_key=True, serialize=False)),
                ('seller_licence', models.CharField(max_length=255)),
                ('seller_company_name', models.CharField(max_length=50)),
                ('seller_phone', models.CharField(max_length=15)),
                ('seller_address', models.TextField(max_length=255)),
                ('seller_email', models.CharField(max_length=100)),
                ('seller_pan', models.CharField(max_length=20)),
                ('seller_gst', models.CharField(max_length=50)),
                ('seller_bank_acc', models.CharField(max_length=50)),
                ('seller_IFSC', models.CharField(max_length=50)),
                ('seller_status', models.CharField(default='active', max_length=7)),
            ],
            options={
                'db_table': 'Seller_data_model',
            },
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=50)),
                ('product_brand', models.CharField(max_length=25)),
                ('product_description', models.CharField(max_length=255)),
                ('product_price', models.IntegerField()),
                ('seller_product_quantity', models.IntegerField()),
                ('product_status', models.CharField(default='active', max_length=7)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminApp.productcategory')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SellerApp.sellerdatamodel')),
            ],
            options={
                'db_table': 'Product_model',
            },
        ),
        migrations.CreateModel(
            name='ProductImageModel',
            fields=[
                ('product_image_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_image', models.ImageField(upload_to='product_images/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SellerApp.productmodel')),
            ],
            options={
                'db_table': 'product_image_model',
            },
        ),
        migrations.CreateModel(
            name='ProductDiscount',
            fields=[
                ('discount_id', models.AutoField(primary_key=True, serialize=False)),
                ('discount_amount', models.IntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminApp.eventmodel')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SellerApp.productmodel')),
            ],
            options={
                'db_table': 'product_discount_model',
            },
        ),
        migrations.CreateModel(
            name='PCSpecificationModel',
            fields=[
                ('specification_id', models.AutoField(primary_key=True, serialize=False)),
                ('spec_ram', models.IntegerField()),
                ('spec_processor', models.IntegerField()),
                ('spec_storage', models.IntegerField()),
                ('spec_gpu', models.IntegerField()),
                ('spec_resolution', models.IntegerField()),
                ('spec_display_size', models.IntegerField()),
                ('spec_os', models.CharField(max_length=10)),
                ('spec_refresh_rate', models.IntegerField()),
                ('warranty', models.IntegerField()),
                ('product_price', models.IntegerField()),
                ('product_status', models.CharField(default='active', max_length=7)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminApp.productcategory')),
                ('product_img', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SellerApp.productimagemodel')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SellerApp.productmodel')),
            ],
            options={
                'db_table': 'pc_specification_model',
            },
        ),
        migrations.CreateModel(
            name='AudioModel',
            fields=[
                ('specification_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_type', models.TextField(max_length=50)),
                ('spec_bluetooth', models.TextField(max_length=5)),
                ('spec_playback', models.CharField(max_length=10)),
                ('spec_mic', models.CharField(max_length=5)),
                ('spec_latency', models.IntegerField()),
                ('warranty', models.IntegerField()),
                ('product_price', models.IntegerField()),
                ('product_status', models.CharField(default='active', max_length=7)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminApp.productcategory')),
                ('product_img', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SellerApp.productimagemodel')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SellerApp.productmodel')),
            ],
            options={
                'db_table': 'audio_model',
            },
        ),
        migrations.CreateModel(
            name='SmartPhoneModel',
            fields=[
                ('specification_id', models.AutoField(primary_key=True, serialize=False)),
                ('spec_ram', models.IntegerField()),
                ('spec_processor', models.IntegerField()),
                ('spec_storage', models.IntegerField()),
                ('spec_resolution', models.IntegerField()),
                ('spec_display_size', models.IntegerField()),
                ('color', models.CharField(max_length=10)),
                ('spec_battery', models.IntegerField()),
                ('spec_camera', models.IntegerField()),
                ('spec_os', models.CharField(max_length=10)),
                ('warranty', models.IntegerField()),
                ('product_price', models.IntegerField()),
                ('product_status', models.CharField(default='active', max_length=7)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminApp.productcategory')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SellerApp.productmodel')),
                ('product_img', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SellerApp.productimagemodel')),
            ],
            options={
                'db_table': 'smartphone_model',
            },
        ),
        migrations.CreateModel(
            name='TeleVisionModels',
            fields=[
                ('specification_id', models.AutoField(primary_key=True, serialize=False)),
                ('spec_resolution', models.IntegerField()),
                ('spec_display_size', models.IntegerField()),
                ('spec_os', models.CharField(max_length=10)),
                ('warranty', models.IntegerField()),
                ('product_price', models.IntegerField()),
                ('product_status', models.CharField(default='active', max_length=7)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminApp.productcategory')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SellerApp.productmodel')),
                ('product_img', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SellerApp.productimagemodel')),
            ],
            options={
                'db_table': 'Television_model',
            },
        ),
    ]
