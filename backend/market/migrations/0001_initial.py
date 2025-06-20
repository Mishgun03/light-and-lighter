# Generated by Django 5.2.3 on 2025-06-15 23:21

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
            name='Item',
            fields=[
                ('item_id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('archetype', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('listing_id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('price', models.IntegerField()),
                ('seller', models.CharField(blank=True, max_length=255, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField()),
                ('expires_at', models.DateTimeField()),
                ('attributes', models.JSONField(default=dict)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='market.item')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('avg_price', models.FloatField()),
                ('min_price', models.IntegerField()),
                ('max_price', models.IntegerField()),
                ('volume', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_history', to='market.item')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites_by', to='market.item')),
            ],
            options={
                'unique_together': {('user', 'item')},
            },
        ),
    ]
