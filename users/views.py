from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_user(request):
    if request.method == 'POST':
        email = request.POST["userEmail"]
        password = request.POST["userPassword"]

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('vacancies')
        else:
            messages.success(request, "There was an error logging in, try again!")
            return redirect('login')
    else:
        return render(request, 'users/login.html')


def logout_user(request):
    logout(request)

    messages.success(request, "You've just logged out.")
    return redirect('vacancies')
