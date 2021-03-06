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
    if snake.doc_count == 0:
        messages.warning(request,'no documents found for {}'.format(', '.join(doc_ids)))
        return redirect('/')
    file_name = os.path.basename(snake.path_to_zip)
    wrapper = FileWrapper(file(snake.path_to_zip, 'rb'))
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=' + file_name

    missing = [x for x in doc_ids if x not in snake.found_docs]
    messages.info(request, 'downloaded {0}/{1} files'.format(snake.doc_count, len(doc_ids)))
    messages.info(request, 'could not find records for {0}'.format(', '.join(missing)))

    return response


def poll_state(request):
    pass
