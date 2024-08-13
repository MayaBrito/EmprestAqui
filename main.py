from comment import Comment
from item import Item
from person import Person
from request import Request
from utils import read_csv
from engine_search import Engine
from forms import Forms
from flask import Flask, flash, render_template, request, redirect, make_response,url_for

app = Flask(__name__)
users = {}
itens = {}

def check_user() ->(str,bool):
    name = request.cookies.get("username")
    password = request.cookies.get("password")
    err = False
    if not validate_password(name,password):
        err = True
    return name, err

def validate_password(name,password):
    null = (user == None or password == None)
    real_account = name in users.keys()
    return not null and real_account and (users[name].password == password)

@app.route('/',methods=['GET'])
def Login():
    user,err = check_user()
    if err:
        return render_template('login.html')
    else:
        resp = make_response(redirect(url_for('menu'))) 
        return resp

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST': 
        name = request.form['username']
        password = request.form['password']
        if validate_password(name,password):
            resp = make_response(redirect(url_for('menu'))) 
            resp.set_cookie('username', name)
            resp.set_cookie('password',password)
        else:
            output = "wrong username or password" 
            resp = make_response(output) 
    return resp

@app.route('/register',methods=['GET','POST'])
def register():
    return render_template('register.html')

@app.route('/confirmation', methods = ['GET','POST']) 
def confirmation(): 
    if request.method == 'POST': 
        name = request.form['username']
        desc = request.form['description']
        phone = request.form['phone']
        password = request.form['password']
        if name not in users:
            new_user = Person(name,desc,phone,password)
            users[name] = new_user
            resp = make_response(redirect(url_for('menu')))
            resp.set_cookie('username', name)
            resp.set_cookie('password',password)
        else:
            output = "user already registered with this name" 
            resp = make_response(output) 
    return resp

@app.route('/menu',methods=['GET','POST'])
def menu():
    user,err = check_user()
    if err:
        return redirect("/")

    search = Forms(request.form)
    if request.method == 'POST':
        return results(search,user)
    else:
        return render_template('index.html', form=search,name=user)


@app.route('/results')
def results(search,user):
    results = []
    text_search = search.data['search']
    filter = search.data['filter']
    results = engine.search(text_search,filter)

    if len(results) == 0:
        #flash('sem results, tente novamente!') 
        return redirect(url_for('menu'))
    else:
        return render_template('results.html', results=results)

@app.route('/item')
def item():
    item_id = int(request.args['id'])
    if item_id not in itens.keys():
        output = "non-existent item" 
        resp = make_response(output)
        return resp
    else:
        item = itens[item_id]
        return render_template('item.html',item=item,comments=item.comments)

@app.route('/requisition',methods=['GET','POST'])
def requisition():
    name, err = check_user()
    if err:
        return redirect("/")
    item_id = int(request.form["id"])
    user = users[name]
    seller = users[itens[item_id].owner_id]
    new_request = Request("open",item_id,name,user.phone,seller.phone)
    user.requests_made[item_id] = new_request
    seller.received_requests[(item_id,name)] = new_request
    return redirect(url_for("open_requests"))

@app.route('/accept',methods=['GET','POST'])
def accept():
    name, err = check_user()
    if err:
        return redirect("/")
    item_id = int(request.form["id"])
    user = users[name]
    interested = request.form["interested"]
    user.received_requests[(item_id,interested)].state = 'accepted'
    return redirect(url_for("open_received_requests"))

@app.route('/publish_item')
def publish():
    return render_template('publish_item.html')

@app.route('/evaluate_publication',methods=['GET','POST'])
def evaluate_publication():
    user, err= check_user()
    if err:
        return redirect("/") 
    name = request.form['name']
    desc = request.form['desc']
    photo = request.form['photo']
    item_id = len(itens)
    new_item = Item(item_id,name,owner_id=user,desc=desc,photo=photo)
    users[user].publica_item(new_item)
    itens[item_id] = new_item
    engine.adicionar_item(new_item)
    return make_response(redirect(url_for('menu'))) 

@app.route('/user')#meus itens postados
def user():
    name, err = check_user()
    user = users[name]
    if err:
        return redirect("/")
    return render_template('user.html', user=user)

@app.route('/open_received_requests')
def open_received_requests():
    name, err = check_user()
    user = users[name]
    if err:
        return redirect("/")
    return render_template('open_received_requests.html',requests=user.received_requests,itens=itens)

@app.route('/open_requests')
def open_requests():
    name, err = check_user()
    user = users[name]
    if err:
        return redirect("/")
    
    return render_template('open_requests.html',requests=user.requests_made,itens=itens)   

if __name__ == '__main__':
    programmers = [
        Person("joão", "henrrique", "99999999","xavier"),
        Person("guilherme","silva", "88888888","toledo")
    ]
    bananas = [
        Item(1,"banana maçã","joão"),
        Item(2,"banana nanica","joão"),
        Item(3,"maçã","joão"),
        Item(4,"banana prata","joão"),
        Item(5,"banana nevada","guilherme",desc="da gromis",photo="https://receitinhas.com.br/receita/pizza-de-banana-nevada/")
    ]
    bananas[-1].comments["carlos"] = Comment("achei ruim\nbem ruim\nnão é lá essas coisas",2)
    request_1 = Request('open',1,programmers[1].name,programmers[1].phone,programmers[0].phone)
    request_2 = Request('accepted',5,programmers[0].name,programmers[0].phone,programmers[1].phone)
    programmers[0].received_requests[(request_1.item,request_1.interested)] = request_1
    programmers[1].requests_made[request_1.item] = request_1
    programmers[1].received_requests[(request_2.item,request_2.interested)] = request_2
    programmers[0].requests_made[request_2.item] = request_2

    for p in programmers:
        users[p.name] = p

    for b in bananas:
        itens[b.id] = b
        users[b.owner_id].itens[b.id] = b

    engine = Engine(bananas)
    app.run()