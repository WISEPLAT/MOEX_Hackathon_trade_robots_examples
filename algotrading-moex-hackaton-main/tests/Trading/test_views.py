import pytest
import test_helpers

from django.urls import reverse


pytestmark = [pytest.mark.django_db]


def tests_stock_list_view(client):
    instance1 = test_helpers.create_Trading_stock()
    instance2 = test_helpers.create_Trading_stock()
    url = reverse("Trading_stock_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_stock_create_view(client):
    url = reverse("Trading_stock_create")
    data = {
        "ticker": "text",
        "name": "text",
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_stock_detail_view(client):
    instance = test_helpers.create_Trading_stock()
    url = reverse("Trading_stock_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_stock_update_view(client):
    instance = test_helpers.create_Trading_stock()
    url = reverse("Trading_stock_update", args=[instance.pk, ])
    data = {
        "ticker": "text",
        "name": "text",
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_strategy_list_view(client):
    instance1 = test_helpers.create_Trading_strategy()
    instance2 = test_helpers.create_Trading_strategy()
    url = reverse("Trading_strategy_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_strategy_create_view(client):
    url = reverse("Trading_strategy_create")
    data = {
        "label": "text",
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_strategy_detail_view(client):
    instance = test_helpers.create_Trading_strategy()
    url = reverse("Trading_strategy_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_strategy_update_view(client):
    instance = test_helpers.create_Trading_strategy()
    url = reverse("Trading_strategy_update", args=[instance.pk, ])
    data = {
        "label": "text",
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_trader_list_view(client):
    instance1 = test_helpers.create_Trading_trader()
    instance2 = test_helpers.create_Trading_trader()
    url = reverse("Trading_trader_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_trader_create_view(client):
    url = reverse("Trading_trader_create")
    data = {
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_trader_detail_view(client):
    instance = test_helpers.create_Trading_trader()
    url = reverse("Trading_trader_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_trader_update_view(client):
    instance = test_helpers.create_Trading_trader()
    url = reverse("Trading_trader_update", args=[instance.pk, ])
    data = {
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_trading_history_list_view(client):
    instance1 = test_helpers.create_Trading_trading_history()
    instance2 = test_helpers.create_Trading_trading_history()
    url = reverse("Trading_trading_history_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_trading_history_create_view(client):
    stock = test_helpers.create_Trading_stock()
    url = reverse("Trading_trading_history_create")
    data = {
        "priceUpdateDateTime": datetime.now(),
        "price": 1.0f,
        "stock": stock.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_trading_history_detail_view(client):
    instance = test_helpers.create_Trading_trading_history()
    url = reverse("Trading_trading_history_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_trading_history_update_view(client):
    stock = test_helpers.create_Trading_stock()
    instance = test_helpers.create_Trading_trading_history()
    url = reverse("Trading_trading_history_update", args=[instance.pk, ])
    data = {
        "priceUpdateDateTime": datetime.now(),
        "price": 1.0f,
        "stock": stock.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302
