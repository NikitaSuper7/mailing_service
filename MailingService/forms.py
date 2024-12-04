from django import forms
from django.forms import BooleanField

from .models import Mailing
from django.core.exceptions import ValidationError


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = "form-check-input"
            else:
                fild.widget.attrs['class'] = 'form-class'



class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['name', 'client', 'massage', 'message_states', 'sent_at', 'end_send_at']

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название продукта'
        })
        self.fields['client'].widget.attrs.update({
            'class': 'form-control',

        })
        self.fields['massage'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['message_states'].widget.attrs.update({
            'class': 'form-control',
        })

        # self.fields['created_at'].widget.attrs.update({
        #     'class': 'form-control',
        # })
        self.fields['sent_at'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['end_send_at'].widget.attrs.update({
            'class': 'form-control'
        })