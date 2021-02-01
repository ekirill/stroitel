from django import forms
from core.models import StroiUser
from core.services.auth import normalize_phone, is_stroi_staff


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=20)

    def clean_username(self):
        username = self.cleaned_data['username'].strip()

        if not username:
            raise forms.ValidationError('Обязательное поле.')

        if not username.isdigit():
            raise forms.ValidationError('Номер участка должен состоять только из цифр.')

        if StroiUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с этим номером участка уже зарегистрирован.')

        return username

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        if not phone:
            raise forms.ValidationError('Обязательное поле.')

        norm_phone = normalize_phone(self.cleaned_data['phone'])
        if not norm_phone or not norm_phone.startswith('8') or len(norm_phone) < 11:
            raise forms.ValidationError(
                'В номере телефона должно быть не менее 11 цифр, и номер должен начинаться с `8` или `+7`.'
            )

        if not is_stroi_staff(norm_phone):
            raise forms.ValidationError(
                'Ваш номер не найден среди известных нам номеров телефонов СНТ. '
                'Если вы, действительно, член СНТ Строитель, напишите в общий WhatsApp чат СНТ Строитель '
                'просьбу добавить Ваш номер.'
            )

        if StroiUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Пользователь с этим номером телефона уже зарегистрирован.')

        return norm_phone

    def clean_password(self):
        password = self.cleaned_data['password'].strip()
        if not password:
            raise forms.ValidationError('Обязательное поле.')

        if len(password) < 6:
            raise forms.ValidationError('Пароль должен быть не менее 6 символов.')

        return password

    class Meta:
        model = StroiUser
        fields = ["username", "password", "phone"]
