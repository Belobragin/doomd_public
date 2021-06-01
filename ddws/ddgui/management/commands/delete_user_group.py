""" This comannd adds group to User model """
# syntax:   python3 manage.py delete_user_group -g promo
#           python3 manage.py delete_user_group -g spoof


from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    
    help = "Delete existing group for User model"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-g', '--group_name', dest='group_name', type=str)

    # A command must define handle()
    def handle(self, *args, **options):
        """
        delete group with self.group_name 
        """
        try:
            del_group = Group.objects.filter(name=options.get('group_name')).delete()
            self.stdout.write(f"Deleted group {options.get('group_name')} for User model")
        except Exception as ee:
            fake_temp = f"No such user group: {options.get('group_name')}"
            raise AttributeError(fake_temp)