from django.shortcuts import render


def social_login(request):
    return render(request, 'social_login.html', {})
