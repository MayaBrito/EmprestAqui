class Pedido:
    def __init__(self,estado:str,item:str,interessado:str,interessado_contato:str=None,fornecedor_contato:str=None):
        self._estado = estado
        self._item = item
        self._interessado = interessado
        self._interessado_contato = interessado_contato
        self._fornecedor_contato = fornecedor_contato
    
    @property
    def estado(self)-> str:
        """get para o estado do pedido"""
        return self._estado
    
    @property
    def interessado(self)-> str:
        """get para o interessado no pedido"""
        return self._interessado
    
    @property
    def interessado_contato(self)-> str:
        """get para o interessado no pedido"""
        return self._interessado_contato
    
    @property
    def fornecedor_contato(self)-> str:
        """get para o fornecedor no pedido"""
        return self._fornecedor_contato
    
    @property
    def item(self)-> str:
        """get para o id do item"""
        return self._item
    
    @estado.setter
    def estado(self,valor:str)-> str:
        """set para o estado do pedido"""
        self._estado = valor
