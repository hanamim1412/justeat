# Generated by Django 5.0.4 on 2024-05-08 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0010_alter_category_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='note',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
