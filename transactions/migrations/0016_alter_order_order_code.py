# Generated by Django 5.0.4 on 2024-05-08 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0015_alter_order_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_code',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
