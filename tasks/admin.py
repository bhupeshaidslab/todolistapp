from django.contrib import admin

from .models import Category, Label, Task


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "color")
    list_filter = ("user",)
    search_fields = ("name", "user__username")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "color")
    list_filter = ("user",)
    search_fields = ("name", "user__username")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "priority", "due_date", "completed", "created_at")
    list_filter = ("completed", "priority", "category")
    search_fields = ("title", "user__username")
    filter_horizontal = ("labels",)
