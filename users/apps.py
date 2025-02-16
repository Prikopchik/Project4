from django.apps import AppConfig
from django.db.models.signals import post_migrate

class UsersConfig(AppConfig):
    name = 'users'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        post_migrate.connect(create_groups, sender=self)


def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Permission, Group
    from django.contrib.contenttypes.models import ContentType

    mailing_content_type = ContentType.objects.filter(app_label="mailings").first()
    receiver_content_type = ContentType.objects.filter(app_label="mailings").first()

    if not mailing_content_type or not receiver_content_type:
        print("ContentType для mailings ещё не создан. Пропускаем создание групп.")
        return  

    user_permissions = Permission.objects.filter(codename__in=[
        'add_mailing', 'change_mailing', 'view_mailing',
        'add_receiver', 'change_receiver', 'view_receiver'
    ])

    manager_permissions = Permission.objects.filter(codename__in=[
        'view_user', 'view_mailing', 'view_receiver',
        'change_mailing', 'change_receiver'
    ])

    user_group, _ = Group.objects.get_or_create(name='User')
    manager_group, _ = Group.objects.get_or_create(name='Manager')

    user_group.permissions.set(user_permissions)
    manager_group.permissions.set(manager_permissions)

    print("Группы User и Manager успешно созданы и настроены.")
