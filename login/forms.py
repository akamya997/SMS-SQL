from django import forms
from . import models
from django.db.models import Q
from django.core.exceptions import ValidationError

class UserForm(forms.Form):
    username = forms.CharField(label='学号/工号', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密码', max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class InputForm(forms.ModelForm):
    def clean(self):
        cd = self.cleaned_data
        pscj = cd.get("pscj")
        zpcj = cd.get("zpcj")
        kscj = cd.get("kscj")

        if pscj < 0 or pscj > 100:
            raise ValidationError("Invalid data")
        if kscj < 0 or kscj > 100:
            raise ValidationError("Invalid data")
        if zpcj < 0 or zpcj > 100:
            raise ValidationError("Invalid data")
        return cd

    class Meta:
        model = models.Event
        exclude = ('id',)


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.OpenCourse
        exclude = ('id',)
