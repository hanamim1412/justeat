# Generated by Django 5.0.4 on 2024-05-20 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0038_remove_order_rider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='mop',
            field=models.CharField(choices=[('CASH', 'Cash'), ('GCASH', 'Gcash')], max_length=10),
        ),
    ]
