from django.urls import reverse
from rest_framework.test import APIClient
import pytest

from stocks.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        email='testuser@example.com',
        password='testpassword',
    )

def test_login(api_client, user):
    url = reverse('login')
    data = {'email': 'amin.owais22@gmail.com', 'password': 'admin123'}
    response = api_client.post(url, data=data)
    assert response.status_code == 200
    assert 'token' in response.data
    assert response.data['token'] == user.get_access_token()

def test_login_with_invalid_data(api_client):
    url = reverse('login')
    data = {'email': '', 'password': ''}
    response = api_client.post(url, data=data)
    assert response.status_code == 401
    assert response.data == {'email': ['This field may not be blank.'], 'password': ['This field may not be blank.']}

def test_login_with_incorrect_credentials(api_client):
    url = reverse('login')
    data = {'email': 'testuser@example.com', 'password': 'wrongpassword'}
    response = api_client.post(url, data=data)
    assert response.status_code == 401
    assert response.data == {'detail': 'Incorrect email or password.'}
