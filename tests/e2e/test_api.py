from accounts import config
import client

def test_open_account():
    id = config.initialCustomerId()
    res = client.openAccount(id, 10.54)
    assert res.status_code == 201

    res = client.accountDetails(id).json()
    assert res["customerId"] == id
    assert res["firstName"] == "Georgi"
    assert res["lastName"] == "Mateev"
    assert res["balance"] == 10.54

    res2 = client.openAccount(id, 10)
    assert res2.status_code == 201

    res2 = client.accountDetails(id).json()

    assert res2["balance"] == 20.54
    assert len(res2["transactions"]) == 2

def test_not_existing_account():
    res2 = client.accountDetails(id)
    assert res2.status_code == 404

def test_negative_amount():
    id = config.initialCustomerId()
    res = client.openAccount(id, -1)
    assert res.status_code == 400