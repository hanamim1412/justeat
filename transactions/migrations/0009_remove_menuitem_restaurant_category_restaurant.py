# Generated by Django 5.0.4 on 2024-05-07 11:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_remove_user_is_admin_delete_custom_admin'),
        ('transactions', '0008_alter_cartitem_menu_item_alter_menuitem_restaurant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='restaurant',
        ),
        migrations.AddField(
            model_name='category',
            name='restaurant',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.restaurant'),
        ),
    ]
