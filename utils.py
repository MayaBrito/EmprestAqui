from comment import Comment
from item import Item
from person import Person
import csv
import json

def read_csv():
# Open and read the JSON file
    with open('people.json', 'r') as p:
        people_json = json.load(p)
    with open('items.json','r') as i:
        item_json = json.load(i)
    with open('comments.json', 'r') as c:
        comment_json = json.load(c)
    with open('requests.json', 'r') as r:
        request_json = json.load(r)
    return people_json, item_json, comment_json, request_json