from django.shortcuts import render, redirect
from .models import Vacancy
from django.core.paginator import Paginator


def home(request):
    return render(request, 'main/base.html')


def all_vacancies(request):
    vacancies = (
        Vacancy.objects.all()
        .select_related("company")
        .values("pk", "salary_range", "required_experience_range", "title", "company__name", "description")
    )

    p = Paginator(vacancies, 1)
    page = request.GET.get('page')
    vacancies_paginated = p.get_page(page)

    vacancies_count = vacancies.count()

    return render(request, "main/vacancies.html", {"vacancies": vacancies_paginated, "vacancies_total": vacancies_count})


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

            paginator = Paginator(vacancies_searched, 1)
            page = request.GET.get('page')
            vacancies_paginated = paginator.get_page(page)

            vacancies_count = vacancies_searched.count()

            return render(request, 'main/vacancies_search.html', {"vacancies": vacancies_paginated,  "vacancies_total": vacancies_count})
        else:
            return redirect("vacancies")
    else:
        vacancies_searched = request.session['search_results']

        paginator = Paginator(vacancies_searched, 1)
        page = request.GET.get('page')
        vacancies_paginated = paginator.get_page(page)

        vacancies_count = len(vacancies_searched)

        return render(request, 'main/vacancies_search.html', {"vacancies": vacancies_paginated, "vacancies_total": vacancies_count})


def vacancy_detail(request, pk):
    vacancy = Vacancy.objects.filter(pk=pk).select_related("company")
    return render(request, "main/vacancy_detail.html", {"vacancy": vacancy})
