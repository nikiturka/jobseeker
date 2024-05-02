from django.shortcuts import render, redirect, get_object_or_404
from .models import Vacancy, UserProfile
from django.core.paginator import Paginator


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
    increase_vacancy_views(request, pk)

    vacancy = Vacancy.objects.get(pk=pk)
    similar_vacancies = Vacancy.objects.filter(company=vacancy.company).exclude(pk=pk)[:4]

    return render(request, "main/vacancy_detail.html", {"vacancy": vacancy, "similar_vacancies": similar_vacancies})


def increase_vacancy_views(request, vacancy_id):
    user = request.user.id
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)

    if user not in vacancy.views.all():
        vacancy.views.add(user)
        vacancy.save()

    return redirect('vacancy-detail', pk=vacancy_id)
