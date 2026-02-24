from django.db import transaction
from django.shortcuts import render, redirect

from accounts.models import Card
from transaction.forms import TransactionForm


def transaction_(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            with transaction.atomic() as t:
                t = form.save(commit=False)
                t.to_card.amount += t.amount
                t.to_card.save()
                t.from_card.amount -= t.amount
                t.from_card.save()
                t.save()
            return redirect('post:list')
        else:
            return render(request, 'transaction/create.html', context={'form': form})
    else:
        form = TransactionForm()
        return render(request, 'transaction/create.html', context={'form': form})
