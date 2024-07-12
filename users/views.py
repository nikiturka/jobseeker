from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from main.forms import CustomUserCreationForm
from main.models import UserProfile, HR, Vacancy
from .forms import UserProfileChangeForm, HRProfileChangeForm, UserProfilePictureChangeForm, HRProfilePictureChangeForm


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

            if form.cleaned_data['is_hr'] is True:
                new_hr = HR.objects.create(user=user, is_hr=True)
                new_hr.save()

                messages.success(request, "Аккаунт нанимателя создан.")
            else:
                new_user = UserProfile.objects.create(user=user)
                new_user.save()
                messages.success(request, "Аккаунт создан.")

            messages.success(request, "Регистрация прошла успешно!")

            return redirect('vacancies')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/registration.html', {"registration_form": form})


@login_required
def user_detail(request, pk):
    user_profile = UserProfile.objects.get(user__pk=pk)

    if request.method == 'POST':
        user_form = UserProfileChangeForm(request.POST, request.FILES, instance=user_profile)
        pfp_form = UserProfilePictureChangeForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid():
            user_form.save()

        if pfp_form.is_valid():
            pfp_form.save()

            messages.success(request, "Информация о профиле была изменена.")
        else:
            messages.success(request, "Не удалось изменить информацию о профиле.")

    else:
        user_form = UserProfileChangeForm(instance=user_profile)
        pfp_form = UserProfilePictureChangeForm(instance=user_profile)

    return render(request, 'users/user_detail.html', {'form': user_form, 'pfp_form': pfp_form})


@login_required
def hr_detail(request, pk):
    hr_profile = HR.objects.get(user__pk=pk)

    hr_vacancies = Vacancy.objects.filter(publisher=hr_profile)

    if request.method == 'POST':
        form = HRProfileChangeForm(request.POST, request.FILES, instance=hr_profile)
        pfp_form = HRProfilePictureChangeForm(request.POST, request.FILES, instance=hr_profile)

        if form.is_valid():
            form.save()

        if pfp_form.is_valid():
            pfp_form.save()

            messages.success(request, "Информация о профиле была изменена.")
        else:
            messages.success(request, "Не удалось изменить информацию о профиле.")

    else:
        form = HRProfileChangeForm(instance=hr_profile)
        pfp_form = HRProfilePictureChangeForm(instance=hr_profile)

    return render(request, 'users/hr_detail.html', {'form': form, "pfp_form": pfp_form, "hr_vacancies": hr_vacancies})
