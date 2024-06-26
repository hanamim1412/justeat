# Generated by Django 5.0.4 on 2024-05-05 09:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='menu_item',
            field=models.ManyToManyField(blank=True, related_name='order', to='transactions.menuitem'),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='subtotal_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='category',
        ),
        migrations.AlterField(
            model_name='order',
            name='rider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_assigned', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='OrderDetail',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='menu_item', to='transactions.category'),
        ),
    ]
