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
