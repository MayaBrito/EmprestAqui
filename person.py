from comment import Comment
from item import Item
from request import Request

class Person:
    _comments:dict[str,Comment] = {}
    _itens:dict[str,Item] = {}
    _requests_made:dict[int,Request] = {}
    _received_requests:dict[(str,int),Request] = {} #item_id,interessado_id
    def __init__(self,name:str,desc:str,phone:str,password:str):
        self._name = name
        self._desc = desc
        self._phone = phone
        #TODO telefone
        #TODO email
        self._password = password
        self._requests_made = {}
        self._received_requests = {}
        self._comments = {}
        self._itens = {}
    
    @property
    def requests_made(self)->dict[int,Request]:
        """get para os requests feitos"""
        return self._requests_made
    
    @property
    def received_requests(self)->dict[(int,str),Request]:
        """get para os requests recebidos"""
        return self._received_requests
    
    @property
    def itens(self)->dict[int,str]:
        """get para os requests recebidos"""
        #print(self._itens)
        return self._itens

    @property
    def password(self)-> str:
        """get para a password da person"""
        return self._password

    @property
    def name(self)-> str:
        """get para o name da person"""
        return self._name
    
    @property
    def desc(self)-> str:
        """get para os description da person"""
        return self._desc
    
    @property
    def phone(self)-> str:
        """get para os phone da person"""
        return self._phone

    @property
    def comments(self)->dict[Comment]:
        """get para os comments da person em itens"""
        return self._comments

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
