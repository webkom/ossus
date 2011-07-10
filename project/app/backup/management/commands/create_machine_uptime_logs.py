# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from app.backup.models import Machine

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Machine.create_uptime_logs()