# Generated by Django 5.0.4 on 2024-05-07 12:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_remove_user_is_admin_delete_custom_admin'),
        ('transactions', '0009_remove_menuitem_restaurant_category_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.restaurant'),
        ),
    ]
