from attr import attributes
from rest_framework import serializers
from .models import Item, Favorite, PriceHistory#, Listing


class ItemSerializer(serializers.ModelSerializer):
    item = serializers.CharField(source='name')
    class Meta:
        model = Item
        fields = ['item_id', 'item', 'archetype']


class MarketItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    price = serializers.IntegerField()
    price_per_unit = serializers.IntegerField()
    quantity = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    expires_at = serializers.DateTimeField()
    seller = serializers.CharField(allow_null=True)

    def to_representation(self, instance):
        item_data = {
            "item_id": instance.get("item_id"),
            "item": instance.get("item"),
            "archetype": instance.get("archetype"),
            "rarity": instance.get("rarity"),
        }

        attributes_data = {}
        for key, value in instance.items():
            if key.startswith("primary") or key.startswith("secondary_"):
                attributes_data[key] = value

        representation = {
            "id": instance.get("id"),
            "price": instance.get("price"),
            "price_per_unit": instance.get("price_per_unit"),
            "quantity": instance.get("quantity"),
            "created_at": instance.get("created_at"),
            "expires_at": instance.get("expires_at"),
            "seller": instance.get("seller"),

            "item": item_data,
            "attributes": attributes_data,
        }

        return representation



class ListingSerializer(serializers.Serializer):
    count = serializers.IntegerField(source='pagination.count')
    limit = serializers.IntegerField(source='pagination.limit')
    cursor = serializers.IntegerField(source='pagination.cursor', allow_null=True)
    page = serializers.IntegerField(source='pagination.page', allow_null=True)
    previous = serializers.CharField(source='pagination.prev', allow_null=True)

    results = MarketItemSerializer(many=True, source='body')

class ListingQuerySerializer(serializers.Serializer):
    item_name = serializers.CharField(required=False, help_text='Поиск по названию предмета')
    rarity = serializers.CharField(required=False, default=None, help_text='Фильтр по редкости')
    sort = serializers.CharField(required=False, default='date_asc', help_text='Сортировка результатов')
    cursor = serializers.CharField(required=False, default=None, help_text='Курсор для пагинации')
    limit = serializers.IntegerField(required=False, default=25, help_text='Количество результатов на странице')
    page = serializers.IntegerField(required=False, default=1, help_text='Номер страницы')


class FavoriteReadSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    class Meta:
        model = Favorite
        fields = ['item']


class FavoriteWriteSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(),
        source='item',
        write_only=True
    )

    class Meta:
        model = Favorite
        fields = ['item_id']


class PriceHistorySerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    avg_price = serializers.FloatField(source='avg')
    min_price = serializers.IntegerField(source='min')
    max_price = serializers.IntegerField(source='max')
    volume = serializers.IntegerField()
