import json
from random import random, seed
from typing import Callable, Generator
from faker import Faker
import math

from comentario import Comentario
from item import Item
from pedido import Pedido
from pessoa import Pessoa


class DataFakerConfig:
    def __init__(
            self,
            people_n: int = 20,
            requests_n: int = 1000,
            gen_comments_per_person: Generator[int, None, None] = None,
            gen_items_per_person: Generator[int, None, None] = None,
            gen_comments_per_item: Generator[int, None, None] = None,
    ) -> None:
        # Number of people
        self._people_n: int = people_n
        # Number of requests
        self._requests_n: int = requests_n
        # Generates number of comments per person

        def default_comments_per_person() -> Generator[int, None, None]:
            while True:
                yield 20
        self._comments_per_person = gen_comments_per_person(
        ) if gen_comments_per_person else default_comments_per_person()
        # Generates number of items per person

        def default_items_per_person() -> Generator[int, None, None]:
            while True:
                yield 10
        self._items_per_person = gen_items_per_person(
        ) if gen_items_per_person else default_items_per_person()
        # Generates number of comments per item

        def default_comments_per_item() -> Generator[int, None, None]:
            while True:
                yield 30
        self._comments_per_item = gen_comments_per_item(
        ) if gen_comments_per_item else default_comments_per_item()

    @property
    def comments_per_item(self) -> int:
        return next(self._comments_per_item)

    @property
    def comments_per_person(self) -> int:
        return next(self._comments_per_person)

    @property
    def items_per_person(self) -> int:
        return next(self._items_per_person)

    @property
    def requests_n(self) -> int:
        return self._requests_n

    @property
    def people_n(self) -> int:
        return self._people_n


class DataFaker:
    def __init__(self) -> None:
        self._item_id_seq = -1
        self._person_id_seq = -1
        self._comment_id_seq = -1
        self._request_id_seq = -1

        self._people: dict[int, Pessoa] = {}
        self._comments: dict[int, Comentario] = {}
        self._items: dict[int, Item] = {}
        self._requests: dict[int, Pedido] = {}  # Item id, Interested id

    @property
    def people(self) -> dict[int, Pessoa]:
        return self._people

    @property
    def comments(self) -> dict[int, Comentario]:
        return self._comments

    @property
    def items(self) -> dict[int, Item]:
        return self._items

    @property
    def requests(self) -> dict[int, Pedido]:
        return self._requests

    def create_fake_data(self, fk: Faker, cfg: DataFakerConfig):
        # Creating people
        people = self.fake_people(fk, cfg.people_n)

        # Creating comments for people
        for p in people.values():
            for comment in self.fake_comments(fk, cfg.comments_per_person).values():
                other_p_id = p._id
                while other_p_id == p._id:
                    other_p_id = math.ceil(random() * cfg.people_n)

                p._comentarios[other_p_id] = comment

        # Creating items for people
        for p in people.values():
            for item in self.fake_items(fk, cfg.items_per_person).values():
                item._dono_id = p._id
                # Creating fake comments for item
                for c in self.fake_comments(fk, cfg.comments_per_item).values():
                    other_p_id = p._id
                    while other_p_id == p._id:
                        other_p_id = math.ceil(random() * cfg.people_n)

                    item._comentarios[other_p_id] = c

                p._itens[item.id] = item

        # Creating requests for people
        requests = self.fake_requests(fk, cfg.requests_n)
        for req in requests.values():
            interested = self._people[req.interessado]
            owner = self._people[self._items[req.item].dono_id]
            owner._pedidos_recebidos[(req.item, req.interessado)] = req
            interested._pedidos_feitos[req.item] = req

    def _fake_n(self, fk: Faker, n: int, fake_fn: Callable[[Faker], tuple[any, any]]) -> dict[any, any]:
        l = {}

        for _ in range(n):
            v, k = fake_fn(fk)
            l[k] = v

        return l

    def fake_comments(self, fk: Faker, n: int) -> dict[int, Comentario]:
        new_comments = self._fake_n(fk, n, self.fake_comment)
        self._comments.update(new_comments)
        return new_comments

    def fake_comment(self, fk: Faker) -> tuple[Comentario, int]:
        self._comment_id_seq += 1
        return Comentario(fk.text(), fk.random_int(0, 10), self._comment_id_seq), self._comment_id_seq

    def fake_items(self, fk: Faker, n: int = 1) -> dict[int, Item]:
        new_items = self._fake_n(fk, n, self.fake_item)
        self._items.update(new_items)
        return new_items

    def fake_item(self, fk: Faker) -> tuple[Item, int]:
        self._item_id_seq += 1
        r = random()  # Número aleatório entre 0 e 1
        name = fk.text(5)
        price = r * fk.random_int(1, 1000)
        desc = fk.text(200)
        return Item(self._item_id_seq, name, 0, price, desc), self._item_id_seq

    def fake_requests(self, fk: Faker, n: int = 1) -> dict[int, Pedido]:
        new_requests = self._fake_n(fk, n, self.fake_request)
        self._requests.update(new_requests)
        return new_requests

    def fake_request(self, fk: Faker, n: int = 1) -> tuple[Pedido, int]:
        self._request_id_seq += 1
        estado = fk.state()
        item_id = math.ceil(random() * self._item_id_seq)
        item = self._items[item_id]
        owner = self._people[item.dono_id]

        interested_id = item.dono_id
        while interested_id == item.dono_id:
            interested_id = math.ceil(random() * self._person_id_seq)
        interested = self._people[interested_id]

        return Pedido(estado, item_id, interested_id, interested.contato, owner.contato, self._request_id_seq), self._request_id_seq

    def fake_people(self, fk: Faker, n: int = 1) -> dict[int, Pessoa]:
        new_people = self._fake_n(fk, n, self.fake_person)
        self._people.update(new_people)
        return new_people

    def fake_person(self, fk: Faker) -> tuple[Pessoa, int]:
        name = fk.name()
        desc = fk.text(200)
        contact = fk.phone_number()
        password = fk.password()
        self._person_id_seq += 1
        return Pessoa(name, desc, contact, password, self._person_id_seq), self._person_id_seq


if __name__ == "__main__":
    fk = Faker()
    dfk = DataFaker()
    cfg = DataFakerConfig()
    Faker.seed(42)  # Seed for faker
    seed(42)  # Seed for python's random

    dfk.create_fake_data(fk, cfg)
    for resource in ["people", "comments", "items", "requests"]:
        with open(f'{resource}.json', 'w') as f:
            f.write(json.dumps(dfk.__getattribute__(
                resource), default=lambda x: x.to_dict()))
