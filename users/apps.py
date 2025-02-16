from django.apps import AppConfig
from django.db.models.signals import post_migrate

class UsersConfig(AppConfig):
    name = 'users'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        post_migrate.connect(create_groups, sender=self)
    
def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Permission,Group
    import time
    
    retries = 5
    for _ in range(retries):
        if Permission.objects.filter(codename='add_mailing').exists():
            break
        time.sleep(1)  

    try:
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

    except Permission.DoesNotExist:
        print("Не удалось найти нужные права, возможно, они ещё не созданы.")
