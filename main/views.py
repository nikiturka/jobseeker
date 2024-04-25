from django.shortcuts import render, redirect
from .models import Vacancy


def home(request):
    return render(request, 'main/base.html')


def all_vacancies(request):
    vacancies = (
        Vacancy.objects.all()
        .select_related("company")
        .values("pk", "salary_range", "required_experience_range", "title", "company__name", "description")
    )

    vacancies_count = vacancies.count()

    return render(request, "main/vacancies.html", {"vacancies": vacancies, "vacancies_total": vacancies_count})


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
            vacancies_count = vacancies_searched.count()

            return render(request, 'main/vacancies.html', {"vacancies": vacancies_searched,  "vacancies_total": vacancies_count})
        else:
            return redirect("vacancies")
    else:
        return redirect("vacancies")


def vacancy_detail(request, pk):
    vacancy = Vacancy.objects.filter(pk=pk).select_related("company")
    return render(request, "main/vacancy_detail.html", {"vacancy": vacancy})
