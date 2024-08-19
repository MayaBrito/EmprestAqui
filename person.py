from comment import Comment
from item import Item
from request import Request


class Person:
    def __init__(self, id: int, name: str, password: str, phone: str, email: str, city: str):
        self._id = id
        self._name = name
        self._password = password
        self._phone = phone
        self._email = email
        self._city = city
        self._received_comments: dict[int, Comment] = {}
        self._items: dict[int, Item] = {}
        self._requests_made: dict[int, Request] = {}
        # item_id, interested_id
        self._requests_received: dict[(int, int), Request] = {}

    @property
    def requests_made(self) -> dict[int, Request]:
        """get requests made"""
        return self._requests_made

    @property
    def requests_received(self) -> dict[(int, int), Request]:
        """get received requests"""
        return self._requests_received

    @property
    def received_comments(self) -> dict[int, Comment]:
        """get received comments"""
        return self._received_comments

    @property
    def items(self) -> dict[int, str]:
        """get items"""
        return self._items

    @property
    def password(self) -> str:
        """get password"""
        return self._password

    @property
    def name(self) -> str:
        """get name"""
        return self._name

    @property
    def id(self) -> int:
        """get id"""
        return self._id

    @property
    def city(self) -> str:
        """get city"""
        return self._city

    @city.setter
    def city(self, value: str):
        """set city"""
        self._city = value

    @property
    def phone(self) -> str:
        """get phone"""
        return self._phone

    @property
    def email(self) -> str:
        """get email"""
        return self._email

    @property
    def general_score(self) -> str:
        """get score"""
        return sum([c.score for c in self._received_comments.values()])

    # @classmethod
    # def publica_comment(self,item:Item,comment:Comment)->None:
    #     self._comments[item.id] = comment

    # @classmethod
    # def publica_item(self,item:Item)->None:
    #     #print(self._itens)
    #     self._itens[item.id] = item

    # @classmethod
    # def validate_password(self,senha_proposta)->bool:
    #     print(senha_proposta,self._password)
    #     return senha_proposta == self._password

    def to_dict(self) -> dict[any, any]:
        """parses object to dict"""
        return {
            "id": self._id,
            "name": self._name,
            "password": self._password,
            "phone": self._phone,
            "email": self.email,
            "city": self.city,
            "requests_made": [x.to_dict() for x in self._requests_made.values()],
            "requests_received": [x.to_dict() for x in self._requests_received.values()],
            "comments_received": [x.to_dict() for x in self._received_comments.values()],
            "items": [x.to_dict() for x in self._items.values()],
        }
