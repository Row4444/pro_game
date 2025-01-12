from django.urls import path

from task import views

urlpatterns = [
    path("", views.TaskListCreateView.as_view(), name="task-create-list"),
    path("<int:pk>", views.TaskGetUpdateDeleteView.as_view(), name="task-crud"),
]
