from django import forms
from . import models

class UserForm(forms.Form):
    username = forms.CharField(label='学号/工号', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密码', max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class InputForm(forms.ModelForm):
    class Meta:
        model = models.Event
        exclude = ('id',)

