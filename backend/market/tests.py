import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from market.models import Item, Favorite
from unittest.mock import MagicMock, patch


@pytest.mark.django_db
class TestFavoriteViewSet:
    def test_list_favorites_unauthenticated(self, api_client):
        """Неаутентифицированный пользователь не может видеть избранное."""
        url = reverse('favorite-list')
        response = api_client.get(url)
        assert response.status_code == 401

    def test_list_favorites_authenticated(self, api_client):
        """Аутентифицированный пользователь видит свое избранное."""
        user = mixer.blend(User)
        item1 = mixer.blend(Item)
        mixer.blend(Favorite, user=user, item=item1)

        api_client.force_authenticate(user=user)
        url = reverse('favorite-list')
        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['item']['item_id'] == item1.item_id

    def test_create_favorite(self, api_client):
        """Пользователь может добавить предмет в избранное."""
        user = mixer.blend(User)
        item = mixer.blend(Item)

        api_client.force_authenticate(user=user)
        url = reverse('favorite-list')
        data = {'item_id': item.item_id}
        response = api_client.post(url, data, format='json')

        assert response.status_code == 201
        assert Favorite.objects.filter(user=user, item=item).exists()

    def test_delete_favorite(self, api_client):
        """Пользователь может удалить предмет из избранного."""
        user = mixer.blend(User)
        item = mixer.blend(Item)
        mixer.blend(Favorite, user=user, item=item)

        api_client.force_authenticate(user=user)
        # URL для удаления конкретного элемента: favorite-detail
        url = reverse('favorite-detail', kwargs={'item_id': item.item_id})
        response = api_client.delete(url)

        assert response.status_code == 204
        assert not Favorite.objects.filter(user=user, item=item).exists()

# Тесты с мокированием API

@pytest.mark.django_db
def test_get_listings_success(api_client, mocker):
    """
    Тест успешного получения списка лотов с мокированием внешнего API.
    """
    # 1. Готовим фейковый ответ от внешнего API
    fake_api_response = {
        "pagination": {"count": 1, "limit": 25, "cursor": None, "page": 1, "prev": None},
        "body": [
            {
                "id": 12345, "price": 100, "price_per_unit": 100, "quantity": 1,
                "created_at": "2023-10-27T10:00:00Z", "expires_at": "2023-10-28T10:00:00Z",
                "seller": "TestSeller", "item_id": "some_item_id", "item": "Test Item",
                "archetype": "Fighter", "rarity": "Uncommon"
            }
        ]
    }

    # 2. "Патчим" (заменяем) метод httpx.Client.get
    # Он будет возвращать наш фейковый ответ вместо реального запроса
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = fake_api_response

    # Мы используем patch с with, чтобы замена работала только внутри этого блока
    with patch('httpx.Client.get', return_value=mock_response) as mock_get:
        url = reverse('listing')
        response = api_client.get(url, {'item_name': 'Test Item'})

        # 3. Проверяем результат
        assert response.status_code == 200
        assert response.data['count'] == 1
        assert response.data['results'][0]['item']['item'] == 'Test Item'

        # Убедимся, что наш mock был вызван с правильными параметрами
        mock_get.assert_called_once()


@pytest.mark.django_db
def test_get_listings_api_error(api_client, mocker):
    """
    Тест поведения при ошибке внешнего API.
    """
    # Патчим httpx.Client.get, чтобы он вызывал исключение
    with patch('httpx.Client.get', side_effect=Exception("API is down")) as mock_get:
        url = reverse('listing')
        response = api_client.get(url)

        assert response.status_code == 503  # SERVICE_UNAVAILABLE
        assert "error" in response.data


@pytest.mark.django_db
def test_get_price_history_success(api_client, mocker):
    item = mixer.blend(Item, item_id="test_sword_id")

    fake_history_response = {
        "body": [
            {"timestamp": "2023-10-27T10:00:00Z", "avg": 150.5, "min": 140, "max": 160, "volume": 50}
        ]
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = fake_history_response
    mock_response.raise_for_status = MagicMock()

    mocker.patch(
        'httpx.Client.get',
        return_value=mock_response
    )

    url = reverse('price-history', kwargs={'item_id': item.item_id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['avg_price'] == 150.5
