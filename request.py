class Request:
    def __init__(self,state:str,item_id:int,interested:int,supplier:int):
        self._state = state
        self._item_id = item_id
        self._interested = interested
        self._supplier = supplier
    
    @property
    def state(self)-> str:
        """get para o state do request"""
        return self._state
    
    @property
    def interested(self)-> str:
        """get para o interested no request"""
        return self._interested
    
    @property
    def supplier(self)-> str:
        """get para o interested no request"""
        return self._supplier
    
    @property
    def item_id(self)-> int:
        """get para o id do item"""
        return self._item_id
    
    @state.setter
    def state(self,value:str)-> str:
        """set para o state do request"""
        self._state = value
