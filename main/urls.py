from django.urls import path

from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vacancies', views.all_vacancies, name='vacancies'),
    path('vacancies/<int:pk>', views.vacancy_detail, name='vacancy-detail')
]
