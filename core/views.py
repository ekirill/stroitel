from django.shortcuts import render


def guide(request):
    return render(request, 'guide.html', {'page': 'guide'})


def initiatives(request):
    return render(request, 'initiatives.html', {'page': 'initiatives'})


def documents(request):
    return render(request, 'documents.html', {'page': 'documents'})


def contacts(request):
    return render(request, 'contacts.html', {'page': 'contacts'})
