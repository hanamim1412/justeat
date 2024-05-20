# Generated by Django 5.0.4 on 2024-05-01 16:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=20)),
                ('default_address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=255)),
                ('business_hours', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Rider',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=20)),
                ('driver_license', models.CharField(max_length=50)),
                ('age', models.PositiveIntegerField()),
            ],
        ),
    ]