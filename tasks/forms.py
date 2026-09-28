from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "priority", "due_date", "category"]
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "What needs to be done?",
                "autocomplete": "off",
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Optional description",
                "rows": 3,
            }),
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "priority": forms.Select(),
            "category": forms.Select(),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = user.categories.all()
        self.fields["category"].required = False
        self.fields["due_date"].required = False
