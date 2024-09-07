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
	
	#TODO pass filters
	def search(self, query: str) -> list:
		return self.index.search(query)
	
	

