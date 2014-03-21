# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template import loader, Context

from focusbackup.app.machine.models import Machine


class Command(BaseCommand):

    def handle (self, *args, **kwargs):

        delayed_machines = []

        for machine in Machine.objects.filter(template=False):
            if machine.delayed_schedules():
                delayed_machines.append(machine)

        template = loader.get_template("machine/templates/delayed_machines.html")

        subject, from_email, to = 'Focus24 - delays', 'focus24@focus24.no', 'me@frecar.no'

        html_content = template.render(Context({
            'machines': delayed_machines
        }))

        msg = EmailMultiAlternatives(subject, "", from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
