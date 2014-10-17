# -*- coding: utf-8 -*-

from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template import loader, Context

from focusbackup.app.machine.models import Machine


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        lost_machines = []

        for machine in Machine.objects.filter(template=False, active=True):
            if machine.lost_connection_to_client():
                lost_machines.append(machine)

        if lost_machines:
            template = loader.get_template("machine/templates/lost_machines.html")
            subject = 'Focus24 - lost machines'
            from_email, to = 'focus24@focus24.no', 'me@frecar.no'

            html_content = template.render(Context({
                'machines': lost_machines
            }))

            msg = EmailMultiAlternatives(subject, "", from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
