# Generated by Django 5.0.2 on 2024-04-07 09:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_rename_daily_change_pln_assetallocation_daily_change_xxx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.currency'),
        ),
    ]
