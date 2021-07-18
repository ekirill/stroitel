from django.shortcuts import render


def billing(request):
    context = {

    }
    return render(request, "billing/index.html", context)
