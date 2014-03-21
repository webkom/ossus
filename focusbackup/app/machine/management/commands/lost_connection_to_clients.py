# -*- coding: utf-8 -*-

from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template import loader, Context

from focusbackup.app.machine.models import Machine


class Command(BaseCommand):

    def handle (self, *args, **kwargs):

        lost_machines = []

        for machine in Machine.objects.filter(template=False):
            if machine.lost_connection_to_client():
                lost_machines.append(machine)

        template = loader.get_template("machine/templates/lost_machines.html")

        subject, from_email, to = 'Focus24 - lost machines', 'focus24@focus24.no', 'me@frecar.no'

        html_content = template.render(Context({
            'machines': lost_machines
        }))

        msg = EmailMultiAlternatives(subject, "", from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()