# -*- coding: utf-8 -*-

from django.core.management.commands.loaddata import Command as loaddata
from django.db import connection, transaction


class Command(loaddata):
    def handle (self, *args, **kwargs):
        cursor = connection.cursor()

        cursor.execute("delete from auth_group_permissions;")
        transaction.commit_unless_managed()

        cursor.execute("delete from auth_permission;")
        transaction.commit_unless_managed()

        cursor.execute("delete from django_admin_log;")
        transaction.commit_unless_managed()

        cursor.execute("delete from django_content_type;")
        transaction.commit_unless_managed()

        super(Command, self).handle(*args, **kwargs)