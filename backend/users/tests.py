import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from mixer.backend.django import mixer


@pytest.mark.django_db
def test_user_registration_success(api_client):
    """
    Тест успешной регистрации нового пользователя.
    """
    url = reverse('auth_register')
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "StrongPassword123"
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201
    assert User.objects.filter(username="testuser").exists()


@pytest.mark.django_db
def test_user_registration_fail_existing_user(api_client):
    """
    Тест провальной регистрации (пользователь уже существует).
    """
    # Создаем пользователя заранее
    mixer.blend(User, username="testuser", email="test@example.com")

    url = reverse('auth_register')
    data = {
        "username": "testuser",
        "email": "another@example.com",
        "password": "StrongPassword123"
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_user_login_success(api_client):
    password = "StrongPassword123"
    test_username = "testuser"
    # Создаем пользователя с email, по которому будем логиниться
    user = mixer.blend(User, username=test_username, email="login@example.com")
    user.set_password(password)
    user.save()

    url = reverse('token_obtain_pair')
    data = {
        "username": test_username,  # Используем email для входа
        "password": password
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == 200, response.data # Добавим вывод ошибки, если тест упадет
    assert 'access' in response.data