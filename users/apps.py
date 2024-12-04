from django.apps import AppConfig
from django.contrib.auth.models import Group

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(create_groups, sender=self)

def create_groups(sender, **kwargs):
    user_group, created = Group.objects.get_or_create(name='User')
    manager_group, created = Group.objects.get_or_create(name='Manager')
    
    if created:
        user_group.permissions.set([
            'add_mailing', 'change_mailing', 'view_mailing',
            'add_receiver', 'change_receiver', 'view_receiver'
        ])
        manager_group.permissions.set([
            'view_user', 'view_mailing', 'view_receiver',
            'change_mailing', 'change_receiver'
        ])
