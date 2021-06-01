""" This comannd adds group to User model """
# syntax:   python3 manage.py delete_user_permissions -p can_spoof 
#           python3 manage.py delete_user_permissions --permission can_spoof
#           python3 manage.py delete_user_permissions --permission can_spoof


from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    
    help = "Delete existing group for User model"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-p', '--permission', dest='permission', type=str)

    # A command must define handle()
    def handle(self, *args, **options):
        """
        delete group with self.group_name 
        """
        try:
            del_permission =  Permission.objects.filter(codename=options.get('permission')).delete()
            self.stdout.write(f"Deleted permission {options.get('permission')} for User model")
        except Exception as ee:
            fake_temp = f"No such permission: {options.get('permission')}"
            raise AttributeError(fake_temp)
