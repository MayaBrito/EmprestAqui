from comentario import Comentario
import json;


class Item:
    _comentarios: dict[int, Comentario] = {}

    def __init__(self, id: int, nome: str, dono_id: int, preco: float = None, desc: str = None, foto: str = None, disponivel: bool = True):
        self._id = id
        self._nome = nome
        self._preco = preco
        self._desc = desc
        self._foto = foto
        self._disponivel = disponivel
        self._dono_id = dono_id
        self._comentarios = {}
        
    def __init__(self, id: int, nome: str, dono_id: int, preco: float = None, desc: str = None, foto: str = None, disponivel: bool = True, commentaries: list = []):
        self._id = id
        self._nome = nome
        self._preco = preco
        self._desc = desc
        self._foto = foto
        self._disponivel = disponivel
        self._dono_id = dono_id
        self._comentarios = commentaries

    @property
    def id(self) -> int:
        """get para o id do item"""
        return self._id

    @property
    def dono_id(self) -> int:
        """get para o id do dono"""
        return self._dono_id

    @property
    def nome(self) -> str:
        """get para o nome do item"""
        return self._nome

    @property
    def preco(self) -> str:
        """get para o preco do item"""
        return self._preco

    @property
    def descricao(self) -> str:
        """get para a descricao do item"""
        return self._desc

    @property
    def foto(self) -> str:
        """get para a foto do item"""
        return self._foto

    @property
    def comentarios(self) -> dict[str, Comentario]:
        """get para os comentarios do item"""
        return self._comentarios

    @property
    def disponivel(self) -> bool:
        """get para a disponibilidade do item"""
        return self._disponivel
    
    @property
    def get_full_text(self) -> str:
        return self.nome + self.descricao

    @disponivel.setter
    def disponivel(self, valor: bool):
        """set para a disponibilidade do item"""
        self._disponivel = valor

    @classmethod
    def get_nota_media(self) -> float:
        numero_comentarios: float = float(len(self._comentarios))
        total_notas: float = 0.0
        for comentario in self._comentarios.values():
            total_notas += comentario.get_nota()
        return total_notas/numero_comentarios

    @classmethod
    def adiciona_comentario(self, pessoa, comentario: Comentario) -> None:
        self._comentarios[pessoa.nome] = comentario

    def to_dict(self) -> dict[any, any]:
        return {
            "id": self._id,
            "nome": self._nome,
            "preco": self._preco,
            "desc": self._desc,
            "foto": self._foto,
            "disponivel": self._disponivel,
            "dono_id": self._dono_id,
            "comentarios": [c.to_dict() for c in self._comentarios.values()],
        }
        
    @classmethod
    def json_to_items_array(self, filepath) -> list:
        with open(filepath, 'r') as f:
            json_dict = json.loads(f.read())
        items_dict = {}
        
        for key in json_dict:
            item = json_dict[key]
            formated_item = Item(item['id'], item['nome'], item['dono_id'], item['preco'], item['desc'], item['foto'], item['disponivel'], item['comentarios'])
            items_dict.update({item['id']: formated_item})

        print(items_dict)
        return items_dict