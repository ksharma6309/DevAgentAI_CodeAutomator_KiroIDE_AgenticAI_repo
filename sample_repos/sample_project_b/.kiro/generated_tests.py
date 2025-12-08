import pytest
from service_client import get_company_name

class DummyResp:
    def __init__(self, json_data):
        self._json = json_data
    def raise_for_status(self):
        return None
    def json(self):
        return self._json


def fake_get(url):
    return DummyResp({
        "id": 1,
        "company": {"name": "Example Corp"}
    })


def test_get_company_name(monkeypatch):
    monkeypatch.setattr('service_client.requests.get', lambda url: fake_get(url))
    assert get_company_name(1) == "Example Corp"
