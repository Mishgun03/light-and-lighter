import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Item, Favorite, PriceSnapshot, LeaderboardEntry

# pytestmark используется для применения маркера ко всем тестам в модуле
# db - это фикстура pytest-django, которая предоставляет доступ к базе данных для каждого теста
pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    """Фикстура для создания экземпляра APIClient."""
    return APIClient()


@pytest.fixture
def test_user(django_user_model):
    """Фикстура для создания тестового пользователя."""
    return django_user_model.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def authenticated_client(api_client, test_user):
    """Фикстура для создания аутентифицированного клиента."""
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.fixture
def test_item():
    """Фикстура для создания тестового предмета."""
    return Item.objects.create(
        id="item123",
        name="Test Sword",
        rarity="Epic",
        type="Weapon",
    )


# --- Тесты ---

def test_register_user(api_client):
    """
    1. Тест регистрации нового пользователя.
    Проверяет, что новый пользователь может быть успешно создан, и что попытка
    создания пользователя с уже существующим именем вернет ошибку.
    """
    url = reverse("register")
    data = {"username": "newuser", "password": "newpassword123", "email": "newuser@example.com"}
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert User.objects.filter(username="newuser").exists()

    # Попытка зарегистрировать пользователя с тем же именем
    response_fail = api_client.post(url, data)
    assert response_fail.status_code == 400
    assert response_fail.json()["detail"] == "username already exists"


def test_obtain_jwt_token(api_client, test_user):
    """
    2. Тест получения JWT токена.
    Проверяет, что зарегистрированный пользователь может получить токен доступа
    и обновления при предоставлении правильных учетных данных.
    """
    url = reverse("token_obtain_pair")
    data = {"username": "testuser", "password": "testpassword"}
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@patch("market.views.external_get")
def test_list_items_and_proxy(mock_external_get, api_client):
    """
    3. Тест получения списка предметов.
    Проверяет, что конечная точка /api/items/ проксирует запрос к внешнему API,
    возвращает данные и синхронизирует их с локальной базой данных.
    """
    mock_external_get.return_value = {
        "body": [{
            "id": "mock_item_1",
            "name": "Mock Sword",
            "rarity": "Legendary",
            "type": "Weapon"
        }]
    }
    url = reverse("item-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.json()["body"]) == 1
    # Проверяем, что предмет был создан в локальной БД
    assert Item.objects.filter(id="mock_item_1").exists()


@patch("market.views.external_get")
def test_item_market_data(mock_external_get, api_client, test_item):
    """
    4. Тест получения рыночных данных для предмета.
    Проверяет, что конечная точка /api/items/{id}/market/ получает данные
    о ценах и создает PriceSnapshot в локальной базе данных.
    """
    mock_external_get.return_value = {
        "body": [{
            "id": 98765,
            "item_id": test_item.id,
            "price": 500,
            "created_at": "2025-01-01T12:00:00Z"
        }]
    }
    url = reverse("item-market", kwargs={"pk": test_item.id})
    response = api_client.get(url)
    assert response.status_code == 200
    # Проверяем, что был создан снимок цены
    assert PriceSnapshot.objects.filter(market_id=98765).exists()


def test_add_favorite_item(authenticated_client, test_item):
    """
    5. Тест добавления предмета в избранное.
    Проверяет, что аутентифицированный пользователь может добавить
    существующий предмет в свой список избранного.
    """
    url = reverse("favorite-list")
    data = {"item_id": test_item.id}
    response = authenticated_client.post(url, data)
    assert response.status_code == 201
    assert Favorite.objects.filter(user__username="testuser", item=test_item).exists()


def test_remove_favorite_item(authenticated_client, test_user, test_item):
    """
    6. Тест удаления предмета из избранного.
    Проверяет, что пользователь может удалить предмет из своего
    списка избранного через специальное действие 'remove'.
    """
    Favorite.objects.create(user=test_user, item=test_item)
    url = reverse("favorite-remove")
    data = {"item_id": test_item.id}
    response = authenticated_client.post(url, data)
    assert response.status_code == 200
    assert not Favorite.objects.filter(user=test_user, item=test_item).exists()


def test_get_favorites_list(authenticated_client, test_user, test_item):
    """
    7. Тест получения списка избранных предметов.
    Проверяет, что пользователь получает только свои избранные предметы.
    """
    Favorite.objects.create(user=test_user, item=test_item)
    url = reverse("favorite-list")
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["item"]["id"] == test_item.id


def test_dashboard_view(authenticated_client, test_user, test_item):
    """
    8. Тест получения данных для панели управления.
    Проверяет, что конечная точка /api/dashboard/ возвращает список
    избранного пользователя и информацию о популяции.
    """
    Favorite.objects.create(user=test_user, item=test_item)
    PriceSnapshot.objects.create(item=test_item, price=150, created_at="2025-01-01T10:00:00Z")
    url = reverse("dashboard")
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert "favorites" in response.data
    assert "population" in response.data
    assert len(response.data["favorites"]) == 1
    assert response.data["favorites"][0]["item"]["name"] == "Test Sword"
    assert response.data["favorites"][0]["latest_price"]["price"] == 150


@patch("market.views.external_get")
def test_leaderboard_view(mock_external_get, api_client):
    """
    9. Тест получения данных таблицы лидеров.
    Проверяет, что конечная точка /api/leaderboard/ получает данные,
    сохраняет их локально и возвращает клиенту.
    """
    mock_external_get.return_value = {
        "body": [{
            "character": "Player1",
            "class": "Fighter",
            "rank": "Grandmaster",
            "score": 9000,
            "current_position": 1,
        }]
    }
    url = reverse("leaderboard")
    response = api_client.get(url, {"id": "TEST_LEADERBOARD"})
    assert response.status_code == 200
    assert len(response.data["entries"]) == 1
    assert response.data["entries"][0]["character"] == "Player1"
    # Проверяем, что запись была создана в локальной БД
    assert LeaderboardEntry.objects.filter(leaderboard_id="TEST_LEADERBOARD").exists()


@patch("market.views.external_get")
def test_price_history_fallback(mock_external_get, api_client, test_item):
    """
    10. Тест получения истории цен с резервным вариантом.
    Проверяет, что если внешний API для аналитики недоступен, конечная точка
    возвращает данные из локальных снимков цен (PriceSnapshot).
    """
    # Имитируем сбой внешнего API
    mock_external_get.side_effect = Exception("API is down")

    # Создаем локальные данные
    PriceSnapshot.objects.create(item=test_item, price=100, created_at="2025-01-01T00:00:00Z")
    PriceSnapshot.objects.create(item=test_item, price=120, created_at="2025-01-01T01:00:00Z")

    url = reverse("price_history", kwargs={"item_id": test_item.id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["price"] == 100  # Данные отсортированы и перевернуты
    assert response.data[1]["price"] == 120