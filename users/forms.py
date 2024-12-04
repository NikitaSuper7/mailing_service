from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


# Форма регистрации пользователей:
class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False, help_text="Введите номер телефона")
    username = forms.CharField(max_length=50, required=False)
    usable_password = None

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

        def clean_phone_number(self):
            phone_number = self.cleaned_data.get('phone_number')
            if phone_number and not phone_number.isdigit():
                raise forms.ValidationError("Номер телефона должен состоять только из цифр")
            return phone_number
