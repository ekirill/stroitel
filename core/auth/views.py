from django.contrib.auth import login
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
            login(request, user)
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
