import pytest

pytestmark = pytest.mark.django_db(transaction=True)
from wallet_api.apicore.models import Wallet
from django.db.models import F
from django.db import IntegrityError


def test_negative_balance():
    wallet = Wallet.objects.create(label='Test wallet', balance=100.00)
    with pytest.raises(IntegrityError):
        Wallet.objects.update(balance=F('balance')-200)
    wallet.refresh_from_db()
    assert wallet.balance == 100.00
