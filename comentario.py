class Comentario:
    def __init__(self, comentatio: str, nota: str, id: int = 0, foto: str = None):
        self._comentario = comentatio
        self._nota = nota
        self._id = id

    @property
    def comentario(self) -> str:
        """get para o corpo do comentario"""
        return self._comentario

    @property
    def nota(self) -> float:
        """get para a avaliacao do comentario"""
        return self._nota

    def to_dict(self) -> dict[any, any]:
        return {
            "id": self._id,
            "comentario": self._comentario,
            "nota": self._nota
        }
