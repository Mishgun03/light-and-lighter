from rest_framework import serializers
from .models import Item, PriceSnapshot, Favorite, LeaderboardEntry, PopulationSnapshot


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "id",
            "archetype",
            "name",
            "rarity",
            "type",
            "slot_type",
            "armor_type",
            "gear_score",
            "vendor_price",
            "data",
        ]


class PriceSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceSnapshot
        fields = [
            "id",
            "item",
            "market_id",
            "price",
            "price_per_unit",
            "quantity",
            "created_at",
            "has_sold",
            "has_expired",
            "attributes",
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "item", "created_at"]


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaderboardEntry
        fields = [
            "leaderboard_id",
            "character",
            "character_class",
            "rank",
            "score",
            "current_position",
            "previous_position",
            "updated_at",
        ]


class PopulationSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopulationSnapshot
        fields = ["timestamp", "num_online", "num_lobby", "num_dungeon"]


