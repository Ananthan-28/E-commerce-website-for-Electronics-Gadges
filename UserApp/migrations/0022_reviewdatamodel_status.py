# Generated by Django 5.0.2 on 2024-05-07 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0021_alter_orderdetailsmodel_billing_ref_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewdatamodel',
            name='status',
            field=models.CharField(default='Active', max_length=10),
        ),
    ]
