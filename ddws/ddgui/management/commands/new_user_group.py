""" This comannd adds group to User model """
#for permissions essence refer to ddws/hardcode.py - look at specific group 
# syntax:   python3 manage.py new_user_group -g promo
#           python3 manage.py new_user_group -g spoof
#           python3 manage.py new_user_group -g news

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    
    help = "Make new group for User model"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-g', '--group_name', dest='group_name', type=str)

    # A command must define handle()
    def handle(self, *args, **options):
        """
        create group with self.group_name
        """
        new_group, created = Group.objects.get_or_create(name=options.get('group_name'))                                    
        self.stdout.write(f"Group {options.get('group_name')} created")