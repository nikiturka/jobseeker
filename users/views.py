from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from main.forms import CustomUserCreationForm
from main.models import UserProfile


def login_user(request):
    if request.method == 'POST':
        email = request.POST["userEmail"]
        password = request.POST["userPassword"]

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('vacancies')
        else:
            messages.success(request, "Введены неверные данные, попробуйте снова!")
            return redirect('login')
    else:
        return render(request, 'users/login.html')


def logout_user(request):
    logout(request)

    messages.success(request, "Вы вышли из учётной записи.")
    return redirect('vacancies')


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user = authenticate(email=email, password=password)
            login(request, user)

            messages.success(request, "Регистрация прошла успешно!")

            return redirect('vacancies')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/registration.html', {"registration_form": form})


@login_required
def user_detail(request, pk):
    try:
        user_profile = UserProfile.objects.get(pk=pk)
        return render(request, 'users/user_detail.html', {"user_profile": user_profile})
    except UserProfile.DoesNotExist:
        return redirect('404_page')
