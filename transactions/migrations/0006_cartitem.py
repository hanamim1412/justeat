# Generated by Django 5.0.4 on 2024-05-06 16:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_remove_customer_image_remove_restaurant_image_and_more'),
        ('transactions', '0005_remove_menuitem_category_remove_order_menu_item_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.customer')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.menuitem')),
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.restaurant')),
                ('rider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.rider')),
            ],
        ),
    ]