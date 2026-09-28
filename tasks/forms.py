from django import forms

from .models import Label, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "priority",
            "due_date",
            "category",
            "labels",
            "completed",
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Task title",
                "autocomplete": "off",
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Notes (optional)",
                "rows": 3,
            }),
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "priority": forms.Select(),
            "category": forms.Select(),
            "labels": forms.CheckboxSelectMultiple(),
            "completed": forms.CheckboxInput(),
        }
        labels = {
            "due_date": "Deadline",
            "category": "List",
            "completed": "Mark completed",
        }

    def __init__(self, user, *args, **kwargs):
        show_status = kwargs.pop("show_status", False)
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = user.categories.all()
        self.fields["category"].required = False
        self.fields["due_date"].required = False
        self.fields["labels"].queryset = user.labels.all()
        self.fields["labels"].required = False
        if not show_status:
            self.fields.pop("completed")
