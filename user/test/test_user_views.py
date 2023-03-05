

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client, RequestFactory
from task.models import Task
from user.views import RegisterView, CustomLoginView, ProfileView


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.mark.django_db
def test_register_view(client):
    response = client.get(reverse('register'))
    assert response.status_code == 200

    data = {
        'username': 'johndoe',
        'password1': 'mysecretpassword',
        'password2': 'mysecretpassword',
    }
    response = client.post(reverse('register'), data)
    assert response.status_code == 302
    assert response.url == reverse('tasks')

    user = User.objects.get(username='johndoe')
    assert user is not None


@pytest.mark.django_db
def test_custom_login_view(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200

    user = User.objects.create_user(username='johndoe', password='mysecretpassword')
    data = {
        'username': 'johndoe',
        'password': 'mysecretpassword',
    }
    response = client.post(reverse('login'), data)
    assert response.status_code == 302
    assert response.url == reverse('tasks')


@pytest.mark.django_db
def test_profile_view(factory):
    user = User.objects.create_user(username='johndoe', password='mysecretpassword')
    request = factory.get(reverse('profile'))
    request.user = user

    task1 = Task.objects.create(title='Task 1', description='Description', assigned_to=user, status='New')
    task2 = Task.objects.create(title='Task 2', description='Description', assigned_to=user, status='In Progress')
    task3 = Task.objects.create(title='Task 3', description='Description', assigned_to=user, status='Completed')

    response = ProfileView.as_view()(request)
    assert response.status_code == 200
    assert response.context_data['new_count'] == 1
    assert response.context_data['in_progress_count'] == 1
    assert response.context_data['completed_count'] == 1
    assert response.context_data['completed_percentage'] == 33.33
