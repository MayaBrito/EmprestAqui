import json
import os
from comment import Comment
from item import Item
from person import Person
from request import Request
from Search_Engine import SearchEngine
from forms import Location
from flask import Flask, render_template, request, redirect, make_response,url_for,send_file, session, jsonify
import pickle as pk

import threading
import time
import shutil

import re

BACKUP_COUNTER = -1
BACKUP_DIR = "backup_"
DATA_DIR = "data"
PHOTOS_DIR = "photos"

app = Flask(__name__)
emailsearch = {}
users = {}
itens = {}

# helper function for saving item
def save_item(name,owner_id,desc,photo,available) -> int:
    item_id = len(itens)
    item_instance = Item(item_id,name,owner_id,desc,photo,available)
    itens[item_instance.id] = item_instance
    users[item_instance.owner_id].itens[item_instance.id] = item_instance
    return item_id

# helper fuction for saving user
def save_user(name,password,phone,email,city) -> int:
    user_id = len(users)
    new_user = Person(user_id,name,password,phone,email,city)
    users[user_id] = new_user
    emailsearch[email] = user_id
    return user_id

# helper function to create comments
def save_comment(receiver_type,comment,score,commenter,receiver):
    if receiver_type == "item":
        comment_id = len(itens[receiver].comments)
        new_comment = Comment(comment_id,comment,score)
        itens[receiver].comments[commenter] = new_comment
        return comment_id
    if receiver_type == "user":
        comment_id = len(users[receiver].received_comments)
        new_comment = Comment(comment_id,comment,score)
        users[receiver].received_comments[commenter] = new_comment
        return comment_id

# helper function for creating a request object and applying it to users
def save_request(item_id,interested_id,supplier_id,state='open'):
    new_request = Request(None,'open',item_id,interested_id,supplier_id)
    users[supplier_id].requests_received[(item_id,interested_id)] = new_request
    users[interested_id].requests_made[item_id] = new_request

# simple user validation implement saver metods if made into a comercial product
def check_user() ->tuple[str,bool]:
    email = request.cookies.get("email")
    password = request.cookies.get("password")
    err = False
    if not validate_password(email,password):
        err = True
    return email, err

# TODO remove if unused
# def verify_information(attributes:list):
#     verified = True
#     for attribute in attributes:
#         if len(attribute) == 0:
#             verified = False
#     return verified

# simple password checking implement at least hashing if made into a comercial product
def validate_password(email,password) ->bool:
    null = (email == None or password == None)
    real_account = email in emailsearch.keys()
    if null:
        return False
    if not real_account:
        return False 
    user_to_validate = users[emailsearch[email]]
    user_password = user_to_validate.password
    is_valid_password =  user_password == password
    return is_valid_password

# verify if the email format is valid 
def verify_email(possible_email) ->bool:
    invalid = set("\"(),:;<>[\\]")
    if len(possible_email) <= 3:
        return False
    if not invalid.isdisjoint(set(possible_email)):
        return False
    if ".." in possible_email:
        return False
    if possible_email.count("@") != 1:
        return False
    return True
    
@app.route('/create_user',methods=["POST"])
def create_user():
    name = request.form["name"]
    password = request.form["password"]
    phone = request.form["phone"]
    email = request.form["email"]
    city = request.form["city"]
    new_id = save_user(name,password,phone,email,city)
    return jsonify(error="",id=new_id)

@app.route('/create_comemnt',methods=["POST"])
def create_user():
    user = request.form["email"]
    instance_id = int(request.form["id"])
    instance_type = request.form["type"]
    new_score = request.form["score"]
    new_comment = request.form["comment"]
    save_comment(new_comment,new_score,user.id,instance_id,instance_type)
    return jsonify(error="")

@app.route('/create_request',methods=["POST"])
def create_user():
    user = request.form["email"]
    item_id = int(request.form["id"])
    instance_type = request.form["type"]
    new_score = request.form["score"]
    new_comment = request.form["comment"]
    save_comment(new_comment,new_score,user.id,instance_id,instance_type)
    return jsonify(error="")

@app.route('/search',methods=["GET"])
def search():
    text_search = request.args["text_search"]
    filter_location = request.args["filter_location"]
    filter_review = request.args["filter_review"]
    filter_avaliability = request.args["filter_avaliability"]
    results = engine.search(text_search, filter_location, users, filter_review, filter_avaliability)
    return jsonify(results)

@app.route('/item/id',methods=["GET"])
def item(id):
    email = request.args["email"]
    if id not in itens.keys():
        return jsonify(""),400
    else:
        item = itens[id]
        is_owner = users[emailsearch[email]].id == item.owner_id
        return jsonify(item=item,owner=is_owner)