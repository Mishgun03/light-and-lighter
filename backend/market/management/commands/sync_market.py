from __future__ import annotations

from django.core.management.base import BaseCommand
from django.utils import timezone

from market.api_client import DarkerDBClient
from market.models import Item, PriceSnapshot


class Command(BaseCommand):
    help = "Sync recent market listings for a given item name or id"

    def add_arguments(self, parser):
        parser.add_argument("--item_id", type=str, help="Exact item id")
        parser.add_argument("--item", type=str, help="Item name contains")
        parser.add_argument("--limit", type=int, default=50)

    def handle(self, *args, **options):
        client = DarkerDBClient()
        params = {k: v for k, v in options.items() if k in {"item_id", "item", "limit"} and v}
        data = client.market(**params, condense=True)
        count = 0
        for row in data.get("body", []):
            item_id = row.get("item_id")
            item, _ = Item.objects.update_or_create(
                id=item_id,
                defaults={
                    "archetype": row.get("archetype", ""),
                    "name": row.get("item", item_id),
                    "rarity": row.get("rarity", ""),
                    "type": "",
                    "data": {},
                },
            )
            PriceSnapshot.objects.update_or_create(
                market_id=row.get("id"),
                defaults={
                    "item": item,
                    "price": row.get("price", 0),
                    "price_per_unit": row.get("price_per_unit"),
                    "quantity": row.get("quantity", 1),
                    "created_at": row.get("created_at"),
                    "has_sold": row.get("has_sold", False),
                    "has_expired": row.get("has_expired", False),
                    "attributes": {k: v for k, v in row.items() if k.startswith("primary_") or k.startswith("secondary_")},
                },
            )
            count += 1
        self.stdout.write(self.style.SUCCESS(f"Synced {count} listings"))


