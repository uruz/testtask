import pytest


def test_endpoint(client):
    response = client.get('/ping/')
    assert response.status_code == 200
    assert response.content == b'200 OK!'
