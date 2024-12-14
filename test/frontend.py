from forms import Forms, Location
from flask import Flask, render_template, request, redirect, make_response,url_for,send_file, session

app = Flask(__name__)

def save_cookies(resp,email,password):
    resp.set_cookie('email', email)
    resp.set_cookie('password',password)
    return resp

@app.route('/',methods=['GET','POST'])
def default():
    resp = make_response(redirect(url_for('menu'))) 
    return resp

@app.route('/login',methods=['GET','POST'])
def login():
    resp = make_response(render_template('login.html'))
    if "exit" in request.form:
        resp.set_cookie('email', "")
        resp.set_cookie('password',"")
    return resp

@app.route('/login_confirmation',methods=['GET','POST'])
def login_confirmation(): 
    email = request.form['email']
    password = request.form['password']
    if verify_credentials(email,password):
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
    return render_template('register.html',location = location,name=name,phone=phone,email=email,error=error)

# TODO call api instead of function
@app.route('/confirmation', methods = ['GET','POST']) 
def confirmation():  
    name = request.form['username']
    password = request.form['password']
    phone = request.form['phone']
    email = request.form['email']
    city = request.form['filter']
    resp = make_response(redirect(url_for("register")))
    resp.set_cookie('name',name)
    resp.set_cookie('phone',phone)
    resp.set_cookie('email',email)
    # TODO generate e-mail verification
    error = save_user(name,password,phone,email,city)
    if not error:
        output = "Usuario já registrado com esse email" 
        resp = render_template("error.html",error=output) 
    else:
        resp = make_response(redirect(url_for('menu')))
        resp = save_cookies(resp,email,password)
        return resp
    return resp

@app.route('/menu/<error>',methods=['GET','POST'])
@app.route('/menu',defaults={'error': ""},methods=['GET','POST'])
def menu(error):
    print(error)
    location = Location(request.form)
    return render_template('index.html', error=error, location=location)

# TODO call api instead of function
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
        return render_template('results.html', results=results, location = location, search = text_search)

# TODO call api instead of function
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
        return render_template('item.html',item=item,comments=item.comments,owner=users[item.owner_id],users=users,is_owner=is_owner)

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

# TODO call api instead of function
@app.route('/item_request',methods=['GET','POST'])
def item_request():
    email, err = check_user()
    if err:
        return render_template('login.html')
    item_id = int(request.form["id"])
    user = users[emailsearch[email]]
    seller = users[itens[item_id].owner_id]
    make_request(item_id,user.id,seller.id)
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
        user.requests_received[(item_id,interested)].state = 'accepted'
        itens[item_id].available = False
    else:
        user.requests_received[(item_id,interested)].state = 'rejected'
    return redirect(url_for("open_received_requests"))

@app.route('/publish_item',methods=['GET','POST'])
def publish_item():
    email, err = check_user()
    if err:
        return render_template('login.html')
    return render_template('publish_item.html')

# TODO call api instead of function
@app.route('/edit_item',methods=['GET','POST'])
def edit_item():
    email,err = check_user()
    if err:
        return render_template('login.html')
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
    return render_template("edit_item.html",item=edited_item)


# TODO call api instead of function
@app.route('/evaluate_edition',methods=['GET','POST'])
def evaluate_edition():
    global engine
    email, err= check_user()
    if err:
        return render_template('login.html')
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

# TODO call api instead of function
@app.route('/remove_item',methods=['GET','POST'])
def remove_item():
    email, err= check_user()
    if err:
        return render_template('login.html')
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
    

# TODO call api instead of function
@app.route('/evaluate_publication',methods=['GET','POST'])
def evaluate_publication():
    email, err= check_user()
    if err:
        return render_template('login.html')
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

# TODO call api instead of function
@app.route('/image',methods=['GET'])
def image():
    photo_id = request.args['id']
    data_path = os.path.join(DATA_DIR,BACKUP_DIR+str(BACKUP_COUNTER))
    if os.path.exists(os.path.join(data_path,PHOTOS_DIR,photo_id)):
        return send_file(os.path.join(data_path,PHOTOS_DIR,photo_id))
    return send_file(os.path.join(PHOTOS_DIR,"null.png"))

# TODO call api instead of function
@app.route('/user',methods=['GET','POST'])
def user():
    email, err = check_user()
    if err: 
        if'id' not in request.args:
            return render_template('login.html')
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
    return render_template('user.html',user=requested_user,active_user=active_user,users=users)

@app.route('/change_location',methods=['GET','POST'])
def change_location():
    email, err = check_user()
    if err:
        return render_template('login.html')
    user = users[emailsearch[email]]
    location = Location(request.form)
    return render_template('change_location.html',location=location )

# TODO call api instead of function
@app.route('/apply_location_changes',methods=['GET','POST'])
def apply_location():
    email, err = check_user()
    if err:
        return render_template('login.html')
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
        return render_template('login.html')
    user = users[emailsearch[email]]
    return render_template('open_received_requests.html',requests=user.requests_received,itens=itens,users=users)

@app.route('/open_requests',methods=['GET','POST'])
def open_requests():
    email, err = check_user()
    if err:
        return render_template('login.html')
    user = users[emailsearch[email]]
    return render_template('open_requests.html',requests=user.requests_made,itens=itens,users=users)  