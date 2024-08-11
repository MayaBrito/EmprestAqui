from comentario import Comentario
from item import Item
from pessoa import Pessoa
import csv

def read_csv(file_name:str)->dict[str,str]:
    conteudo:dict[str,str] = {}

    with open(file_name, mode ='r')as file:
        arquivo = csv.reader(file)
        cabecalho = next(arquivo)
        for coluna in cabecalho:
            conteudo[coluna]:list = []
        for linha in arquivo:
            for indice,coluna in enumerate(linha):
                conteudo[cabecalho[indice]]:str = coluna
    
    return conteudo
