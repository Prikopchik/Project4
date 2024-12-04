from django.core.management.base import BaseCommand
from mailings.models import Mailing
from mailings.utils import send_mailing

class Command(BaseCommand):
    help = 'Send a mailing by its ID.'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки для отправки')

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']
        try:
            mailing = Mailing.objects.get(pk=mailing_id)
            success = send_mailing(mailing)
            if success:
                self.stdout.write(self.style.SUCCESS(f'Рассылка {mailing_id} успешно отправлена.'))
            else:
                self.stdout.write(self.style.ERROR(f'Не удалось отправить рассылку {mailing_id}.'))
        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Рассылка с ID {mailing_id} не найдена.'))
