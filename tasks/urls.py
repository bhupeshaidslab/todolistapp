from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("task/add/", views.task_add, name="task_add"),
    path("task/clear-completed/", views.task_clear_completed, name="task_clear_completed"),
    path("task/<int:pk>/", views.task_manage, name="task_manage"),
    path("task/<int:pk>/edit/", views.task_edit, name="task_edit"),
    path("task/<int:pk>/pending/", views.task_mark_pending, name="task_mark_pending"),
    path("task/<int:pk>/toggle/", views.task_toggle, name="task_toggle"),
    path("task/<int:pk>/delete/", views.task_delete, name="task_delete"),
]
