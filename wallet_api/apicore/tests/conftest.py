import pytest
from wallet_api.apicore.models import Wallet
pytestmark = [pytest.mark.django_db]


@pytest.fixture
def default_wallet():
    wallet, _ = Wallet.objects.get_or_create(label='Test wallet', balance=100.00)
    return wallet


@pytest.fixture
def wallets20():
    for i in range(20):
        Wallet.objects.create(label=f'Test wallet {i}', balance=i * 10.00)
    return Wallet.objects.all()


@pytest.fixture
def transactions20(default_wallet):
    for i in range(20):
        default_wallet.transactions.create(txid=f'TX{i}', amount=i * 10.00)
    return default_wallet.transactions.all()


@pytest.fixture
def one_transaction(default_wallet):
    default_wallet.transactions.create(txid='TX1', amount=10.00)
    return default_wallet.transactions.first()


@pytest.fixture
def wallets3():
    w1, w2, w3 = (Wallet.objects.create(label=f'Test wallet {i}', balance=i * 10.00) for i in range(3))
    for i in range(2):
        w1.transactions.create(txid=f'W1_TX{i}', amount=i * 10.00)
    for i in range(3):
        w2.transactions.create(txid=f'W2_TX{i}', amount=i * 20.00)
    for i in range(5):
        w3.transactions.create(txid=f'W3_TX{i}', amount=i * -30.00)
    return w1, w2, w3
