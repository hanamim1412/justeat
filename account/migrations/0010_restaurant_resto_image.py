# Generated by Django 5.0.4 on 2024-05-09 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_remove_user_is_admin_delete_custom_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='resto_image',
            field=models.ImageField(blank=True, null=True, upload_to='restaurant_images/'),
        ),
    ]