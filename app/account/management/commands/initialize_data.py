from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    """
    Commands class to initialize the custom Admins and Moderators groups and their respoective permissions
    upon project/django container start.
    """
    help = 'Initialize groups and permissions'

    def handle(self, *args, **kwargs):
        permissions = [
            {"codename": "can_view_users", "name": "Can view users page"},
            {"codename": "can_manage_users", "name": "Can manage users page"},
            {"codename": "can_manage_themes", "name": "Can manage themes page"},
            {"codename": "can_manage_rooms", "name": "Can manage rooms page"},
            {"codename": "can_view_abuse_reports", "name": "Can view abuse reports page"},
            {"codename": "can_process_abuse_reports", "name": "Can process abuse reports page"},
            {"codename": "can_manage_offending_words", "name": "Can manage offending words page"},
        ]

        content_type = ContentType.objects.get(app_label='account', model='profile')

        for perm in permissions:
            Permission.objects.get_or_create(
                codename=perm["codename"],
                name=perm["name"],
                content_type=content_type,
            )

        admins_group, _ = Group.objects.get_or_create(name="Admins")
        moderators_group, _ = Group.objects.get_or_create(name="Moderators")

        all_permissions = Permission.objects.filter(codename__in=[perm["codename"] for perm in permissions])
        admins_group.permissions.set(all_permissions)

        moderator_permissions = all_permissions.filter(codename__in=["can_view_abuse_reports",
                                                                     "can_manage_offending_words",
                                                                     "can_process_abuse_reports"])
        moderators_group.permissions.set(moderator_permissions)

        self.stdout.write(self.style.SUCCESS('Groups and permissions initialized successfully!'))
