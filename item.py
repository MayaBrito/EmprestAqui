
import json
from collections import Counter
from comment import Comment

class Item:
    def __init__(self,
            item_id: int,
            name: str,
            owner_id: int,
            price: int,
            desc: str = None,
            photo: str = None,
            available: bool = True,
            comments:dict[int, Comment]|None = None):
        self.id = item_id
        self.price = price
        self.name = name
        self.desc = desc
        self.term_frequencies = Counter()
        self.photo = photo
        self.available = available
        self.owner_id = owner_id
        self.comments: dict[int, Comment] = comments
        if comments == None:
            self.comments: dict[int, Comment] = {}
    
    def show(self):
        print(dir(self))
        
    def general_score(self)-> str:
        """get para a nota do item"""
        total = sum([c.score for c in self.comments.values()])
        ammount = len(self.comments)
        score = 0
        if (ammount != 0):
            score = total/ammount
        half_star = (2*score)%2
        score = int(score)
        rest = 5 - (int(score+half_star))
        return "★"*int(score) + "⋆"*int(half_star)+"☆"*int(rest)

    def get_avg_score(self) -> float:
        comment_count: float = float(len(self.comments))
        total_score: float = 0.0
        for c in self.comments.values():
            total_score += c.score
        if comment_count == 0.0 :
            return 2.5
        return total_score/comment_count

    def get_full_text(self) -> str:
        return self.name + ' ' + self.desc

    def add_comment(self, p, c: Comment) -> None:
        self.comments[p.name] = c
    
    def to_dict(self) -> dict[str, any]:
        """parse object to dict"""
        return {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "photo": self.photo,
            "available": self.available,
            "owner_id": self.owner_id,
            "comments": [c.to_dict() for c in self.comments.values()],
        }
  
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