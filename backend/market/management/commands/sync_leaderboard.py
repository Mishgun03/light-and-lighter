from __future__ import annotations

from django.core.management.base import BaseCommand

from market.api_client import DarkerDBClient
from market.models import LeaderboardEntry


class Command(BaseCommand):
    help = "Sync a leaderboard by id"

    def add_arguments(self, parser):
        parser.add_argument("leaderboard_id", type=str)

    def handle(self, *args, **options):
        leaderboard_id = options["leaderboard_id"]
        client = DarkerDBClient()
        data = client.leaderboard(leaderboard_id)
        LeaderboardEntry.objects.filter(leaderboard_id=leaderboard_id).delete()
        for row in data.get("body", []):
            LeaderboardEntry.objects.create(
                leaderboard_id=leaderboard_id,
                character=row.get("character"),
                character_class=row.get("class"),
                rank=row.get("rank"),
                score=row.get("score"),
                current_position=row.get("current_position"),
                previous_position=row.get("previous_position"),
            )
        self.stdout.write(self.style.SUCCESS(f"Leaderboard {leaderboard_id} synced"))


