import pytest
from item import Item
from comment import Comment

def test_item_initialization():

    item_id = 1
    name = "Bike"
    owner_id = 101
    description = "Mountain bike"
    photo_url = "http://example.com/photo.jpg"
    available = True
    comments = {
        1: Comment(1, "Ótimo produto", 5.0),
        2: Comment(2, "Muito bom", 4.0)
    }

    item = Item(item_id, name, owner_id, description, photo_url, available, comments)

    assert item.id == item_id
    assert item.name == name
    assert item.owner_id == owner_id
    assert item.desc == description
    assert item.photo == photo_url
    assert item.available == available
    assert item.comments == comments

def test_item_general_score():
    comments = {
        1: Comment(1, "Ótimo produto", 4.5),
        2: Comment(2, "Muito bom", 4.0)
    }
    item = Item(1, "Bike", 101, "Mountain bike", comments=comments)

    expected_score_representation = "★★★★☆"

    assert item.general_score == expected_score_representation

def test_item_to_dict():

    comments = {
        1: Comment(1, "Ótimo produto", 5.0),
        2: Comment(2, "Muito bom", 4.0)
    }
    item = Item(1, "Bike", 101, "Mountain bike", "http://example.com/photo.jpg", True, comments)

    expected_dict = {
        "id": 1,
        "name": "Bike",
        "desc": "Mountain bike",
        "photo": "http://example.com/photo.jpg",
        "available": True,
        "owner_id": 101,
        "comments": [
            {"id": 1, "comment": "Ótimo produto", "score": 5.0},
            {"id": 2, "comment": "Muito bom", "score": 4.0}
        ]
    }
    assert item.to_dict() == expected_dict

