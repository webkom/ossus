import mimetypes
import os
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from settings import BASE_PATH

STATIC_ROOT = os.path.join(BASE_PATH, "media")

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