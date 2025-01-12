import pytest
from django.urls import reverse
from rest_framework import status

from tests.fixtures import *

from task import models as task_models


@pytest.mark.django_db
def test_task_list(auth_client, user):
    TaskFactory.create_batch(3, user=user)
    other_user = UserFactory()
    TaskFactory.create_batch(2, user=other_user)

    url = reverse("task-create-list")

    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 3


@pytest.mark.django_db
def test_task_create(auth_client, user):
    url = reverse("task-create-list")
    data = {
        "title": "New Task",
        "description": "Task description",
        "priority": task_models.PriorityEnum.HIGH.value,
        "status": task_models.StatusEnum.IN_PROGRESS.value,
    }

    response = auth_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    task = task_models.Task.objects.get(user=user, title="New Task")
    assert task.description == "Task description"


@pytest.mark.django_db
def test_task_retrieve(auth_client, user):
    task = TaskFactory(user=user)
    url = reverse("task-crud", kwargs={"pk": task.pk})

    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == task.id


@pytest.mark.django_db
def test_task_update(auth_client, user):
    task = TaskFactory(user=user)
    url = reverse("task-crud", kwargs={"pk": task.pk})
    data = {"title": "Updated Task"}

    response = auth_client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.title == "Updated Task"


@pytest.mark.django_db
def test_task_delete(auth_client, user):
    task = TaskFactory(user=user)
    url = reverse("task-crud", kwargs={"pk": task.pk})

    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not task_models.Task.objects.filter(pk=task.pk).exists()


@pytest.mark.django_db
def test_task_create_with_blank_description(auth_client, user):
    url = reverse("task-create-list")

    data = {
        "title": "Task with empty description",
        "description": "",  # blank
        "priority": "medium",
        "status": "new",
    }
    response = auth_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED

    task = task_models.Task.objects.get(id=response.data["id"])
    assert task.description is None

    data = {
        "title": "Task with spaces in description",
        "description": "   ",  # blank with spaces
        "priority": "medium",
        "status": "new",
    }
    response = auth_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED

    task = task_models.Task.objects.get(id=response.data["id"])
    assert task.description is None
