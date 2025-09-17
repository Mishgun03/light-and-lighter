from datetime import datetime
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.db.models import Min, Max
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item, PriceSnapshot, Favorite, LeaderboardEntry, PopulationSnapshot
from .serializers import (
    ItemSerializer,
    PriceSnapshotSerializer,
    FavoriteSerializer,
    LeaderboardEntrySerializer,
    PopulationSnapshotSerializer,
)


def external_get(path: str, params: dict | None = None):
    params = params or {}
    if settings.DARKERDB_API_KEY:
        params.setdefault("key", settings.DARKERDB_API_KEY)
    url = f"{settings.DARKERDB_API_BASE}{path}"
    res = requests.get(url, params=params, timeout=20)
    res.raise_for_status()
    return res.json()


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all().order_by("name")
    serializer_class = ItemSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        # Proxy to external API for search; optionally sync minimal fields locally
        query_params = {k: v for k, v in request.query_params.items()}
        data = external_get("/v1/items", params=query_params)
        body = data.get("body", [])
        # Upsert items asynchronously in a real app; here do minimal sync
        for item in body:
            Item.objects.update_or_create(
                id=item["id"],
                defaults={
                    "archetype": item.get("archetype", ""),
                    "name": item.get("name", ""),
                    "rarity": item.get("rarity", ""),
                    "type": item.get("type", ""),
                    "slot_type": item.get("slot_type"),
                    "armor_type": item.get("armor_type"),
                    "gear_score": item.get("gear_score"),
                    "vendor_price": item.get("vendor_price"),
                    "data": item,
                },
            )
        return Response(data)

    @action(detail=True, methods=["get"], permission_classes=[permissions.AllowAny])
    def market(self, request, pk=None):
        params = {"item_id": pk, "limit": request.query_params.get("limit", 25), "condense": "true"}
        data = external_get("/v1/market", params=params)
        # Store price snapshots
        for row in data.get("body", []):
            item = Item.objects.filter(id=row.get("item_id")).first()
            if not item:
                continue
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
        return Response(data)

    @action(detail=True, methods=["get"], permission_classes=[permissions.AllowAny])
    def icon(self, request, pk=None):
        # Cache item icon under media/icons/{id}.png
        filename = f"icons/{pk}.png"
        if default_storage.exists(filename):
            url = default_storage.url(filename)
            return Response({"icon": url})
        # Fetch from external API
        params = {"key": settings.DARKERDB_API_KEY} if settings.DARKERDB_API_KEY else {}
        url = f"{settings.DARKERDB_API_BASE}/v1/items/{pk}/icon"
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        default_storage.save(filename, ContentFile(r.content))
        return Response({"icon": default_storage.url(filename)})


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related("item")

    def perform_create(self, serializer):
        item_id = self.request.data.get("item_id")
        item = Item.objects.filter(pk=item_id).first()
        if not item:
            # Try to fetch from external API and upsert
            try:
                data = external_get(f"/v1/items/{item_id}", params={"condense": "true"})
                body = data.get("body", {})
                if body:
                    item, _ = Item.objects.update_or_create(
                        id=body.get("id", item_id),
                        defaults={
                            "archetype": body.get("archetype", ""),
                            "name": body.get("name", item_id),
                            "rarity": body.get("rarity", ""),
                            "type": body.get("type", ""),
                            "slot_type": body.get("slot_type"),
                            "armor_type": body.get("armor_type"),
                            "gear_score": body.get("gear_score"),
                            "vendor_price": body.get("vendor_price"),
                            "data": body,
                        },
                    )
            except Exception:
                pass
        if not item:
            raise ValueError("Unknown item_id")
        serializer.save(user=self.request.user, item=item)

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def remove(self, request):
        item_id = request.data.get("item_id")
        Favorite.objects.filter(user=request.user, item_id=item_id).delete()
        return Response({"ok": True})

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def charts(self, request):
        # Aggregate min/max per day for user's favorites
        item_ids = self.get_queryset().values_list("item_id", flat=True)
        snapshots = (
            PriceSnapshot.objects.filter(item_id__in=item_ids)
            .values("item_id")
            .annotate(min_price=Min("price"), max_price=Max("price"))
        )
        return Response(list(snapshots))


class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user).select_related("item")
        favs = [
            {
                "id": f.id,
                "created_at": f.created_at,
                "item": ItemSerializer(f.item).data,
                "latest_price": PriceSnapshot.objects.filter(item=f.item).order_by("-created_at").values("price").first() or {},
            }
            for f in favorites
        ]
        population = PopulationSnapshot.objects.order_by("-timestamp").first()
        return Response({
            "favorites": favs,
            "population": PopulationSnapshotSerializer(population).data if population else None,
        })


class LeaderboardView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        leaderboard_id = request.query_params.get("id", "EA6_SHR")
        data = external_get(f"/v1/leaderboards/{leaderboard_id}")
        # Optionally refresh cache
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
        return Response({
            "id": leaderboard_id,
            "entries": LeaderboardEntrySerializer(
                LeaderboardEntry.objects.filter(leaderboard_id=leaderboard_id).order_by("current_position"), many=True
            ).data,
        })


class PopulationView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        data = external_get("/v1/population")
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
        return Response(data)


class AuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Provide JWT via SimpleJWT token pair endpoint redirect
        # Frontend should use /api/token/ and /api/token/refresh/ normally
        return Response({"message": "Use /api/token/ to obtain JWT."})


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from django.contrib.auth.models import User
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        if not username or not password:
            return Response({"detail": "username and password required"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"detail": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"id": user.id, "username": user.username, "email": user.email})


class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from django.contrib.auth.models import User
        from django.core.mail import send_mail
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"ok": True})
        # Simple tokenless flow for demo (console email)
        send_mail(
            subject="Password reset instructions",
            message="Contact admin to reset password in this demo.",
            from_email=None,
            recipient_list=[email],
            fail_silently=True,
        )
        return Response({"ok": True})


class PriceHistoryView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, item_id: str):
        # Prefer external analytics for rich history; fallback to local snapshots
        interval = request.query_params.get("interval", "1h")
        try:
            data = external_get(f"/v1/market/analytics/{item_id}/prices/history", params={"interval": interval})
            body = data.get("body", [])
            transformed = [
                {
                    "created_at": row.get("timestamp"),
                    "avg": row.get("avg"),
                    "min": row.get("min"),
                    "max": row.get("max"),
                    "volume": row.get("volume"),
                }
                for row in body
            ]
            return Response(transformed)
        except Exception:
            # Fallback to local snapshots if external analytics unavailable
            limit = int(request.query_params.get("limit", 100))
            qs = (
                PriceSnapshot.objects.filter(item_id=item_id)
                .order_by("-created_at")
                .values("created_at", "price")[:limit]
            )
            return Response(list(reversed(list(qs))))


