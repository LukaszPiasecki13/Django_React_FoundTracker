# Generated by Django 5.0.2 on 2024-04-05 19:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('asset_class', models.CharField()),
                ('currency', models.CharField(max_length=3)),
                ('current_price', models.DecimalField(decimal_places=3, default=0.0, max_digits=16)),
            ],
        ),
        migrations.CreateModel(
            name='AssetClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Asset classes',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=3)),
            ],
            options={
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.CreateModel(
            name='AssetAllocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=3, default=0.0, max_digits=16)),
                ('average_purchase_price', models.DecimalField(decimal_places=3, default=0.0, max_digits=16)),
                ('daily_change', models.DecimalField(decimal_places=3, default=0.0, max_digits=16)),
                ('daily_change_PLN', models.DecimalField(decimal_places=3, default=0.0, max_digits=16)),
                ('participation', models.DecimalField(decimal_places=3, default=0.0, max_digits=16)),
                ('rate_of_return', models.DecimalField(decimal_places=3, default=0.0, max_digits=16)),
                ('rate_of_return_PLN', models.DecimalField(decimal_places=3, default=0.0, max_digits=16)),
                ('profit_PLN', models.DecimalField(decimal_places=3, default=0.0, max_digits=16)),
                ('dividends', models.DecimalField(decimal_places=3, default=0.0, max_digits=16)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.asset')),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('operation_type', models.CharField(max_length=20)),
                ('asset_class', models.CharField()),
                ('ticker', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('currency', models.CharField(max_length=3)),
                ('quantity', models.FloatField()),
                ('price', models.FloatField()),
                ('fee', models.FloatField()),
                ('comment', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pocket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('fees', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('assets', models.ManyToManyField(through='portfolio.AssetAllocation', to='portfolio.asset')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='assetallocation',
            name='pocket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.pocket'),
        ),
    ]