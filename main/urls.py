from django.urls import path

from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vacancies', views.all_vacancies, name='vacancies'),
    path('vacancies_search', views.vacancies_search, name='vacancies-search'),
    path('vacancies/<int:pk>', views.vacancy_detail, name='vacancy-detail'),
    path('vacancies/create', views.create_vacancy, name='vacancy-create'),
    path('vacancies/delete/<int:pk>', views.delete_vacancy, name='vacancy-delete')
]
