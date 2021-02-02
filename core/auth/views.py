from django.contrib.auth import login as do_login
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
)
from django.shortcuts import render

from core.auth.forms import RegisterForm


def register(request):
    success_registration = False
    if request.method == 'POST':
        user_form = RegisterForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            success_registration = True
            do_login(request, user)
    else:
        user_form = RegisterForm()

    return render(
        request,
        'auth/register.html',
        {
            'form':user_form,
            'success_registration': success_registration,
        }
    )


class LoginView(BaseLoginView):
    template_name = 'auth/login.html'


class LogoutView(BaseLogoutView):
    template_name = 'auth/logout.html'
