import pytest
import factory

from rest_framework.test import APIClient

from django.contrib.auth.models import User
from task import models as task_models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@progame.com")
    password = factory.PostGenerationMethodCall("set_password", "password")


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = task_models.Task

    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: f"Task {n}")
    description = factory.Faker("text")
    status = task_models.StatusEnum.NEW.value
    priority = task_models.PriorityEnum.MEDIUM.value


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client
