import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from task.models import Task


@pytest.fixture(scope='module')
def user():
    return mixer.blend(User)


@pytest.fixture(scope='module')
def task():
    return mixer.blend(Task)


def test_task_model(user, task):
    assert isinstance(task.name, str)
    assert isinstance(task.description, str)
    assert isinstance(task.created_at, type(task.updated_at))
    assert isinstance(task.assigned_to, User)
    assert task.status in ['New', 'In Progress', 'Completed']
    assert isinstance(str(task), str)
    assert Task._meta.ordering == ['status']
