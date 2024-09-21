from Index import Index

from item import Item

class SearchEngine():
    
	def __init__(self,items:list[Item]):
		index = Index()
		#TODO pass item list
		index.generate_index(items)
		self.index = index

	def index_item(self, item: Item):
		self.index.index_item(item)
	

	def search(self, query: str, filterByAverage=False, disponibilidade=False) -> list: #se tiver com disponibilidade false, pode ter tanto item disponivel quanto indisponivel.
		return self.index.search(query, filterByAverage, disponibilidade)
	
	

