# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template import loader, Context

from focusbackup.app.machine.models import Machine


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        delayed_machines = []

        for machine in Machine.objects.filter(template=False, active=True):
            if machine.delayed_schedules():
                delayed_machines.append(machine)

        if delayed_machines:
            template = loader.get_template("machine/templates/delayed_machines.html")

            subject, from_email = '%s - delays' % settings.BRAND, settings.DEFAULT_FROM_EMAIL
            to = [admin[0] for admin in settings.ADMINS]

            html_content = template.render(Context({
                'machines': delayed_machines
            }))

            msg = EmailMultiAlternatives(subject, "", from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
