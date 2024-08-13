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
            gen_comments_per_person: Generator[int, None, None] = None,
            gen_items_per_person: Generator[int, None, None] = None,
            gen_comments_per_item: Generator[int, None, None] = None,
    ) -> None:
        # Number of people
        self._people_n: int = people_n
        # Generates number of comments per person
        def default_comments_per_person() -> Generator[int, None, None]:
            while True:
                yield 20
        self._comments_per_person = gen_comments_per_person() if gen_comments_per_person else default_comments_per_person()
        # Generates number of items per person
        def default_items_per_person() -> Generator[int, None, None]:
            while True:
                yield 10
        self._items_per_person = gen_items_per_person() if gen_items_per_person else default_items_per_person()
        # Generates number of comments per item
        def default_comments_per_item() -> Generator[int, None, None]:
            while True:
                yield 30
        self._comments_per_item = gen_comments_per_item() if gen_comments_per_item else default_comments_per_item()

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
    def people_n(self) -> int:
        return self._people_n


class DataFaker:
    def __init__(self) -> None:
        self._item_id_seq = 0
        self._person_id_seq = 0
        self._people: list[Pessoa] = []
        self._items: list[Item] = []

    @property
    def people(self) -> list[Pessoa]:
        return self._people

    def create_fake_data(self, fk: Faker, cfg: DataFakerConfig):
        # Creating people
        people = self.fake_people(fk, cfg.people_n)

        # Creating comments for people
        for p in people:
            for comment in self.fake_comments(fk, cfg.comments_per_person):
                other_p_id = p._id
                while other_p_id == p._id:
                    other_p_id = math.ceil(random() * cfg.people_n)

                p._comentarios[other_p_id] = comment

        # Creating items for people
        for p in people:
            for item in self.fake_items(fk, cfg.items_per_person):
                item._dono_id = p._id
                # Creating fake comments for item
                for c in self.fake_comments(fk, cfg.comments_per_item):
                    other_p_id = p._id
                    while other_p_id == p._id:
                        other_p_id = math.ceil(random() * cfg.people_n)

                    item._comentarios[other_p_id] = c
                
                p._itens[item.id] = item

        # TODO: Creating requests for people

    def _fake_n(self, fk: Faker, n: int, fake_fn: Callable[[Faker], list[any]]) -> list[any]:
        l = []

        for _ in range(n):
            l.append(fake_fn(fk))

        return l

    def fake_comments(self, fk: Faker, n: int) -> list[Comentario]:
        return self._fake_n(fk, n, self.fake_comment)

    def fake_comment(self, fk: Faker) -> Comentario:
        return Comentario(fk.text(), fk.random_int(0, 10))

    def fake_items(self, fk: Faker, n: int = 1) -> list[Item]:
        self._items = self._fake_n(fk, n, self.fake_item)
        return self._items

    def fake_item(self, fk: Faker) -> Item:
        self._item_id_seq += 1
        r = random()  # Número aleatório entre 0 e 1
        name = fk.text(5)
        price = r * fk.random_int(1, 1000)
        desc = fk.text(200)
        return Item(self._item_id_seq, name, 0, price, desc)

    def fake_requests(self, fk: Faker, n: int = 1) -> Pedido:
        return self._fake_n(fk, n, self.fake_request)

    def fake_request(self, fk: Faker, n: int = 1) -> Pedido:
        estado = fk.estado_nome()
        item_id = math.ceil(random() * self._item_id_seq)
        item = self._items[item_id]
        owner = self._people[item.dono_id]
        interested_id = math.ceil(random() * self._person_id_seq)
        interested = self._people[interested_id]
        return Pedido(estado, item_id, interested_id, interested.contato, owner.contato)

    def fake_people(self, fk: Faker, n: int = 1) -> list[Pessoa]:
        self._people = self._fake_n(fk, n, self.fake_person)
        return self._people

    def fake_person(self, fk: Faker) -> Pessoa:
        name = fk.name()
        desc = fk.text(200)
        contact = fk.phone_number()
        password = fk.password()
        self._person_id_seq += 1
        return Pessoa(name, desc, contact, password, self._person_id_seq)


if __name__ == "__main__":
    fk = Faker()
    dfk = DataFaker()
    cfg = DataFakerConfig()
    Faker.seed(42)  # Seed for faker
    seed(42)  # Seed for python's random

    dfk.create_fake_data(fk, cfg)
    print(dfk.people[0].itens[1]._comentarios)
