from EmprestAqui.item import Item
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer
from collections import Counter

from EmprestAqui.item import Item
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

class Index():
    def __init__(self):
        self.index = {} # {"abraco": set(6,3,2)}
        self.items = {} # {4: Item}
        
        
    def index_document(self, item: Item):
        for token in self.generate_tokens(Item.fulltext()):
                if token not in self.index:
                        self.index[token] = set()
                self.index[token].add(item.id)

    def stemme_words(self,tokens):
        stemmer = PorterStemmer()
        return [stemmer.stem(token) for token in tokens]

    def generate_tokens_for_item(self, item_fulltext: str) -> list:
        tokens = []
        tokenize_setences = sent_tokenize(item_fulltext)
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
        stemmed_words = self.stemme_words(tokens_without_stop_words)

        for token in stemmed_words:
            tokens.append(token)
        return tokens
    
    def generate_index(self, file_path:str):
        list_items = Item.json_to_items_array(file_path)
        for item in list_items:
            self.index_document(item)
        #TODO salvar em arquivo.
        
    