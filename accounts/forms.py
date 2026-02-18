from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=13, label="AUID")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
