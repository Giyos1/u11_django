from django.db import models

from accounts.models import Card


class Transaction(models.Model):
    from_card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='from_card_transaction')
    to_card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='to_card_transaction')
    amount = models.IntegerField()

    class Meta:
        db_table = "transaction"

