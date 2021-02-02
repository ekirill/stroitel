from django import forms
from core.models import StroiUser
from core.services.auth import normalize_phone, is_stroi_staff


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=False)
    password = forms.CharField(max_length=50, required=False)
    phone = forms.CharField(max_length=20, required=False)

    def clean_username(self):
        username = self.cleaned_data['username'].strip()

        if not username:
            raise forms.ValidationError('Заполните поле')

        if not username.isdigit():
            raise forms.ValidationError('Введите только цифры номера участка')

        if StroiUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Вы уже зарегистрированы. Воспользуйтесь входом.')

        return username

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        if not phone:
            raise forms.ValidationError('Заполните поле')

        norm_phone = normalize_phone(self.cleaned_data['phone'])
        if not norm_phone or not norm_phone.startswith('8') or len(norm_phone) < 11:
            raise forms.ValidationError(
                'Номер телефона должен состоять из 11 цифр и начинаться с 8 или +7'
            )

        if not is_stroi_staff(norm_phone):
            raise forms.ValidationError(
                'Ваш номер отсутствует в базе данных. '
                'Напишите в основной WhatsApp чат СНТ '
                'просьбу о добавлении номера.'
            )

        if StroiUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Пользователь с этим номером телефона уже зарегистрирован.')

        return norm_phone

    def clean_password(self):
        password = self.cleaned_data['password'].strip()
        if not password:
            raise forms.ValidationError('Заполните поле')

        if len(password) < 6:
            raise forms.ValidationError('Пароль должен быть не менее 6 символов')

        return password

    class Meta:
        model = StroiUser
        fields = ["username", "password", "phone"]
