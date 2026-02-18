from django import forms
from .models import Feedback

class LoginForm(forms.Form):
    username = forms.CharField(max_length=13, label="AUID")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")




class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("feedback",)
        widgets = {
            "feedback": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Fikringizni yozing... (taklif, muammo, g‘oya)",
            })
        }
