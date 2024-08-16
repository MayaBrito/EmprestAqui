from comment import Comment
from item import Item
from person import Person
from request import Request
from utils import read_csv
from engine_search import Engine
from forms import Forms
from flask import Flask, flash, render_template, request, redirect, make_response,url_for

app = Flask(__name__)
emailsearch = {}
users = {}
itens = {}

def save_user(resp,name,password,phone,email,city):
    new_id = len(users)
    new_user = Person(new_id,name,password,phone,email,city)
    users[new_id] = new_user
    emailsearch[email] = new_id
    resp.set_cookie('email', name)
    resp.set_cookie('password',password)
    return resp

def save_cookies(resp,email,password):
    resp.set_cookie('email', email)
    resp.set_cookie('password',password)
    return resp

def check_user() ->(str,bool):
    email = request.cookies.get("email")
    password = request.cookies.get("password")
    err = False
    if not validate_password(email,password):
        err = True
    return email, err

def validate_password(email,password):
    # print(email,password)
    # print(emailsearch)
    # users[emailsearch[email]].password
    null = (email == None or password == None)
    real_account = email in emailsearch.keys()
    return not null and real_account and (
        users[emailsearch[email]].password == password
        )

@app.route('/',methods=['GET'])
def Login():
    # user,err = check_user()
    # if err:
    #     return render_template('login.html')
    # else:
    resp = make_response(redirect(url_for('menu'))) 
    return resp

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST': 
        email = request.form['email']
        password = request.form['password']
        if validate_password(email,password):
            resp = make_response(redirect(url_for('menu'))) 
            resp = save_cookies(resp,email,password)
            return resp
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
        password = request.form['password']
        phone = request.form['phone']
        email = request.form['email']
        city = request.form['city']
        if email not in emailsearch:
            resp = make_response(redirect(url_for('menu')))
            save_user(resp,name,password,phone,email,city)
            return resp
        else:
            output = "user already registered with this email" 
            resp = make_response(output) 
    return resp

@app.route('/menu',methods=['GET','POST'])
def menu():
    # user,err = check_user()
    # if err:
    #     return redirect("/")

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

@app.route('/item_request',methods=['GET','POST'])
def item_request():
    email, err = check_user()
    if err:
        return render_template('login.html')
    item_id = int(request.form["id"])
    user = users[emailsearch[email]]
    seller = users[itens[item_id].owner_id]
    new_request = Request("open",item_id,name,user.phone,seller.phone)
    user.requests_made[item_id] = new_request
    seller.received_requests[(item_id,name)] = new_request
    return redirect(url_for("open_requests"))

@app.route('/accept_request',methods=['GET','POST'])
def accept():
    email, err = check_user()
    if err:
        return render_template('login.html')
    item_id = int(request.form["id"])
    user = users[emailsearch[email]]
    interested = request.form["interested"]
    user.received_requests[(item_id,interested)].state = 'accepted'
    return redirect(url_for("open_received_requests"))

# @app.route('/reject_request',methods=['GET','POST'])
# def accept():
#     email, err = check_user()
#     if err:
#         return render_template('login.html')
#     item_id = int(request.form["id"])
#     user = users[emailsearch[email]]
#     interested = request.form["interested"]
#     user.received_requests[(item_id,interested)].state = 'accepted'
#     return redirect(url_for("open_received_requests"))

@app.route('/publish_item',methods=['GET','POST'])
def publish():
    email, err = check_user()
    if err:
        return render_template('login.html')
    return render_template('publish_item.html')

@app.route('/evaluate_publication',methods=['GET','POST'])
def evaluate_publication():
    email, err= check_user()
    if err:
        return render_template('login.html')
    name = request.form['name']
    desc = request.form['desc']
    photo = request.form['photo']
    item_id = len(itens)
    user = users[emailsearch[email]]
    new_item = Item(item_id,name,owner_id=user.id,desc=desc,photo=photo)
    user.itens[item_id] = new_item
    itens[item_id] = new_item
    engine.adicionar_item(new_item)
    return make_response(redirect(url_for('menu'))) 

@app.route('/user',methods=['GET','POST'])#meus itens postados
def user():
    email, err = check_user()
    if err:
        return render_template('login.html')
    user = users[emailsearch[email]]
    return render_template('user.html', user=user)

@app.route('/open_received_requests',methods=['GET','POST'])
def open_received_requests():
    email, err = check_user()
    if err:
        return render_template('login.html')
    user = users[emailsearch[email]]
    return render_template('open_received_requests.html',requests=user.received_requests,itens=itens)

@app.route('/open_requests',methods=['GET','POST'])
def open_requests():
    email, err = check_user()
    if err:
        return render_template('login.html')
    user = users[emailsearch[email]]
    return render_template('open_requests.html',requests=user.requests_made,itens=itens)   

if __name__ == '__main__':
    programmers = [
        Person(0,"joão", "henrrique", "99999999","xavier@gmail.com","bananeiras"),
        Person(1,"guilherme","silva", "88888888","toledo@gmail.com","bahia")
    ]
    bananas = [
        Item(0,"banana maçã",0),
        Item(1,"banana nanica",0),
        Item(2,"maçã",0),
        Item(3,"banana prata",0),
        Item(4,"banana nevada",1,desc="da gromis",photo="https://receitinhas.com.br/receita/pizza-de-banana-nevada/")
    ]
    bananas[-1].comments["carlos"] = Comment("achei ruim\nbem ruim\nnão é lá essas coisas",2)
    request_1 = Request('open',1,programmers[1].name,programmers[1].phone,programmers[0].phone)
    request_2 = Request('accepted',4,programmers[0].name,programmers[0].phone,programmers[1].phone)
    programmers[0].received_requests[(request_1.item,request_1.interested)] = request_1
    programmers[1].requests_made[request_1.item] = request_1
    programmers[1].received_requests[(request_2.item,request_2.interested)] = request_2
    programmers[0].requests_made[request_2.item] = request_2

    for p in programmers:
        users[p.id] = p
        emailsearch[p.email] = p.id

    for b in bananas:
        itens[b.id] = b
        users[b.owner_id].itens[b.id] = b

    engine = Engine(bananas)
    app.run()