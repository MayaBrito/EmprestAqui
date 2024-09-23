import pytest
from person import Person
from item import Item
from comment import Comment
from request import Request

def test_person_initialization():
    person_id = 1
    name = "John Doe"
    password = "password123"
    phone = "123-456-7890"
    email = "johndoe@example.com"
    city = "Campina Grande"

    person = Person(person_id, name, password, phone, email, city)

    assert person.id == person_id
    assert person.name == name
    assert person.password == password
    assert person.phone == phone
    assert person.email == email
    assert person.city == city
    assert person.requests_made == {}
    assert person.requests_received == {}
    assert person.received_comments == {}
    assert person.itens == {}

def test_person_general_score():
    person = Person(1, "John Doe", "password123", "123-456-7890", "johndoe@example.com", "Campina Grande")

    person.received_comments[1] = Comment(1, "Ótimo", 4.5)
    person.received_comments[2] = Comment(2, "Bom", 4.0)
    person.received_comments[3] = Comment(3, "Regular", 3.5)

    expected_score_representation = "★★★★☆"

    assert person.general_score == expected_score_representation

def test_person_to_dict():
    person = Person(1, "John Doe", "password123", "123-456-7890", "johndoe@example.com", "Campina Grande")
    
    item = Item(1, "Bike", 1)
    person.itens[1] = item
    
    comment = Comment(1, "Ótimo", 4.5)
    person.received_comments[1] = comment

    request_made = Request(1, "open", 1, 1, 2)
    person.requests_made[1] = request_made

    request_received = Request(2, "pending", 1, 3, 1)
    person.requests_received[(1, 3)] = request_received

    expected_dict = {
        "id": 1,
        "name": "John Doe",
        "password": "password123",
        "phone": "123-456-7890",
        "email": "johndoe@example.com",
        "city": "Campina Grande",
        "requests_made": [request_made.to_dict()],
        "requests_received": [request_received.to_dict()],
        "comments_received": [comment.to_dict()],
        "itens": [item.to_dict()],
    }

    assert person.to_dict() == expected_dict

def test_person_set_city():
    person = Person(1, "John Doe", "password123", "123-456-7890", "johndoe@example.com", "Campina Grande")

    new_city = "Los Angeles"
    person.city = new_city

    assert person.city == new_city
