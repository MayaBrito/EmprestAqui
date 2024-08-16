from comment import Comment
from item import Item
from request import Request

class Person:
    _received_comments:dict[int,Comment] = {}
    _itens:dict[int,Item] = {}
    _requests_made:dict[int,Request] = {}
    _received_requests:dict[(int,int),Request] = {} #item_id,interessado_id
    def __init__(self,person_id:int, name:str, password:str,phone:str,email:str,city:str):
        self._id = person_id
        self._name = name
        self._password = password
        self._phone = phone
        self._email = email
        self._city = city
        self._requests_made = {}
        self._received_requests = {}
        self._received_comments = {}
        self._itens = {}
    
    @property
    def requests_made(self)->dict[int,Request]:
        """get para os requests feitos"""
        return self._requests_made
    
    @property
    def received_requests(self)->dict[(int,int),Request]:
        """get para os requests recebidos"""
        return self._received_requests
    
    @property
    def received_comments(self)->dict[int,Comment]:
        """get para as avaliações da pessoa"""
        return self._received_comments
    
    @property
    def itens(self)->dict[int,str]:
        """get para os itens da pessoa"""
        return self._itens

    @property
    def password(self)-> str:
        """get para a senha da pessoa"""
        return self._password

    @property
    def name(self)-> str:
        """get para o nome da pessoa"""
        return self._name
    
    @property
    def id(self)->int:
        """get para o id da pessoa"""
        return self._id
    
    @property
    def city(self)->str:
        return self._city
    
    @property
    def phone(self)-> str:
        """get para o numero da pessoa"""
        return self._phone
    
    @property
    def email(self)-> str:
        """get para o email da pessoa"""
        return self._email
    
    @property
    def general_score(self)-> str:
        """get para a nota media da pessoa"""
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
