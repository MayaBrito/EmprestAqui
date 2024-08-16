from comment import Comment

class Item:
    _comments:dict[str,Comment] = {}
    def __init__(self,item_id:int,name:str,owner_id:str,desc:str=None,photo:str=None,available:bool=True):
        self._id = item_id
        self._name = name
        self._desc = desc
        self._photo = photo
        self._disponivel = available
        self._owner_id = owner_id
        self._comments = {}
    
    @property
    def id(self)->int:
        """get para o id do item"""
        return self._id
    
    @property
    def owner_id(self)->str:
        """get para o id do dono"""
        return self._owner_id

    @property
    def name(self)-> str:
        """get para o name do item"""
        return self._name
    
    @property
    def general_score(self)-> str:
        """get para o preco do item"""
        return sum([c.score for c in self._comments.values()])
    
    @property
    def desc(self)-> str:
        """get para a desc do item"""
        return self._desc
    
    @property
    def photo(self)->str:
        """get para a photo do item"""
        return self._photo

    @property
    def comments(self)->dict[str,Comment]:
        """get para os comments do item"""
        return self._comments

    @property
    def available(self)->bool:
        """get para a disponibilidade do item"""
        return self._disponivel
    
    @available.setter
    def available(self,value:bool):
        """set para a disponibilidade do item"""
        self._disponivel = value

    @classmethod
    def get_nota_media(self)->float:
        numero_comments:float = float(len(self._comments))
        total_score:float = 0.0
        for comment in self._comments.values():
            total_score += comment.get_nota()
        return total_score/numero_comments
    
    @classmethod
    def adiciona_comment(self,person,comment:Comment)->None:
        self._comments[person.name] = comment
