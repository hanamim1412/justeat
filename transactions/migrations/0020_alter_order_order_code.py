# Generated by Django 5.0.4 on 2024-05-08 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0019_order_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_code',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
