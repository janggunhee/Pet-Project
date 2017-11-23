from django.core.mail import send_mail

from config import celery_app


# celery에 task를 등록하는 데코레이션
@celery_app.task(bind=True)
def send_mail_task(self, subject, message, from_email, recipient):
    # send_mail 함수를 구현
    send_mail(
        # subject=제목
        # message=text로 렌더링되는 html 파일
        # from_email=발신자 (settings.EMAIL_HOST_USER)
        # recipient=수신자
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[
            recipient,
        ]
    )
