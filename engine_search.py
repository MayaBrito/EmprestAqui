from item import Item

class Engine:
    def __init__(self,itens:list[Item]=[]):
        self.itens = itens

    def search(self,parametro:str,filter:list)->list[Item]:
        results = []
        for item in self.itens:
            if parametro.lower() in item.name.lower():
                results.append(item)
        return results

    def adicionar_item(self,item):
        self.itens.append(item)