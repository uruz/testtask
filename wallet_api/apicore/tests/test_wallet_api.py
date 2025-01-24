import pytest

pytestmark = pytest.mark.django_db
from wallet_api.apicore.models import Wallet


def test_wallet_endpoint(client, default_wallet):
    response = client.get('/v1/wallets/')
    assert Wallet.objects.count() == 1
    assert response.status_code == 200
    data = response.json()
    assert data.keys() == {'links', 'data', 'meta'}
    obj_list = data['data']
    assert obj_list == [
        {'type': 'Wallet', 'id': str(default_wallet.id),
         'attributes': {'label': 'Test wallet', 'balance': '100.000000000000000000'}}
    ]


def test_single_wallet_endpoint(client, default_wallet):
    response = client.get(f'/v1/wallets/{default_wallet.id}/')
    assert Wallet.objects.count() == 1
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {'data'}
    assert data['data'] == {'type': 'Wallet', 'id': str(default_wallet.id),
                            'attributes': {'label': 'Test wallet', 'balance': '100.000000000000000000'}}


def test_pagination(client, wallets20):
    response = client.get('/v1/wallets/', {'sort': 'id'})
    assert Wallet.objects.count() == 20
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {'links', 'data', 'meta'}
    obj_list = data['data']
    assert len(obj_list) == 10


def test_sorting(client, wallets20):
    response = client.get('/v1/wallets/', {'sort': '-id'})
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 10
    ids = [item['id'] for item in data]
    assert ids == list(sorted(ids, reverse=True))
