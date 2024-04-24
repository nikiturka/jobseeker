from django.shortcuts import render
from .models import Vacancy, Company


def home(request):
    return render(request, 'main/base.html')


def all_vacancies(request):
    vacancies = (
        Vacancy.objects.all()
        .select_related("company")
        .values("pk", "salary_range", "required_experience_range", "title", "company__name")
    )

    return render(request, "main/vacancies.html", {"vacancies": vacancies})


def vacancy_detail(request, pk):
    vacancy = Vacancy.objects.filter(pk=pk).select_related("company")
    return render(request, "main/vacancy_detail.html", {"vacancy": vacancy})
