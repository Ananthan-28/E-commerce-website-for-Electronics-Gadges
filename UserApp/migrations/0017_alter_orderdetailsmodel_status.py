# Generated by Django 5.0.2 on 2024-04-27 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0016_alter_orderdetailsmodel_billing_ref_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetailsmodel',
            name='status',
            field=models.TextField(default='Order Confirmed', max_length=10),
        ),
    ]
