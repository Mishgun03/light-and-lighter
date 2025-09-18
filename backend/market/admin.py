from django.contrib import admin
from .models import Item, PriceSnapshot, Favorite, LeaderboardEntry, PopulationSnapshot


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rarity", "type")
    search_fields = ("id", "name", "archetype")


@admin.register(PriceSnapshot)
class PriceSnapshotAdmin(admin.ModelAdmin):
    list_display = ("item", "price", "created_at", "has_sold")
    list_filter = ("has_sold", "has_expired")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "created_at")


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ("leaderboard_id", "character", "current_position", "score")


@admin.register(PopulationSnapshot)
class PopulationSnapshotAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "num_online", "num_lobby", "num_dungeon")


