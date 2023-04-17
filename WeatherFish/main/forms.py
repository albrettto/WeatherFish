from django import forms
from django.forms import ModelForm, TextInput, Textarea
from .models import Feedback, Town, Measurement


class Measurement_Form(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['temp','pres','speed']
        widgets = {
            'temp': forms.RadioSelect,
            'pres': forms.RadioSelect,
            'speed': forms.RadioSelect,
        }


class Town_Form(forms.ModelForm):
    class Meta:
        model = Town
        fields = ['town_ch']
        widgets = {
            'town_ch': forms.RadioSelect,
        }


class Calendar_Form(forms.Form):
    date_inf = forms.DateField()
    date_inf.widget.attrs.update({'class' : 'form-control col'})
    date_inf2 = forms.DateField()
    date_inf2.widget.attrs.update({'class' : 'form-control col'})


class Feedback_Form(ModelForm):
    class Meta:
        # Определяем модель, на основе которой создаем форму
        model = Feedback
        # Поля, которые будем использовать для заполнения
        fields = ['email', 'message']

        widgets = {
            "email": TextInput(attrs = {
                'class': 'form-control',
                'placeholder':'example@gmail.com'
            }),
            "message": Textarea(attrs = {
                'class': 'form-control'
            }),
        }
