from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'page': 'index'})


def documents(request):
    return render(request, 'documents.html', {'page': 'documents'})


def contacts(request):
    return render(request, 'contacts.html', {'page': 'contacts'})
