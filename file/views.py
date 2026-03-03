from django.shortcuts import render, redirect

from file.forms import DocumentForm
from file.models import Document


def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post:list')
        else:
            return render(request, 'file/upload.html', {'form': form})
    else:
        form = DocumentForm()
        return render(request, 'file/upload.html', {'form': form})


def file_list(request):
    files = Document.objects.all()
    return render(request, 'file/list.html', {'files': files})
