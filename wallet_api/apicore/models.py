from django.db import models

# 18-digits precision is ambiguous: is it 18 digits total or 18 before point and 18 after?
# Let's be conservative and use more digits on the both sides
MAXDIGITS = 37
DECIMAL_PLACES = 18


class Wallet(models.Model):
    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=MAXDIGITS, decimal_places=DECIMAL_PLACES)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(balance__gte=0), name='balance_gtzero')
        ]
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'


class Transaction(models.Model):
    wallet_id = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='transactions')
    txid = models.CharField(null=False, blank=False, max_length=255, unique=True)
    amount = models.DecimalField(max_digits=MAXDIGITS, decimal_places=DECIMAL_PLACES, db_index=True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

        indexes = [
            models.Index(fields=['wallet_id']),
            # We will almost always filter by wallet_id and then often filter by amount
            models.Index(fields=['wallet_id', 'amount']),
            # Should we really filter by amount without filtering by wallet_id?
            models.Index(fields=['amount']),
            # This is for getting tx by id, which is obv external primary key
            models.Index(fields=['txid']),
        ]
