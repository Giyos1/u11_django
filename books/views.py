from django.http import HttpResponse

from django.shortcuts import render, redirect

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
    return render(request, 'books/create.html')


def book_create_post(request):
    data = request.POST
    Book.objects.create(
        title=data.get('title'),
        description=data.get('description'),
        price=data.get('price')
    )
    return redirect('book_list')


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
