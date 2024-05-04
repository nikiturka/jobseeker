from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import VacancyCreationForm
from .models import Vacancy, HR
from django.core.paginator import Paginator
from .tasks import notify_publisher_on_vacancy_reply


def home(request):
    return render(request, 'main/base.html', {"user": request.user})


def all_vacancies(request):
    vacancies = (
        Vacancy.objects.all()
        .select_related("company")
        .values("pk", "salary_range", "required_experience_range", "title", "company__name", "description")
    )

    p = Paginator(vacancies, 4)
    page = request.GET.get('page')
    vacancies_paginated = p.get_page(page)

    vacancies_count = vacancies.count()

    return render(request, "main/vacancies.html", {"vacancies": vacancies_paginated, "vacancies_total": vacancies_count, "user": request.user})


def vacancies_search(request):
    if request.method == "POST":
        searched = request.POST['search-query']
        if searched:
            vacancies_searched = (
                Vacancy
                .objects
                .filter(title__icontains=searched)
                .select_related("company")
                .values("pk", "salary_range", "required_experience_range", "title", "company__name", "description")
            )

            paginator = Paginator(vacancies_searched, 4)
            page = request.GET.get('page')
            vacancies_paginated = paginator.get_page(page)

            vacancies_count = vacancies_searched.count()

            return render(request, 'main/vacancies_search.html', {"vacancies": vacancies_paginated,  "vacancies_total": vacancies_count})
        else:
            return redirect("vacancies")
    else:
        vacancies_searched = request.session['search_results']

        paginator = Paginator(vacancies_searched, 4)
        page = request.GET.get('page')
        vacancies_paginated = paginator.get_page(page)

        vacancies_count = len(vacancies_searched)

        return render(request, 'main/vacancies_search.html', {"vacancies": vacancies_paginated, "vacancies_total": vacancies_count})


def vacancy_detail(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    similar_vacancies = Vacancy.objects.filter(company=vacancy.company).exclude(pk=pk)[:4]
    user = request.user

    if user.is_authenticated:
        if hasattr(user, 'userprofile'):
            user_profile = user.userprofile

            if user_profile not in vacancy.views.all():
                vacancy.views.add(user_profile)
                vacancy.save()

            if request.method == 'POST':
                if user_profile not in vacancy.responses.all():
                    vacancy.responses.add(user_profile)
                    vacancy.save()

                    messages.success(request, 'Вы откликнулись на вакансию.')

                    notify_publisher_on_vacancy_reply.delay(vacancy.id, vacancy.publisher.id)
                else:
                    messages.error(request, 'Вы уже откликались на эту вакансию.')
                return redirect('vacancy-detail', pk=pk)

            return render(request, "main/vacancy_detail.html", {"vacancy": vacancy, "similar_vacancies": similar_vacancies})

        elif hasattr(user, 'hr'):
            if request.method == 'POST':
                messages.error(request, 'HR не может откликаться на вакансии.')
                return redirect('vacancy-detail', pk=pk)
    else:
        if request.method == 'POST':
            messages.error(request, 'Авторизуйтесь, чтобы откликаться на вакансии.')
            return redirect('vacancy-detail', pk=pk)

        return render(request, "main/vacancy_detail.html", {"vacancy": vacancy, "similar_vacancies": similar_vacancies})

    return render(request, "main/vacancy_detail.html", {"vacancy": vacancy, "similar_vacancies": similar_vacancies})


def create_vacancy(request):
    if request.user.is_authenticated:
        is_hr = HR.objects.filter(user=request.user).exists()

        if is_hr:
            if request.method == 'POST':
                form = VacancyCreationForm(request.POST)

                if form.is_valid():
                    vacancy = form.save(commit=False)
                    vacancy.publisher = HR.objects.get(user=request.user)
                    vacancy.save()

                    messages.success(request, "Вакансия размещена.")
                else:
                    messages.success(request, "Не удалось разместить вакансию.")

            else:
                form = VacancyCreationForm()

            return render(request, 'main/vacancy_create.html', {"form": form})
        else:
            return JsonResponse({'Error': 'Вы не являетесь работодателем'})
    else:
        return JsonResponse({'Error': 'Авторизуйтесь, прежде чем зайти на эту страницу.'})


def delete_vacancy(request, pk):
    if request.user.is_authenticated:
        hr = HR.objects.filter(user=request.user)

        if hr.exists():
            vacancy = Vacancy.objects.filter(pk=pk, publisher=hr.first())

            if vacancy.exists():
                vacancy.delete()
                messages.success(request, "Вакансия удалена.")

                return redirect('vacancies')
            else:
                return JsonResponse({'Error': 'Vacancy does not exist.'})
        else:
            return JsonResponse({'Error': 'You are not an HR'})
    else:
        return JsonResponse({'Error': 'Authorize first.'})
