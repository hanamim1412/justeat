# Generated by Django 5.0.4 on 2024-05-05 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_order_menu_item_order_quantity_order_subtotal_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='image',
        ),
    ]
