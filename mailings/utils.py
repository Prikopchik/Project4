import smtplib
from email.mime.text import MIMEText
from .models import MailingAttempt

def send_mailing(mailing):
    """Функция для отправки рассылки и записи попытки."""
    recipients = mailing.recipients.all()
    message = mailing.message
    success_count = 0

    for recipient in recipients:
        try:
            msg = MIMEText(message.body)
            msg['Subject'] = message.subject
            msg['From'] = 'example_email@example.com'
            msg['To'] = recipient.email

            with smtplib.SMTP('smtp.example.com', 587) as server:
                server.starttls()
                server.login('example_email@example.com', 'password') 
                server.send_message(msg)

            MailingAttempt.objects.create(
                mailing=mailing,
                status='Успешно',
                response='Message sent successfully'
            )
            success_count += 1

        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status='Не успешно',
                response=str(e)
            )

    return success_count == len(recipients) 
