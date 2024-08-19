from comment import Comment
from item import Item
from person import Person
import csv

def read_csv(file_name:str)->dict[str,str]:
    content:dict[str,str] = {}

    with open(file_name, mode ='r')as file:
        file = csv.reader(file)
        header = next(file)
        for column in header:
            content[column]:list = []
        for row in file:
            for indice,column in enumerate(row):
                content[header[indice]]:str = column
    
    return content
