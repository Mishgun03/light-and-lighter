import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    """
    Фикстура для создания экземпляра APIClient из DRF.
    """
    return APIClient()