from comment import Comment
from item import Item
from person import Person
from request import Request
from utils import read_csv
from engine_search import Engine
from forms import Forms, Location
from flask import Flask, flash, render_template, request, redirect, make_response,url_for

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
def save_user(name,password,phone,email,city,resp=None) -> int:
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
    new_comment = Comment(comment,score)
    if receiver_type == "item":
        itens[receiver].comments[commenter] = new_comment
    if receiver_type == "user":
        users[receiver].received_comments[commenter] = new_comment

# helper function for creating a request object and applyting it to users
def make_request(item_id,interested_id,supplier_id,state='open'):
    new_request = Request('open',item_id,interested_id,supplier_id)
    users[supplier_id].received_requests[(item_id,interested_id)] = new_request
    users[interested_id].requests_made[item_id] = new_request


# simple user validation implement saver metods if made into a comercial product
def check_user() ->(str,bool):
    email = request.cookies.get("email")
    password = request.cookies.get("password")
    err = False
    if not validate_password(email,password):
        err = True
    return email, err

# simple password checking implement at least hashing if made into a comercial product
def validate_password(email,password) ->bool:
    null = (email == None or password == None)
    real_account = email in emailsearch.keys()
    return not null and real_account and (
        users[emailsearch[email]].password == password
        )

@app.route('/',methods=['GET','POST'])
def default():
    resp = make_response(redirect(url_for('menu'))) 
    return resp

@app.route('/login',methods=['GET','POST'])
def login():
    return  render_template('login.html')

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
    location = Location(request.form)
    return render_template('register.html',location = location)

@app.route('/confirmation', methods = ['GET','POST']) 
def confirmation(): 
    if request.method == 'POST': 
        name = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        email = request.form['email']
        city = request.form['filter']
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
    search = Forms(request.form)
    location = Location(request.form)
    if request.method == 'POST':
        return results(search,user)
    else:
        return render_template('index.html', location=location,form=search,name=user,error=error)


@app.route('/results')
def results(search,user):
    results = []
    text_search = search.data['search']
    filter = search.data['filter']
    results = engine.search(text_search,filter)

    if len(results) == 0:
        #flash('sem results, tente novamente!') 
        return redirect(url_for('menu',error="sem resultados"))
    else:
        return render_template('results.html', results=results)

@app.route('/item')
def item():
    item_id = int(request.args['id'])
    if item_id not in itens.keys():
        output = "non-existent item" 
        resp = render_template("error.html",error=output)
        return resp
    else:
        item = itens[item_id]
        return render_template('item.html',item=item,comments=item.comments,owner=users[item.owner_id],users=users)

@app.route('/comment',methods=['GET','POST'])
def comment():
    email, err = check_user()
    if err:
        return render_template('login.html')
    user = users[emailsearch[email]]
    instance_id = request.form['id']
    instance_type = request.form['type']
    return render_template('comment.html',instance_id=instance_id,instance_type=instance_type)

@app.route('/apply_comment',methods=['GET','POST'])
def apply_comment():
    email, err = check_user()
    if err:
        return render_template('login.html')
    user = users[emailsearch[email]]
    instance_id = int(request.form["id"])
    instance_type = request.form["type"]
    new_score = int(request.form["score"])
    new_comment = request.form["comment"]
    save_comment(new_comment,new_score,user.id,instance_id,instance_type)
    if instance_type == "item":
        return redirect(url_for("item",id=instance_id))
    else:
        return redirect(url_for("user",id=instance_id))

@app.route('/item_request',methods=['GET','POST'])
def item_request():
    email, err = check_user()
    if err:
        return render_template('login.html')
    item_id = int(request.form["id"])
    user = users[emailsearch[email]]
    seller = users[itens[item_id].owner_id]
    new_request = Request("open",item_id,user.id,seller.id)
    user.requests_made[item_id] = new_request
    seller.received_requests[(item_id,user.id)] = new_request
    return redirect(url_for("open_requests"))

@app.route('/accept_request',methods=['GET','POST'])
def accept_request():
    email, err = check_user()
    if err:
        return render_template('login.html')
    item_id = int(request.form["id"])
    user = users[emailsearch[email]]
    interested = int(request.form["interested"])
    if "accept" in request.form:
        user.received_requests[(item_id,interested)].state = 'accepted'
    else:
        user.received_requests[(item_id,interested)].state = 'rejected'
    return redirect(url_for("open_received_requests"))

@app.route('/publish_item',methods=['GET','POST'])
def publish_item():
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

@app.route('/user',methods=['GET','POST'])
def user():
    email, err = check_user()
    if err:
        return render_template('login.html')
    user = users[emailsearch[email]]
    if 'id' in request.args:
        requested_user_id = int(request.args['id'])
    else:
        requested_user_id = user.id
    requested_user = users[requested_user_id]
    active_user = False
    if (requested_user_id == user.id):
        active_user=True
    return render_template('user.html',user=requested_user,active_user=active_user,users=users)

@app.route('/change_location',methods=['GET','POST'])
def change_location():
    email, err = check_user()
    if err:
        return render_template('login.html')
    user = users[emailsearch[email]]
    location = Location(request.form)
    return render_template('change_location.html',location=location )

@app.route('/apply_location_changes',methods=['GET','POST'])
def apply_location():
    email, err = check_user()
    if err:
        return render_template('login.html')
    user = users[emailsearch[email]]

    new_address = request.form["filter"]
    user.city = new_address

    return redirect(url_for("user"))

@app.route('/open_received_requests',methods=['GET','POST'])
def open_received_requests():
    email, err = check_user()
    if err:
        return render_template('login.html')
    user = users[emailsearch[email]]
    return render_template('open_received_requests.html',requests=user.received_requests,itens=itens,users=users)

@app.route('/open_requests',methods=['GET','POST'])
def open_requests():
    email, err = check_user()
    if err:
        return render_template('login.html')
    user = users[emailsearch[email]]
    return render_template('open_requests.html',requests=user.requests_made,itens=itens,users=users)   

if __name__ == '__main__':
    programmers = [
        save_user("joão", "henrrique", "99999999","xavier@gmail.com","João Pessoa"),
        save_user("guilherme","silva", "88888888","toledo@gmail.com","Campina Grande")
    ]
    bananas = [
        save_item("banana maçã",programmers[0],"não é uma maçã","https://st.focusedcollection.com/11312302/i/1800/focused_150226594-stock-photo-apple-and-yellow-banana.jpg",True),
        save_item("banana nanica",programmers[0],"🤏","https://img.freepik.com/premium-photo/very-small-banana-hand_679905-1202.jpg?w=2000",True),
        save_item("maça",programmers[0],":)","https://static.vecteezy.com/system/resources/previews/002/520/838/original/apple-logo-black-isolated-on-transparent-background-free-vector.jpg",False),
        save_item("banana prata",programmers[0],"ingual o fredie mercury","https://thumbs.dreamstime.com/b/silver-banana-isolated-white-background-festive-summer-concept-silver-banana-isolated-white-background-festive-226246185.jpg",True),
        save_item("banana nevada",programmers[1],"da groomis","https://receitinhas.com.br/wp-content/uploads/2022/09/image-730x365.jpg",True),
    ]
    save_comment("olha eu commentando em mim mesmo, como isso é possivel?",5,1,1,"user")
    make_request(bananas[1],programmers[1],programmers[0])
    make_request(bananas[4],programmers[0],programmers[1],state='accepted')
    engine = Engine(itens.values())
    app.run()