# Generated by Django 5.0.2 on 2024-04-18 01:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SellerApp', '0026_alter_pcspecificationmodel_spec_gpu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pcspecificationmodel',
            name='product_img',
        ),
    ]
