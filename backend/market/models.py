from django.conf import settings
from django.db import models


class Item(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    archetype = models.CharField(max_length=128)
    name = models.CharField(max_length=256, db_index=True)
    rarity = models.CharField(max_length=32, db_index=True)
    type = models.CharField(max_length=64, db_index=True)
    slot_type = models.CharField(max_length=64, null=True, blank=True)
    armor_type = models.CharField(max_length=64, null=True, blank=True)
    gear_score = models.IntegerField(null=True, blank=True)
    vendor_price = models.IntegerField(null=True, blank=True)
    data = models.JSONField(default=dict)

    def __str__(self) -> str:
        return f"{self.name} ({self.rarity})"


class PriceSnapshot(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="snapshots")
    market_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    price = models.IntegerField()
    price_per_unit = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(db_index=True)
    has_sold = models.BooleanField(default=False)
    has_expired = models.BooleanField(default=False)
    attributes = models.JSONField(default=dict)

    class Meta:
        indexes = [
            models.Index(fields=["item", "created_at"]),
        ]


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "item")


class LeaderboardEntry(models.Model):
    leaderboard_id = models.CharField(max_length=32, db_index=True)
    character = models.CharField(max_length=64)
    character_class = models.CharField(max_length=32)
    rank = models.CharField(max_length=64, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    current_position = models.IntegerField()
    previous_position = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("leaderboard_id", "character", "current_position")


class PopulationSnapshot(models.Model):
    timestamp = models.DateTimeField(db_index=True)
    num_online = models.IntegerField()
    num_lobby = models.IntegerField()
    num_dungeon = models.IntegerField()


