# Generated by Django 5.0.2 on 2024-04-29 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0019_alter_orderdetailsmodel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetailsmodel',
            name='payment_method',
            field=models.CharField(max_length=20, null=True),
        ),
    ]