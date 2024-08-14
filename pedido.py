class Pedido:
    def __init__(self, estado: str, item: int, interessado: int, interessado_contato: str = None, fornecedor_contato: str = None, id: int = 0):
        self._id = id
        self._estado = estado
        self._item = item
        self._interessado = interessado
        self._interessado_contato = interessado_contato
        self._fornecedor_contato = fornecedor_contato

    @property
    def id(self) -> str:
        """get para o id do pedido"""
        return self._id

    @property
    def estado(self) -> str:
        """get para o estado do pedido"""
        return self._estado

    @property
    def interessado(self) -> int:
        """get para o interessado no pedido"""
        return self._interessado

    @property
    def interessado_contato(self) -> str:
        """get para o interessado no pedido"""
        return self._interessado_contato

    @property
    def fornecedor_contato(self) -> str:
        """get para o fornecedor no pedido"""
        return self._fornecedor_contato

    @property
    def item(self) -> int:
        """get para o id do item"""
        return self._item

    @estado.setter
    def estado(self, valor: str) -> str:
        """set para o estado do pedido"""
        self._estado = valor

    def to_dict(self) -> dict[any, any]:
        return {
            "id": self._id,
            "estado": self._estado,
            "item": self._item,
            "interessado": self._interessado,
            "interessado_contato": self._interessado_contato,
            "fornecedor_contato": self._fornecedor_contato,
        }
