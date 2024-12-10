import json
import os
from comment import Comment
from item import Item
from person import Person
from request import Request
from utils import read_csv
from Search_Engine import SearchEngine
from forms import Forms, Location
from flask import Flask, flash, render_template, request, redirect, make_response,url_for,send_file, session
import pickle as pk
from flask import Flask, send_from_directory

import threading
import time
import shutil

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

# helper function for saving cookies
def save_cookies(resp,email,password):
    resp.set_cookie('email', email)
    resp.set_cookie('password',password)
    return resp

# helper function to create comments
def save_comment(comment,score,commenter,receiver,receiver_type):
    if receiver_type == "item":
        comment_id = len(itens[receiver].comments)
        new_comment = Comment(comment_id,comment,score)
        itens[receiver].comments[commenter] = new_comment
    if receiver_type == "user":
        comment_id = len(users[receiver].received_comments)
        new_comment = Comment(comment_id,comment,score)
        users[receiver].received_comments[commenter] = new_comment

# helper function for creating a request object and applyting it to users
def make_request(item_id,interested_id,supplier_id,state='open'):
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

def verify_information(attributes:list):
    verified = True
    for attribute in attributes:
        if len(attribute) == 0:
            verified = False
    return verified

# simple password checking implement at least hashing if made into a comercial product
def validate_password(email,password) ->bool:
    null = (email == None or password == None)
    real_account = email in emailsearch.keys()
    return not null and real_account and (
        users[emailsearch[email]].password == password
        )

@app.route('/photos/<path:filename>')
def serve_photos(filename):
    return send_from_directory('photos', filename)

@app.route('/',methods=['GET','POST'])
def default():
    resp = make_response(redirect(url_for('menu'))) 
    return resp

@app.route('/login',methods=['GET','POST'])
def login():
    resp = make_response(render_template('login-form/login.html'))
    if "exit" in request.form:
        resp.set_cookie('email', "")
        resp.set_cookie('password',"")
    return resp

@app.route('/login_confirmation',methods=['GET','POST'])
def login_confirmation():
    if request.method == 'POST': 
        email = request.form['email']
        password = request.form['password']
        if validate_password(email,password):
            resp = make_response(redirect(url_for('menu'))) 
            resp = save_cookies(resp,email,password)
            return resp
        else:
            output = "Usuario ou Senha Incorretos" 
            resp = render_template('error.html',error=output)
    return resp

@app.route('/register',methods=['GET','POST'])
def register():
    name = request.cookies.get("name")
    if name == None: name = ""
    phone = request.cookies.get('phone')
    if phone == None: phone = ""
    error = request.cookies.get('error')
    if error == None: error = ""
    email = request.cookies.get('email')
    if email == None: email = ""
    location = Location(request.form)
    return render_template('login-form/register.html',location = location,name=name,phone=phone,email=email,error=error)

@app.route('/confirmation', methods = ['GET','POST']) 
def confirmation(): 
    if request.method == 'POST': 
        name = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        email = request.form['email']
        city = request.form['filter']
        verified = verify_information([name,password,phone,email,city])
        resp = make_response(redirect(url_for("register")))
        resp.set_cookie('name',name)
        resp.set_cookie('phone',phone)
        resp.set_cookie('email',email)
        if ("@" not in email or ".com" not in email):
            resp.set_cookie('error',"e-mail invalido")
            return resp
        if ("Todas as localizações" in city):
            resp.set_cookie("error","localização invalida")
            return resp
        if not verified:
            output = "Existem campos não preenchidos" 
            resp = render_template("error.html",error=output)
            return resp
        if email not in emailsearch:
            save_user(name,password,phone,email,city)
            resp = make_response(redirect(url_for('menu')))
            resp = save_cookies(resp,email,password)
            return resp
        else:
            output = "Usuario já registrado com esse email" 
            resp = render_template("error.html",error=output) 
    return resp

@app.route('/menu/<error>',methods=['GET','POST'])
@app.route('/menu',defaults={'error': ""},methods=['GET','POST'])
def menu(error):
    print(error)
    location = Location(request.form)
    return render_template('search-product/index.html', error=error, location=location)


@app.route('/results',methods=['GET', 'POST'])
def results():
    results = []
    text_search = request.form['search']
    filter_location = request.form['filter']
    if 'avaliability' in request.form:
        filter_avaliability = request.form['avaliability']
    else :
        filter_avaliability = None

    if 'review' in request.form:
        filter_review = request.form['review']
    else :
        filter_review = None

    results = engine.search(text_search, filter_location, users, filter_review, filter_avaliability)
    location = Location(request.form)

    if len(results) == 0:
        #flash('sem results, tente novamente!') 
        return redirect(url_for('menu',error="sem resultados"))
    else:
        return render_template('search-product/results.html', results=results, location = location, search = text_search)

@app.route('/item')
def item():
    item_id = int(request.args['id'])
    if item_id not in itens.keys():
        output = "non-existent item" 
        resp = render_template("error.html",error=output)
        return resp
    else:
        item = itens[item_id]
        email, err = check_user()
        is_owner = False 
        if not err:
            is_owner = users[emailsearch[email]].id == item.owner_id
        return render_template('item/item.html',item=item,comments=item.comments,owner=users[item.owner_id],users=users,is_owner=is_owner)

@app.route('/comment',methods=['GET','POST'])
def comment():
    email, err = check_user()
    if err:
        return render_template('login-form/login.html')
    user = users[emailsearch[email]]
    instance_id = request.form['id']
    instance_type = request.form['type']
    return render_template('user/comment.html',instance_id=instance_id,instance_type=instance_type)

@app.route('/apply_comment',methods=['GET','POST'])
def apply_comment():
    email, err = check_user()
    if err:
        return render_template('login-form/login.html')
    user = users[emailsearch[email]]
    instance_id = int(request.form["id"])
    instance_type = request.form["type"]
    new_score = int(request.form["score"])
    new_comment = request.form["comment"]
    verified = verify_information([new_comment])
    if not verified:
        output = "Existem campos não preenchidos" 
        resp = render_template("error.html",error=output)
        return resp
    save_comment(new_comment,new_score,user.id,instance_id,instance_type)
    if instance_type == "item":
        return redirect(url_for("item",id=instance_id))
    else:
        return redirect(url_for("user",id=instance_id))

@app.route('/item_request',methods=['GET','POST'])
def item_request():
    email, err = check_user()
    if err:
        return render_template('login-form/login.html')
    item_id = int(request.form["id"])
    user = users[emailsearch[email]]
    seller = users[itens[item_id].owner_id]
    make_request(item_id,user.id,seller.id)
    return redirect(url_for("open_requests"))

@app.route('/accept_request',methods=['GET','POST'])
def accept_request():
    email, err = check_user()
    if err:
        return render_template('login-form/login.html')
    item_id = int(request.form["id"])
    user = users[emailsearch[email]]
    interested = int(request.form["interested"])
    if "accept" in request.form:
        user.requests_received[(item_id,interested)].state = 'accepted'
        itens[item_id].available = False
    else:
        user.requests_received[(item_id,interested)].state = 'rejected'
    return redirect(url_for("open_received_requests"))

@app.route('/publish_item',methods=['GET','POST'])
def publish_item():
    email, err = check_user()
    if err:
        return render_template('login-form/login.html')
    return render_template('item/publish_item.html')

@app.route('/edit_item',methods=['GET','POST'])
def edit_item():
    email,err = check_user()
    if err:
        return render_template('login-form/login.html')
    item_id = int(request.form['id'])
    if item_id not in itens.keys():
        output = "non-existent item" 
        resp = render_template("error.html",error=output)
        return resp
    edited_item = itens[item_id]
    if edited_item.owner_id != emailsearch[email]:
        output = "not your item" 
        resp = render_template("error.html",error=output)
        return resp
    return render_template("item/edit_item.html",item=edited_item)


@app.route('/evaluate_edition',methods=['GET','POST'])
def evaluate_edition():
    global engine
    email, err= check_user()
    if err:
        return render_template('login-form/login.html')
    available = 'available' in request.form
    name = request.form['name']
    desc = request.form['desc']
    item_id = int(request.form['id'])
    if item_id not in itens.keys():
        output = "non-existent item" 
        resp = render_template("error.html",error=output)
        return resp
    edited_item = itens[item_id]
    if edited_item.owner_id != emailsearch[email]:
        output = "not your item" 
        resp = render_template("error.html",error=output)
        return resp
    edited_item.available = available
    edited_item.name = name
    edited_item.desc = desc
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != "":
            photo_name = str(item_id)+".jpg"
            photo.save(os.path.join(DATA_DIR,BACKUP_DIR+str(BACKUP_COUNTER),PHOTOS_DIR,photo_name))
            edited_item.photo = photo_name
    engine.index_item(edited_item)
    engine = SearchEngine(itens.values())
    return redirect(url_for("item",id=item_id))

@app.route('/remove_item',methods=['GET','POST'])
def remove_item():
    email, err= check_user()
    if err:
        return render_template('login-form/login.html')
    item_id = int(request.form['id'])
    if item_id not in itens.keys():
        output = "non-existent item" 
        resp = render_template("error.html",error=output)
        return resp
    edited_item = itens[item_id]
    if edited_item.owner_id != emailsearch[email]:
        output = "not your item" 
        resp = render_template("error.html",error=output)
        return resp
    itens.pop(item_id)
    user = users[emailsearch[email]]
    user.itens.pop(item_id)
    pairs = [(i,k) for i,k in user.requests_received.keys()]
    for i,k in pairs:
        if i == item_id:
            req = user.requests_received[(i,k)]
            interested_id = req.interested_id
            users[interested_id].requests_made.pop(i)
            user.requests_received.pop((i,k))
    return redirect(url_for("user"))
    

@app.route('/evaluate_publication',methods=['GET','POST'])
def evaluate_publication():
    email, err= check_user()
    if err:
        return render_template('login-form/login.html')
    name = request.form['name']
    desc = request.form['desc']
    photo = request.files['photo']
    item_id = max(itens.keys())+1
    photo_name = str(item_id)+".jpg"
    photo.save(os.path.join(DATA_DIR,BACKUP_DIR+str(BACKUP_COUNTER),PHOTOS_DIR,photo_name))
    user = users[emailsearch[email]]
    verified = verify_information([name,desc,photo_name])
    if not verified:
        output = "Existem campos não preenchidos" 
        resp = render_template("error.html",error=output)
        return resp
    new_item = Item(item_id,name,owner_id=user.id,desc=desc,photo=photo_name)
    user.itens[item_id] = new_item
    itens[item_id] = new_item
    engine.index_item(new_item)
    return make_response(redirect(url_for('menu'))) 

@app.route('/image',methods=['GET'])
def image():
    photo_id = request.args['id']
    data_path = os.path.join(DATA_DIR,BACKUP_DIR+str(BACKUP_COUNTER))
    if os.path.exists(os.path.join(data_path,PHOTOS_DIR,photo_id)):
        return send_file(os.path.join(data_path,PHOTOS_DIR,photo_id))
    return send_file(os.path.join(PHOTOS_DIR,"null.png"))

@app.route('/user',methods=['GET','POST'])
def user():
    email, err = check_user()
    if err: 
        if'id' not in request.args:
            return render_template('login-form/login.html')
    else:
        user = users[emailsearch[email]]
    if 'id' in request.args:
        requested_user_id = int(request.args['id'])
    else:
        requested_user_id = user.id
    requested_user = users[requested_user_id]
    active_user = False
    if (not err and requested_user_id == user.id):
        active_user=True
    return render_template('user/user.html',user=requested_user,active_user=active_user,users=users)

@app.route('/change_location',methods=['GET','POST'])
def change_location():
    email, err = check_user()
    if err:
        return render_template('login-form/login.html')
    user = users[emailsearch[email]]
    location = Location(request.form)
    return render_template('login-form/change_location.html',location=location )

@app.route('/apply_location_changes',methods=['GET','POST'])
def apply_location():
    email, err = check_user()
    if err:
        return render_template('login-form/login.html')
    user = users[emailsearch[email]]
    
    new_address = request.form["filter"]
    if new_address == "Todas as localizações":
        output = "localização invalida"
        resp = render_template("error.html",error=output)
        return resp
    verified = verify_information([new_address])
    if not verified:
        output = "Existem campos não preenchidos" 
        resp = render_template("error.html",error=output)
        return resp

    user.city = new_address

    return redirect(url_for("user"))

@app.route('/open_received_requests',methods=['GET','POST'])
def open_received_requests():
    email, err = check_user()
    if err:
        return render_template('login-form/login.html')
    user = users[emailsearch[email]]
    return render_template('user/open_received_requests.html',requests=user.requests_received,itens=itens,users=users)

@app.route('/open_requests',methods=['GET','POST'])
def open_requests():
    email, err = check_user()
    if err:
        return render_template('login-form/login.html')
    user = users[emailsearch[email]]
    return render_template('user/open_requests.html',requests=user.requests_made,itens=itens,users=users)   

#@app.route('/save')
def save():
    print("saving...",BACKUP_COUNTER)
    data_path = os.path.join(DATA_DIR,BACKUP_DIR+str(BACKUP_COUNTER))
    with open(os.path.join(data_path,'emailsearch.pickle'), 'wb') as handle:
        pk.dump(emailsearch, handle, protocol=pk.HIGHEST_PROTOCOL)
    with open(os.path.join(data_path,'users.pickle'), 'wb') as handle:
        pk.dump(users, handle, protocol=pk.HIGHEST_PROTOCOL)
    with open(os.path.join(data_path,'itens.pickle'), 'wb') as handle:
        pk.dump(itens, handle, protocol=pk.HIGHEST_PROTOCOL)
    print("saved")
    return

def backup():
    global BACKUP_COUNTER
    print("backing up..",BACKUP_COUNTER)
    old_path = os.path.join(DATA_DIR,BACKUP_DIR+str(BACKUP_COUNTER))
    BACKUP_COUNTER += 1
    new_path = os.path.join(DATA_DIR,BACKUP_DIR+str(BACKUP_COUNTER))
    shutil.copytree(old_path,new_path)
    print("backed up")
    return

def load(new_counter=-1):
    global emailsearch
    global users
    global itens
    global engine
    global BACKUP_COUNTER
    if new_counter != -1:
        BACKUP_COUNTER = new_counter
    data_path = os.path.join(DATA_DIR,BACKUP_DIR+str(BACKUP_COUNTER))

    # with open('people.json') as f:
    #     data = json.loads(f.read())
    #     users = {
    #         int(user_dict['id']): Person(
    #             int(user_dict['id']),
    #             user_dict['name'],
    #             user_dict['password'],
    #             user_dict['phone'],
    #             user_dict['email'],
    #             user_dict['city'],
    #         )
    #         for user_dict in data.values()
    #     }
    # with open('items.json') as f:
    #     data = json.loads(f.read())
    #     itens = {
    #         item_dict['id']: Item(
    #             item_dict['id'],
    #             item_dict['name'],
    #             item_dict['owner_id'],
    #             item_dict['desc'],
    #             item_dict['photo'],
    #             item_dict['available'],
    #         )
    #         for item_dict in data.values()
    #     }

    with open(os.path.join(data_path,'emailsearch.pickle'), 'rb') as f1:
        emailsearch = pk.load(f1)
    with open(os.path.join(data_path,'users.pickle'), 'rb') as f2:
        users = pk.load(f2)
    with open(os.path.join(data_path,'itens.pickle'), 'rb') as f3:
        itens = pk.load(f3)
    engine = SearchEngine(list(itens.values()))
    return

@app.route('/test')
def test():
    return make_response("ok")

def load_data():
    people_json, item_json, comment_json, request_json = read_csv()
    for person in people_json:
        name = people_json[person]["name"]
        password = people_json[person]["password"]
        phone = people_json[person]["phone"]
        email = people_json[person]["email"]
        city = people_json[person]["city"]
        user_id = save_user(name,password,phone,email,city)
        for review in people_json[person]["comments_received"]:
            comment = review["comment"]
            score = min(review["score"],5)
            receiver = user_id
            sender_id = review["id"]
            save_comment(comment,score,sender_id,receiver,"user")
            
    for person in people_json:
        for request in people_json[person]["requests_received"]:
            state = request["state"]
            item_id = request["item_id"]
            interested_id = request["interested_id"]
            supplier_id  = request["supplier_id"]
            make_request(item_id,interested_id,supplier_id)
            

    for item in item_json:
        name = item_json[item]["name"]
        owner_id = item_json[item]["owner_id"]
        desc = item_json[item]["desc"]
        photo = item_json[item]["photo"]
        available = item_json[item]["available"]
        item_id = save_item(name,owner_id,desc,photo,available)
        for review in item_json[item]["comments"]:
            comment = review["comment"]
            score = min(review["score"],5)
            sender_id = review["id"]
            receiver = item_id
            save_comment(comment,score,sender_id,receiver,"item")
    
def assinc_save():
    while True:
        for _ in range(12*60):
            time.sleep(60)
            save()
        backup()
        


if __name__ == '__main__':
    dir_list = os.listdir(DATA_DIR)
    #os.mkdir(os.path.join(DATA_DIR,"backup_1"))
    #print(dir_list[0])
    #os.rmdir(os.path.join(DATA_DIR,"backup_1"))
    if not (len(dir_list) == 0):
        BACKUP_COUNTER = sorted([int(a.split("_")[-1]) for a in dir_list])[-1]
        data_path = os.path.join(DATA_DIR,BACKUP_DIR+str(BACKUP_COUNTER))
        load(BACKUP_COUNTER)

    else:
        BACKUP_COUNTER = 0
        data_path = os.path.join(DATA_DIR,BACKUP_DIR+str(BACKUP_COUNTER))
        os.mkdir(data_path)
        engine = SearchEngine([])

    photo_path = os.path.join(data_path,PHOTOS_DIR)

    if not os.path.exists(photo_path):
        os.mkdir(photo_path)
    saver = threading.Thread(target=assinc_save)
    saver.start()
    app.run(host="0.0.0.0",port=80)
    #app.run()