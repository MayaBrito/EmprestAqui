import pytest
from request import Request

def test_request_initialization():

    request_id = 1
    state = "open"
    item_id = 101
    interested_id = 201
    supplier_id = 301

    request = Request(request_id, state, item_id, interested_id, supplier_id)

    assert request._id == request_id
    assert request.state == state
    assert request.item_id == item_id
    assert request.interested_id == interested_id
    assert request.supplier_id == supplier_id

def test_request_state_setter():

    request = Request(1, "open", 101, 201, 301)

    new_state = "accepted"
    request.state = new_state

    assert request.state == new_state

def test_request_to_dict():

    request_id = 2
    state = "rejected"
    item_id = 102
    interested_id = 202
    supplier_id = 302

    request = Request(request_id, state, item_id, interested_id, supplier_id)

    expected_dict = {
        "id": request_id,
        "state": state,
        "item_id": item_id,
        "interested_id": interested_id,
        "supplier_id": supplier_id,
    }
    assert request.to_dict() == expected_dict
