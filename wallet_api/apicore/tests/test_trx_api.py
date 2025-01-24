import pytest

pytestmark = pytest.mark.django_db
from wallet_api.apicore.models import Wallet, Transaction


def test_transcation_endpoint(client, one_transaction):
    response = client.get('/v1/transactions/')
    assert Transaction.objects.count() == 1
    assert response.status_code == 200
    data = response.json()
    assert data.keys() == {'links', 'data', 'meta'}
    obj_list = data['data']
    assert obj_list == [
        {'type': 'Transaction', 'id': str(one_transaction.id),
         'attributes': {'txid': 'TX1', 'amount': '10.000000000000000000'}}
    ]


def test_single_transaction_endpoint(client, one_transaction):
    response = client.get(f'/v1/transactions/{one_transaction.id}/')
    assert Wallet.objects.count() == 1
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {'data'}
    assert data['data'] == {'type': 'Transaction', 'id': str(one_transaction.id),
                            'attributes': {'txid': 'TX1', 'amount': '10.000000000000000000'}}


def test_pagination_trxs(client, transactions20):
    response = client.get('/v1/transactions/', {'sort': 'id'})
    assert Wallet.objects.count() == 1
    assert Transaction.objects.count() == 20
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {'links', 'data', 'meta'}
    obj_list = data['data']
    assert len(obj_list) == 10


def test_sorting_trxs(client, transactions20):
    response = client.get('/v1/transactions/', {'sort': '-id'})
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 10
    ids = [item['id'] for item in data]
    assert ids == list(sorted(ids, reverse=True))


def test_filter_by_wallet_id(client, wallets3):
    w1, w2, w3 = wallets3
    response = client.get('/v1/transactions/', {'filter[wallet_id]': w1.pk})
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 2
    response = client.get('/v1/transactions/', {'filter[wallet_id]': w3.pk})
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 5
