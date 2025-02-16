from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission

class UsersConfig(AppConfig):
    name = 'users'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        post_migrate.connect(create_groups, sender=self)

def create_groups(sender, **kwargs):
    """Создаём группы и назначаем им права после миграций"""
    user_group, _ = Group.objects.get_or_create(name='User')
    manager_group, _ = Group.objects.get_or_create(name='Manager')

    # Получаем объекты Permission
    user_permissions = [
        Permission.objects.get(codename='add_mailing', content_type__app_label='mailings'),
        Permission.objects.get(codename='change_mailing', content_type__app_label='mailings'),
        Permission.objects.get(codename='view_mailing', content_type__app_label='mailings'),
        Permission.objects.get(codename='add_receiver', content_type__app_label='mailings'),
        Permission.objects.get(codename='change_receiver', content_type__app_label='mailings'),
        Permission.objects.get(codename='view_receiver', content_type__app_label='mailings'),
    ]

    manager_permissions = [
        Permission.objects.get(codename='view_user', content_type__app_label='users'),
        Permission.objects.get(codename='view_mailing', content_type__app_label='mailings'),
        Permission.objects.get(codename='view_receiver', content_type__app_label='mailings'),
        Permission.objects.get(codename='change_mailing', content_type__app_label='mailings'),
        Permission.objects.get(codename='change_receiver', content_type__app_label='mailings'),
    ]

    user_group.permissions.set(user_permissions)
    manager_group.permissions.set(manager_permissions)
