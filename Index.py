import math
from item import Item
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from collections import Counter
from nltk.stem import RSLPStemmer

nltk.download('stopwords')
nltk.download('rslp')

class Index():
    def __init__(self):
        self.index = {} # {"abraco": set(6,3,2)}
        self.items = {} # {4: Item}
        
    def generate_term_frequencies(self, item: Item):
        tokens = self.generate_tokens(item.get_full_text())
        item.term_frequencies = Counter(tokens)

    def index_item(self, item: Item):
        if item.id not in self.items:
            self.items[item.id] = item
            self.generate_term_frequencies(item)
            
        for token in self.generate_tokens(item.get_full_text()):
                if token not in self.index:
                        self.index[token] = set()
                self.index[token].add(item.id)
    
    def document_frequency(self, token):
        return len(self.index.get(token, set()))

    def inverse_document_frequency(self, token):
        return math.log10(len(self.items) / self.document_frequency(token))
    

    def stem_words_pt(self,tokens):
        stemmer = RSLPStemmer()
        return [stemmer.stem(token) for token in tokens]

    def generate_tokens(self, text: str) -> list:
        tokens = []
        tokenize_setences = sent_tokenize(text)
        tokenizer = RegexpTokenizer(r'\w+')
        list_of_list_tokens_without_punc = []

        #Removendo pontuação das palavras
        for sentence in tokenize_setences:
            sentence_without_punct = tokenizer.tokenize(sentence)
            list_of_list_tokens_without_punc.append(sentence_without_punct)

        stop_words = set(stopwords.words("portuguese"))

        # Obtendo as palavras sem pontuação e convertendo tudo para Lower Case
        tokens_with_stop_words = [token.lower() for list_of_tokens in list_of_list_tokens_without_punc for token in list_of_tokens]
        #Removendo Stop Words
        tokens_without_stop_words = [word for word in tokens_with_stop_words if len(stop_words.intersection({word})) == 0 ]
        #Aplicando Stemmer
        stemmed_words = self.stem_words_pt(tokens_without_stop_words)

        for token in stemmed_words:
            tokens.append(token)
        return tokens
    
    def generate_index(self, items:list[Item]):
        for item in items:
            self.index_item(item)

        
        #TODO salvar em arquivo.
    
    def rank(self, entry_tokens, items):
        results = []
        item_ids = []

        for item in items:
            score = sum([item.term_frequency(token) * self.inverse_document_frequency(token) for token in entry_tokens if item.term_frequency(token) is not None])
            results.append((item, score))

        sorted_results = sorted(results, key=lambda item: item[1], reverse=True)
        for item_id, _ in sorted_results:
            item_ids.append(item_id)
        return item_ids
    
    def _results(self, analyzed_query):
        return [self.index.get(token) for token in analyzed_query if self.index.get(token) is not None]
    
    def search(self, query, filterByAverage, disponibilidade):
        entry_tokens = self.generate_tokens(query)
        results = self._results(entry_tokens)
        if len(results) >= 1:
                items = [self.items[item_id] for item_id in set.union(*results)]
        else:
                items = []

        query_result_items = self.rank(entry_tokens, items)
        if disponibilidade:
            query_result_items = [item for item in query_result_items if item.available]
        if filterByAverage:
            filtered_items = sorted(query_result_items, key=lambda item: item.get_avg_score(), reverse=True)
            return filtered_items
        else:
            return query_result_items