from django.http import HttpResponse

from django.shortcuts import render, redirect

from books.forms import BookForm, BookModelForm
from books.models import Book


def home(request):
    return render(request, 'base.html')


def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/list.html', context={'books': books})


def book_detail(request, pk=None):
    book = Book.objects.filter(id=pk).first()
    return render(request, 'books/detail.html', context={'b': book})


def book_delete(request, pk=None):
    Book.objects.filter(id=pk).delete()
    return redirect('book_list')


def book_create(request):
    # form = BookForm()
    form = BookModelForm()
    return render(request, 'books/create.html', context={'form': form})


def book_create_post(request):
    # data = request.POST
    # Book.objects.create(
    #     title=data.get('title'),
    #     description=data.get('description'),
    #     price=data.get('price')
    # )
    # form = BookForm(request.POST)
    form = BookModelForm(request.POST)
    if form.is_valid():
        # data = form.cleaned_data
        # Book.objects.create(
        #     title=data.get('title'),
        #     description=data.get('description'),
        #     price=data.get('price'),
        #     page_count=data.get('page_count'),
        #     genre=data.get('genre')
        # )
        form.save()
        return redirect('book_list')
    else:
        return render(request, 'books/create.html', context={"form": form})


def book_update(request, pk=None):
    book = Book.objects.filter(id=pk).first()
    if request.method == 'POST':
        data = request.POST
        Book.objects.filter(id=pk).update(
            title=data.get('title'),
            description=data.get('description'),
            price=data.get('price')
        )
        return redirect('book_detail', book.id)
    return render(request, 'books/update.html', context={'book': book})
