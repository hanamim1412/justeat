# Generated by Django 5.0.4 on 2024-05-15 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_customer_customer_image_rider_rider_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='resto_qrcode',
            field=models.ImageField(blank=True, null=True, upload_to='qrcode_images/'),
        ),
    ]