class Comment:
    def __init__(self,comment:str,score:str):
        self._comment = comment
        self._score = score
    
    @property
    def comment(self)->str:
        """get para o corpo do comment"""
        return self._comment
    
    @property
    def score(self)->float:
        """get para a avaliacao do comment"""
        return self._score