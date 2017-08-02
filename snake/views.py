from django.shortcuts import HttpResponse, redirect, render
from django.contrib import messages



def home(request):
    return render(request, 'snake/index.html')


def crawl(request):
    document_ids = request.POST.get('document_ids').split()
    if not document_ids:
        messages.warning(request,'no document ids supplied')
        return redirect('/')

    return
