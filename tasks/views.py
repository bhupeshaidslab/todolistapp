from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Case, F, IntegerField, Q, When
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskForm
from .models import DEFAULT_CATEGORIES, DEFAULT_LABELS, Category, Label, Task


def seed_default_categories(user):
    for name, color in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(user=user, name=name, defaults={"color": color})


def seed_default_labels(user):
    for name, color in DEFAULT_LABELS:
        Label.objects.get_or_create(user=user, name=name, defaults={"color": color})


def seed_user_defaults(user):
    seed_default_categories(user)
    seed_default_labels(user)


def register_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")

    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        seed_user_defaults(user)
        login(request, user)
        messages.success(request, "Account created.")
        return redirect("task_list")

    return render(request, "registration/register.html", {"form": form})


def _task_queryset(user, request):
    qs = Task.objects.filter(user=user).select_related("category").prefetch_related("labels")

    status = request.GET.get("status", "all")
    if status in ("active", "pending"):
        qs = qs.filter(completed=False)
    elif status == "done":
        qs = qs.filter(completed=True)

    priority = request.GET.get("priority")
    if priority in Task.Priority.values:
        qs = qs.filter(priority=priority)

    category_id = request.GET.get("category")
    if category_id and category_id.isdigit():
        qs = qs.filter(category_id=int(category_id))

    label_id = request.GET.get("label")
    if label_id and label_id.isdigit():
        qs = qs.filter(labels__id=int(label_id))

    query = request.GET.get("q", "").strip()
    if query:
        qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query))

    sort = request.GET.get("sort", "newest")
    if sort == "oldest":
        qs = qs.order_by("completed", "created_at")
    elif sort == "due":
        qs = qs.order_by("completed", F("due_date").asc(nulls_last=True), "-created_at")
    elif sort == "priority":
        qs = qs.annotate(
            priority_rank=Case(
                When(priority=Task.Priority.HIGH, then=0),
                When(priority=Task.Priority.MEDIUM, then=1),
                When(priority=Task.Priority.LOW, then=2),
                default=1,
                output_field=IntegerField(),
            )
        ).order_by("completed", "priority_rank", "-created_at")
    else:
        qs = qs.order_by("completed", "-created_at")

    return qs.distinct()


def build_task_groups(tasks, show_completed):
    overdue, due_today, pending, completed = [], [], [], []
    for task in tasks:
        if task.completed:
            completed.append(task)
        elif task.is_overdue:
            overdue.append(task)
        elif task.is_due_today:
            due_today.append(task)
        else:
            pending.append(task)

    groups = []
    if overdue:
        groups.append(("Overdue", overdue))
    if due_today:
        groups.append(("Due today", due_today))
    if pending:
        groups.append(("Pending", pending))
    if show_completed and completed:
        groups.append(("Completed", completed))
    return groups


def _filter_context(request):
    status = request.GET.get("status", "all")
    if status == "active":
        status = "pending"
    return {
        "q": request.GET.get("q", ""),
        "status": status,
        "priority": request.GET.get("priority", ""),
        "category": request.GET.get("category", ""),
        "label": request.GET.get("label", ""),
        "sort": request.GET.get("sort", "newest"),
    }


def _filter_query(filters):
    return (
        f"?status={filters['status']}&q={filters['q']}&priority={filters['priority']}"
        f"&category={filters['category']}&label={filters['label']}&sort={filters['sort']}"
    )


@login_required
def task_list(request):
    if not request.user.categories.exists() or not request.user.labels.exists():
        seed_user_defaults(request.user)

    filters = _filter_context(request)
    tasks = list(_task_queryset(request.user, request))
    all_tasks = Task.objects.filter(user=request.user)
    pending_count = all_tasks.filter(completed=False).count()
    completed_count = all_tasks.filter(completed=True).count()
    overdue_count = sum(1 for t in all_tasks.filter(completed=False) if t.is_overdue)

    show_completed = filters["status"] in ("all", "done")
    task_groups = build_task_groups(tasks, show_completed=show_completed)
    if not task_groups and tasks:
        task_groups = [("Tasks", tasks)]

    return render(request, "tasks/task_list.html", {
        "task_groups": task_groups,
        "tasks": tasks,
        "categories": request.user.categories.all(),
        "labels": request.user.labels.all(),
        "priorities": Task.Priority.choices,
        "pending_count": pending_count,
        "completed_count": completed_count,
        "overdue_count": overdue_count,
        "filters": filters,
        "filter_query": _filter_query(filters),
    })


@login_required
def task_add(request):
    if request.method == "POST":
        form = TaskForm(request.user, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            form.save_m2m()
            messages.success(request, "Task added.")
    return redirect("task_list")


@login_required
def task_manage(request, pk):
    task = get_object_or_404(
        Task.objects.select_related("category").prefetch_related("labels"),
        pk=pk,
        user=request.user,
    )
    return render(request, "tasks/task_manage.html", {
        "task": task,
        "priorities": Task.Priority.choices,
    })


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    form = TaskForm(request.user, request.POST or None, instance=task, show_status=True)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Task updated.")
        return redirect("task_manage", pk=task.pk)

    return render(request, "tasks/task_edit.html", {"form": form, "task": task})


@login_required
def task_toggle(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.completed = not task.completed
        task.save()
    return redirect(request.META.get("HTTP_REFERER", "task_list"))


@login_required
def task_mark_pending(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.completed = False
        task.save()
        messages.success(request, "Marked as pending.")
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)
    return redirect("task_manage", pk=pk)


@login_required
def task_delete(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.delete()
        messages.success(request, "Task deleted.")
    return redirect(request.META.get("HTTP_REFERER", "task_list"))


@login_required
def task_clear_completed(request):
    if request.method == "POST":
        deleted, _ = Task.objects.filter(user=request.user, completed=True).delete()
        if deleted:
            messages.success(request, f"Cleared {deleted} completed task(s).")
        else:
            messages.info(request, "No completed tasks to clear.")
    return redirect("task_list")
