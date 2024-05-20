# Generated by Django 5.0.4 on 2024-05-08 15:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_remove_user_is_admin_delete_custom_admin'),
        ('transactions', '0018_alter_order_order_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.customer'),
        ),
    ]