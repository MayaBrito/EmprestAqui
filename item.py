
import json;
from collections import Counter
from comment import Comment

class Item:
    def __init__(
            self,
            item_id: int,
            name: str,
            owner_id: int,
            desc: str = None,
            photo: str = None,
            available: bool = True,
            comments:dict[int, Comment]|None = None):
        self._id = item_id
        self._name = name
        self._desc = desc
        self.term_frequencies = Counter()
        self._photo = photo
        self._available = available
        self._owner_id = owner_id
        self._comments: dict[int, Comment] = comments
        if comments == None:
            self._comments: dict[int, Comment] = {}
    
    @property
    def id(self) -> int:
        """get item id"""
        return self._id

    @property
    def owner_id(self) -> int:
        """get owner id"""
        return self._owner_id

    @property
    def name(self) -> str:
        """get item name"""
        return self._name

    @property
    def general_score(self)-> str:
        """get para o preco do item"""
        total = sum([c.score for c in self._comments.values()])
        ammount = len(self._comments)
        score = 0
        if (ammount != 0):
            score = total/ammount
        half_star = (2*score)%2
        score = int(score)
        rest = 5 - (int(score+half_star))
        return "★"*int(score) + "⋆"*int(half_star)+"☆"*int(rest)

    @property
    def desc(self) -> str:
        """get item description"""
        return self._desc

    @property
    def photo(self) -> str:
        """get item photo"""
        return self._photo

    @property
    def comments(self) -> dict[int, Comment]:
        """get item comments"""
        return self._comments

    @property
    def available(self) -> bool:
        """get item availability"""
        return self._available

    @available.setter
    def available(self, value: bool):
        """set item availability"""
        self._available = value

    @classmethod
    def get_avg_score(self) -> float:
        comment_count: float = float(len(self.comments))
        total_score: float = 0.0
        for c in self.comments.values():
            total_score += c.score
        return total_score/comment_count

    def get_full_text(self) -> str:
        return self._name + ' ' + self._desc
    
    @classmethod
    def add_comment(self, p, c: Comment) -> None:
        self._comments[p.name] = c
    
    def to_dict(self) -> dict[str, any]:
        """parse object to dict"""
        return {
            "id": self._id,
            "name": self._name,
            "desc": self._desc,
            "photo": self._photo,
            "available": self._available,
            "owner_id": self._owner_id,
            "comments": [c.to_dict() for c in self._comments.values()],
        }

    @classmethod    
    def json_to_items_array(self, filepath) -> list:
        with open(filepath, 'r') as f:
            json_dict = json.loads(f.read())
        items_dict = {}
        
        for key in json_dict:
            item = json_dict[key]
            formated_item = Item(item['id'], item['name'], item['owner_id'], item['desc'], item['photo'], item['available'], item['comments'])
            items_dict.update({item['id']: formated_item})
        
        return items_dict
    
    def term_frequency(self, term):
        return self.term_frequencies.get(term)