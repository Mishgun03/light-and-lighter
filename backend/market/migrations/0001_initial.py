from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=64)),
                ('archetype', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=256, db_index=True)),
                ('rarity', models.CharField(max_length=32, db_index=True)),
                ('type', models.CharField(max_length=64, db_index=True)),
                ('slot_type', models.CharField(blank=True, null=True, max_length=64)),
                ('armor_type', models.CharField(blank=True, null=True, max_length=64)),
                ('gear_score', models.IntegerField(blank=True, null=True)),
                ('vendor_price', models.IntegerField(blank=True, null=True)),
                ('data', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='LeaderboardEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leaderboard_id', models.CharField(db_index=True, max_length=32)),
                ('character', models.CharField(max_length=64)),
                ('character_class', models.CharField(max_length=32)),
                ('rank', models.CharField(blank=True, max_length=64, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('current_position', models.IntegerField()),
                ('previous_position', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('leaderboard_id', 'character', 'current_position')},
            },
        ),
        migrations.CreateModel(
            name='PopulationSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(db_index=True)),
                ('num_online', models.IntegerField()),
                ('num_lobby', models.IntegerField()),
                ('num_dungeon', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PriceSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market_id', models.BigIntegerField(blank=True, db_index=True, null=True)),
                ('price', models.IntegerField()),
                ('price_per_unit', models.IntegerField(blank=True, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(db_index=True)),
                ('has_sold', models.BooleanField(default=False)),
                ('has_expired', models.BooleanField(default=False)),
                ('attributes', models.JSONField(default=dict)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snapshots', to='market.item')),
            ],
        ),
        migrations.AddIndex(
            model_name='pricesnapshot',
            index=models.Index(fields=['item', 'created_at'], name='market_pric_item_id_45b0a4_idx'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to='market.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'item')},
            },
        ),
    ]


