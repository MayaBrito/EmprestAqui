class Comentario:
    def __init__(self,comentatio:str,nota:str,foto:str=None):
        self._comentario = comentatio
        self._nota = nota
    
    @property
    def comentario(self)->str:
        """get para o corpo do comentario"""
        return self._comentario
    
    @property
    def nota(self)->float:
        """get para a avaliacao do comentario"""
        return self._nota