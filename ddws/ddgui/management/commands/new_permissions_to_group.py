""" This comannd create permission and add to existent group for User model """
# for existent groups list refer to ddws/hardcode.py - look at specific group 
#
# syntax:   python3 manage.py new_permission_to_group -g promo --permission can_hoax --text "Can hoax" 
#           python3 manage.py new_permission_to_group -g spoof -p can_spoof -t "Can spoof"
#           python3 manage.py new_permission_to_group -g recieve_news -p can_recievenews -t "Will recieve site news"
# permissions are optional and are not of greate use

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    
    help = "Make new group for User model"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-g', '--group_name', dest='group_name', type=str)
        parser.add_argument('-p', '--permission', dest='permission', type = str)
        parser.add_argument('-t', '--text', dest='text', type = str)

    # A command must define handle()
    def handle(self, *args, **options):
        """
        create group with self.group_name and add permission to User 
        """
        new_group = Group.objects.get(name=options.get('group_name'))
        ct = ContentType.objects.get_for_model(User)
        permission = Permission.objects.create(codename=options.get('permission'),
                                               name=options.get('text'),
                                               content_type=ct)
        new_group.permissions.add(permission)                                       
        self.stdout.write(f"Permission {options.get('permission')} added to group {options.get('group_name')} for User model")