import httpx
import hashlib
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from asgiref.sync import async_to_sync

from .models import Favorite
from .serializers import FavoriteReadSerializer, FavoriteWriteSerializer, PriceHistorySerializer, ListingSerializer, \
    ListingQuerySerializer

from django.core.cache import cache


class ListingViewSet(APIView):
    CACHE_TIMEOUT = 60 * 5

    @extend_schema(
        parameters=[ListingQuerySerializer],
        responses={200: ListingSerializer},
        # ...
    )
    def get(self, request, *args, **kwargs):
        query_serializer = ListingQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        validated_data = query_serializer.validated_data

        user_sort_preference = validated_data.get('sort')

        item_name = validated_data.get('item_name')
        validated_data.pop('item_name', None)
        validated_data["item"] = item_name

        if item_name:
            item_name_hash = hashlib.md5(item_name.encode('utf-8')).hexdigest()
        else:
            item_name_hash = 'all'


        cache_key_parts = [
            'listing',
            item_name_hash,
            validated_data.get('rarity') or 'all',
            user_sort_preference,
            validated_data.get('cursor'),
            validated_data.get('limit'),
            validated_data.get('page'),
        ]
        cache_key = "_".join(map(str, filter(None, cache_key_parts)))

        cached_data = cache.get(cache_key)
        if cached_data:
            print(f"CACHE HIT: {cache_key}")
            return Response(cached_data, status=status.HTTP_200_OK)

        print(f"CACHE MISS: {cache_key}")

        api_params = {
            key: value
            for key, value in validated_data.items()
            if value is not None
        }

        api_params.pop('sort', None)

        if user_sort_preference == 'date_asc':
            api_params['order'] = 'asc'
        elif user_sort_preference == 'date_desc':
            api_params['order'] = 'desc'
        elif user_sort_preference in ['price_asc', 'price_desc']:
            api_params['order'] = 'desc'

        # print(api_params)

        external_api_url = "https://api.darkerdb.com/v1/market"
        try:
            with httpx.Client() as client:
                response = client.get(external_api_url, params=api_params)
                response.raise_for_status()
                external_data = response.json()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        results_list = external_data.get('body', [])

        if user_sort_preference in ['price_asc', 'price_desc']:
            is_reverse = (user_sort_preference == 'price_desc')
            results_list.sort(key=lambda item: item.get('price', 0), reverse=is_reverse)
            external_data['body'] = results_list

        serializer = ListingSerializer(
            instance=external_data,
            context={'request': request},
        )
        transformed_data = serializer.data

        cache.set(cache_key, transformed_data, timeout=self.CACHE_TIMEOUT)

        return Response(transformed_data, status=status.HTTP_200_OK)


class PriceHistoryListView(APIView):
    CACHE_TIMEOUT = 60 * 15

    serializer_class = PriceHistorySerializer

    # @extend_schema()
    def get(self, request, item_id: str):
        return async_to_sync(self.handle_request)(request, item_id)

    async def handle_request(self, request, item_id: str):
        from_date = request.query_params.get('from', '7d')
        to_date = request.query_params.get('to', 'now')
        interval = request.query_params.get('interval', '15m')

        cache_key = f"item_history:{item_id}:{from_date}:{to_date}:{interval}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        external_api_url = f"https://api.darkerdb.com/v1/market/analytics/{item_id}/prices/history"
        params = {
            'from': from_date,
            'to': to_date,
            'interval': interval,
        }

        try:
            async with httpx.AsyncClient() as client:
                api_response = await client.get(external_api_url, params=params, timeout=10.0)
                print(api_response)
                api_response.raise_for_status()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return Response(
                    {"detail": f"Item with id '{item_id}' not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(
                {"detail": f"External API error: {e.response.status_code}"},
                status=status.HTTP_502_BAD_GATEWAY
            )
        except httpx.RequestError as e:
            return Response(
                {"detail": f"Could not connect to external API: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY
            )

        external_data = api_response.json()
        history_list = external_data.get('body')

        if history_list is None:
            return Response(
                {"detail": "Invalid response format from external API."},
                status=status.HTTP_502_BAD_GATEWAY
            )

        serializer = PriceHistorySerializer(instance=history_list, many=True)

        final_data = serializer.data

        cache.set(cache_key, final_data, timeout=self.CACHE_TIMEOUT)

        return Response(final_data, status=status.HTTP_200_OK)


class FavoriteViewSet(mixins.CreateModelMixin,  # Обрабатывает POST
                      mixins.ListModelMixin,  # Обрабатывает GET
                      mixins.DestroyModelMixin,  # Обрабатывает DELETE
                      viewsets.GenericViewSet):

    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'item__item_id'

    lookup_url_kwarg = 'item_id'

    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user).select_related('item')

    def get_serializer_class(self):
        if self.action == 'create':
            return FavoriteWriteSerializer
        return FavoriteReadSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
