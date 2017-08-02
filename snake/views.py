import os
import StringIO
import tempfile
import zipfile
from wsgiref.util import FileWrapper

from django.conf import settings
from django.contrib import messages
from django.shortcuts import HttpResponse, redirect, render
from scripts.browser import SnakeySnake


def home(request):
    return render(request, 'snake/index.html')


def crawl(request):
    for f in os.listdir(settings.BASE_DIR):
        if f.endswith('.zip'):
            os.remove(f)
    doc_ids = request.POST.get('document_ids').split()
    if not doc_ids:
        messages.warning(request, 'no document ids supplied')
        return redirect('/')
    snake = SnakeySnake(settings.BASE_DIR)
    snake.retrieve_and_zip_documents(doc_ids)
    snake.kill()
    file_name = os.path.basename(snake.path_to_zip)
    wrapper = FileWrapper(file(snake.path_to_zip, 'rb'))
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    return response


def poll_state(request):
    pass
