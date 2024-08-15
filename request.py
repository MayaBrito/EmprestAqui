class Request:
    def __init__(self,state:str,item:str,interested:str,interested_contact:str=None,supplier_contact:str=None):
        self._state = state
        self._item = item
        self._interested = interested
        self._interested_contact = interested_contact
        self._supplier_contact = supplier_contact
    
    @property
    def state(self)-> str:
        """get para o state do request"""
        return self._state
    
    @property
    def interested(self)-> str:
        """get para o interested no request"""
        return self._interested
    
    @property
    def interested_contact(self)-> str:
        """get para o interested no request"""
        return self._interested_contact
    
    @property
    def supplier_contact(self)-> str:
        """get para o fornecedor no request"""
        return self._supplier_contact
    
    @property
    def item(self)-> str:
        """get para o id do item"""
        return self._item
    
    @state.setter
    def state(self,value:str)-> str:
        """set para o state do request"""
        self._state = value
