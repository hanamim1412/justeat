# Generated by Django 5.0.4 on 2024-05-18 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0032_alter_payment_mop_alter_payment_reference_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='amount_paid',
        ),
    ]
