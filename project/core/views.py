import mimetypes
import os
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from project.app.backup.models import ClientVersion

STATIC_ROOT = os.path.join(settings.BASE_PATH, "media")

def get_absolute_filename(filename='', safe=True):
    if not filename:
        return os.path.join(STATIC_ROOT, 'index')
    if safe and '..' in filename.split(os.path.sep):
        return get_absolute_filename(filename='')

    return os.path.join(STATIC_ROOT, filename)

def retrieve_file(request, filename=''):
    abs_filename = get_absolute_filename(filename)

    mimetypes.add_type('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx', True)
    mime = mimetypes.guess_type(abs_filename)

    wrapper = FileWrapper(file(abs_filename))
    response = HttpResponse(wrapper, content_type=mime[0])
    response['Content-Length'] = os.path.getsize(abs_filename)

    return response

def download_current_agent(request):
    current_agent = ClientVersion.objects.get(current_agent=True)
    return redirect("/file/%s"%current_agent.agent.name)

def download_current_updater(request):
    current_agent = ClientVersion.objects.get(current_updater=True)
    return redirect("/file/%s"%current_agent.updater.name)