from Index import Index

from item import Item

class SearchEngine():
    
	def __init__(self):
		index = Index()
		index.generate_index('items.json')
		self.index = index

	def index_item(self, item: Item):
		self.index.index_item(item)

	def search(self, query: str) -> list:
		return self.index.search(query)
	
	

