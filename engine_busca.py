from item import Item
class Engine:
    def __init__(self,itens:list[Item]=[]):
        self.itens = itens

    def buscar(self,parametro:str,filtro:list)->list[Item]:
        resultados = []
        for item in self.itens:
            if parametro.lower() in item.nome.lower():
                resultados.append(item)
        return resultados

    def adicionar_item(self,item):
        self.itens.append(item)