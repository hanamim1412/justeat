# Generated by Django 5.0.4 on 2024-05-07 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_rename_customadmin_custom_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.DeleteModel(
            name='Custom_Admin',
        ),
    ]