from __future__ import annotations

from django.core.management.base import BaseCommand

from market.api_client import DarkerDBClient
from market.models import PopulationSnapshot


class Command(BaseCommand):
    help = "Sync current population snapshot"

    def handle(self, *args, **options):
        client = DarkerDBClient()
        data = client.population()
        body = data.get("body", {})
        if body:
            PopulationSnapshot.objects.update_or_create(
                timestamp=body.get("timestamp"),
                defaults={
                    "num_online": body.get("num_online", 0),
                    "num_lobby": body.get("num_lobby", 0),
                    "num_dungeon": body.get("num_dungeon", 0),
                },
            )
            self.stdout.write(self.style.SUCCESS("Population synced"))
        else:
            self.stdout.write("No population data")


