import json

# from uuid import uuid4

# import pytest


async def test_search_by_link(client, get_user_from_database):
    user_data = {"URL": "URL1", "page": 1}
    resp = client.post("/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["URL"] == user_data["URL"]
    assert data_from_resp["page"] == user_data["page"]
