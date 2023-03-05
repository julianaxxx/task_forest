
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from django.test import RequestFactory
from task.models import Task
from task.views import TaskList, TaskCreate, TaskUpdate, TaskDelete, TaskDetail


@pytest.fixture(scope='module')
def task():
    return mixer.blend(Task)


@pytest.fixture(scope='module')
def user():
    return mixer.blend(User)


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


@pytest.mark.django_db
def test_task_list_view(factory, user):
    url = reverse('tasks')
    request = factory.get(url)
    request.user = user

    response = TaskList.as_view()(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_task_detail_view(factory, user, task):
    url = reverse('task', kwargs={'pk': task.pk})
    request = factory.get(url)
    request.user = user

    response = TaskDetail.as_view()(request, pk=task.pk)

    assert response.status_code == 200


@pytest.mark.django_db
def test_task_create_view(factory, user):
    url = reverse('task-create')
    request = factory.get(url)
    request.user = user

    response = TaskCreate.as_view()(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_task_update_view(factory, user, task):
    url = reverse('task-update', kwargs={'pk': task.pk})
    request = factory.get(url)
    request.user = user

    response = TaskUpdate.as_view()(request, pk=task.pk)

    assert response.status_code == 200


@pytest.mark.django_db
def test_task_delete_view(factory, user, task):
    url = reverse('task-delete', kwargs={'pk': task.pk})
    request = factory.get(url)
    request.user = user

    response = TaskDelete.as_view()(request, pk=task.pk)

    assert response.status_code == 200
