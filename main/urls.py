from django.urls import path

from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vacancies', views.all_vacancies, name='vacancies'),
    path('vacancies_search', views.vacancies_search, name='vacancies-search'),
    path('vacancies/<int:pk>', views.vacancy_detail, name='vacancy-detail'),
    path('vacanvies/create_vacancy', views.create_vacancy, name='vacancy-create')
]
