from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from jobseeker import settings
from main.models import HR, Vacancy


@shared_task()
def notify_publisher_on_vacancy_reply(vacancy_id, hr_id):
    hr = HR.objects.get(id=hr_id)
    hr_email = hr.user.email

    vacancy = Vacancy.objects.get(pk=vacancy_id)

    mail_subject = "На вашу вакансию откликнулись"
    message = f"У вас новый отклик на вакансию {vacancy.title}!\nДля детального просмотра перейдите в Ваш профиль."
    to_email = hr_email

    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )

    return f"Message sent to {to_email}"
