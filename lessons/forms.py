from django import forms
from homework.models import AssignmentSubmission


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ["github_link", "description"]
        widgets = {
            "github_link": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://github.com/username/repository"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Vazifa haqida qisqacha izoh yozing yoki tushunmagan biror bir muammooingiz"
            }),
        }