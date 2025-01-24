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
    assert response.status_code == 200
    data = response.json()
    assert data['data'] == {'type': 'Transaction', 'id': str(one_transaction.id),
                            'attributes': {'txid': 'TX1', 'amount': '10.000000000000000000'}}


def test_single_transaction_endpoint_by_txid(client, one_transaction):
    response = client.get(f'/v1/transactions/by-txid/{one_transaction.txid}/')
    assert response.status_code == 200
    data = response.json()
    assert data['data']['id'] == str(one_transaction.id)
    assert data['data']['attributes']['txid'] == 'TX1'


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
    response = client.get('/v1/transactions/', {'filter[wallet_id]': w1.pk, 'sort': 'id'})
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 2

    response = client.get('/v1/transactions/', {'filter[wallet_id]': w3.pk, 'sort': 'id'})
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 6


def test_filter_by_amount(client, wallets3):
    w1, w2, w3 = wallets3
    response = client.get('/v1/transactions/', {'filter[amount.gt]': '100', 'sort': 'id'})
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 1
    assert data[0]['attributes']['amount'] == '500.000000000000000000'

    response = client.get('/v1/transactions/', {'filter[amount.lt]': '-100.0000', 'sort': 'id'})
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 2
    assert {item['attributes']['amount'] for item in data} == {'-120.000000000000000000', '-150.000000000000000000'}

    response = client.get('/v1/transactions/', {'filter[amount.gt]': '0', 'sort': 'id'})
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 6


def test_filter_by_amount_on_wallet(client, wallets3):
    w1, w2, w3 = wallets3
    response = client.get('/v1/transactions/', {'filter[wallet_id]': w1.pk, 'filter[amount.gte]': '10', 'sort': 'id'})
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 2

    response = client.get('/v1/transactions/', {'filter[wallet_id]': w1.pk, 'filter[amount.gt]': '10', 'sort': 'id'})
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 1

    response = client.get('/v1/transactions/', {'filter[wallet_id]': w3.pk, 'filter[amount.gt]': '-100', 'sort': 'id'})
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 4
    assert {item['attributes']['amount'] for item in data} == {'-30.000000000000000000',
                                                               '-60.000000000000000000',
                                                               '-90.000000000000000000',
                                                               '500.000000000000000000'}
