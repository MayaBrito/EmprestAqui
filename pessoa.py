from comentario import Comentario
from item import Item
from pedido import Pedido

class Pessoa:
    _comentarios:dict[str,Comentario] = {}
    _itens:dict[str,Item] = {}
    _pedidos_feitos:dict[int,Pedido] = {}
    _pedidos_recebidos:dict[(str,int),Pedido] = {} #item_id,interessado_id
    def __init__(self,nome:str,desc:str,contato:str,senha:str):
        self._nome = nome
        self._desc = desc
        self._contato = contato
        #TODO telefone
        #TODO email
        self._senha = senha
        self._pedidos_feitos = {}
        self._pedidos_recebidos = {}
        self._comentarios = {}
        self._itens = {}
    
    @property
    def pedidos_feitos(self)->dict[int,Pedido]:
        """get para os pedidos feitos"""
        return self._pedidos_feitos
    
    @property
    def pedidos_recebidos(self)->dict[(int,str),Pedido]:
        """get para os pedidos recebidos"""
        return self._pedidos_recebidos
    
    @property
    def itens(self)->dict[int,str]:
        """get para os pedidos recebidos"""
        #print(self._itens)
        return self._itens

    @property
    def senha(self)-> str:
        """get para a senha da pessoa"""
        return self._senha

    @property
    def nome(self)-> str:
        """get para o nome da pessoa"""
        return self._nome
    
    @property
    def descricao(self)-> str:
        """get para os descrição da pessoa"""
        return self._desc
    
    @property
    def contato(self)-> str:
        """get para os contato da pessoa"""
        return self._contato

    @property
    def comentarios(self)->dict[Comentario]:
        """get para os comentarios da pessoa em itens"""
        return self._comentarios

    # @classmethod
    # def publica_comentario(self,item:Item,comentario:Comentario)->None:
    #     self._comentarios[item.id] = comentario

    # @classmethod
    # def publica_item(self,item:Item)->None:
    #     #print(self._itens)
    #     self._itens[item.id] = item
    
    # @classmethod
    # def valida_senha(self,senha_proposta)->bool:
    #     print(senha_proposta,self._senha)
    #     return senha_proposta == self._senha
