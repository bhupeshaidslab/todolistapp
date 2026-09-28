from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#6b7280")

    class Meta:
        ordering = ["name"]
        unique_together = [["user", "name"]]

    def __str__(self):
        return self.name


class Label(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="labels")
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default="#8e8e93")

    class Meta:
        ordering = ["name"]
        unique_together = [["user", "name"]]

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )
    labels = models.ManyToManyField(Label, blank=True, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    due_date = models.DateField(null=True, blank=True, verbose_name="Deadline")
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["completed", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_pending(self):
        return not self.completed

    @property
    def is_overdue(self):
        if self.completed or not self.due_date:
            return False
        return self.due_date < timezone.localdate()

    @property
    def is_due_today(self):
        if self.completed or not self.due_date:
            return False
        return self.due_date == timezone.localdate()

    @property
    def deadline_label(self):
        if not self.due_date:
            return "No deadline"
        if self.completed:
            return f"Deadline was {self.due_date.strftime('%b %d, %Y')}"
        if self.is_overdue:
            return f"Overdue · {self.due_date.strftime('%b %d, %Y')}"
        if self.is_due_today:
            return "Due today"
        return f"Due {self.due_date.strftime('%b %d, %Y')}"


DEFAULT_CATEGORIES = (
    ("Work", "#2563eb"),
    ("Personal", "#7c3aed"),
    ("Errands", "#059669"),
)

DEFAULT_LABELS = (
    ("Urgent", "#ff3b30"),
    ("Focus", "#007aff"),
    ("Waiting", "#ff9500"),
)
