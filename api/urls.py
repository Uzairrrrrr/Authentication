from django.urls import path
from django.contrib import admin
from .views import APIOverview, TaskListView, TaskDetailUpdateDeleteView
from .views import UserRegistrationView
from .views import UserSignInView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', APIOverview.as_view(), name='api-overview'),
    path('task-list/', TaskListView.as_view(), name='task-list'),
    path('task/<int:task_id>/', TaskDetailUpdateDeleteView.as_view(), name='task-detail'),
    path('task/<int:task_id>/delete/', TaskDetailUpdateDeleteView.as_view(), name='task-delete'),
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('signin/', UserSignInView.as_view(), name='signin'),
]
