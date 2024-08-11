from comentario import Comentario
from item import Item
from pessoa import Pessoa
from pedido import Pedido
from utils import read_csv
from engine_busca import Engine
from formulario import Formulario
from flask import Flask, flash, render_template, request, redirect, make_response,url_for

app = Flask(__name__)
usuarios = {}
itens = {}

def verifica_usuario() ->(str,bool):
    nome = request.cookies.get("username")
    senha = request.cookies.get("password")
    err = False
    if not valida_senha(nome,senha):
        err = True
    return nome, err

def valida_senha(nome,senha):
    vazio = (usuario == None or senha == None)
    conta_real = nome in usuarios.keys()
    return not vazio and conta_real and (usuarios[nome].senha == senha)

@app.route('/',methods=['GET'])
def Login():
    usuario,err = verifica_usuario()
    if err:
        return render_template('login.html')
    else:
        resp = make_response(redirect(url_for('menu'))) 
        return resp

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST': 
        nome = request.form['username']
        senha = request.form['password']
        if valida_senha(nome,senha):
            resp = make_response(redirect(url_for('menu'))) 
            resp.set_cookie('username', nome)
            resp.set_cookie('password',senha)
        else:
            output = "usuário ou senha erradas" 
            resp = make_response(output) 
    return resp

@app.route('/registrar',methods=['GET','POST'])
def registrar():
    return render_template('register.html')

@app.route('/confirmacao', methods = ['GET','POST']) 
def confirmacao(): 
    if request.method == 'POST': 
        nome = request.form['username']
        descricao = request.form['description']
        contato = request.form['contato']
        senha = request.form['password']
        if nome not in usuarios:
            novo_usuario = Pessoa(nome,descricao,contato,senha)
            usuarios[nome] = novo_usuario
            resp = make_response(redirect(url_for('menu')))
            resp.set_cookie('username', nome)
            resp.set_cookie('password',senha)
        else:
            output = "usuario já cadastrado com esse nome" 
            resp = make_response(output) 
    return resp

@app.route('/menu',methods=['GET','POST'])
def menu():
    usuario,err = verifica_usuario()
    if err:
        return redirect("/")

    pesquisa = Formulario(request.form)
    if request.method == 'POST':
        return resultados(pesquisa,usuario)
    else:
        return render_template('index.html', form=pesquisa,nome=usuario)


@app.route('/resultados')
def resultados(pesquisa,usuario):
    resultados = []
    texto_pesquisa = pesquisa.data['pesquisa']
    filtro = pesquisa.data['filtro']
    resultados = engine.buscar(texto_pesquisa,filtro)

    if len(resultados) == 0:
        #flash('sem resultados, tente novamente!') 
        return redirect(url_for('menu'))
    else:
        return render_template('results.html', results=resultados)

@app.route('/item')
def item():
    item_id = int(request.args['id'])
    if item_id not in itens.keys():
        output = "item inexistente" 
        resp = make_response(output)
        return resp
    else:
        item = itens[item_id]
        return render_template('item.html',item=item,comentarios=item.comentarios)

@app.route('/requisitar',methods=['GET','POST'])
def requisitar():
    nome, err = verifica_usuario()
    if err:
        return redirect("/")
    item_id = int(request.form["id"])
    usuario = usuarios[nome]
    vendedor = usuarios[itens[item_id].dono_id]
    novo_pedido = Pedido("aberto",item_id,nome,usuario.contato,vendedor.contato)
    usuario.pedidos_feitos[item_id] = novo_pedido
    vendedor.pedidos_recebidos[(item_id,nome)] = novo_pedido
    return redirect(url_for("pedidos_feitos_abertos"))

@app.route('/aceitar',methods=['GET','POST'])
def aceitar():
    nome, err = verifica_usuario()
    if err:
        return redirect("/")
    item_id = int(request.form["id"])
    usuario = usuarios[nome]
    interessado = request.form["interessado"]
    usuario.pedidos_recebidos[(item_id,interessado)].estado = 'aceito'
    return redirect(url_for("pedidos_recebidos_abertos"))

@app.route('/publicar_item')
def publicar():
    return render_template('publicar_item.html')

@app.route('/avaliar_pubicacao',methods=['GET','POST'])
def avaliar_pubicacao():
    usuario, err= verifica_usuario()
    if err:
        return redirect("/") 
    nome = request.form['nome']
    descricao = request.form['descricao']
    foto = request.form['foto']
    item_id = len(itens)
    novo_item = Item(item_id,nome,dono_id=usuario,desc=descricao,foto=foto)
    usuarios[usuario].publica_item(novo_item)
    itens[item_id] = novo_item
    engine.adicionar_item(novo_item)
    return make_response(redirect(url_for('menu'))) 

@app.route('/usuario')#meus itens postados
def usuario():
    nome, err = verifica_usuario()
    usuario = usuarios[nome]
    if err:
        return redirect("/")
    return render_template('usuario.html', usuario=usuario)

@app.route('/pedidos_recebidos_abertos')
def pedidos_recebidos_abertos():
    nome, err = verifica_usuario()
    usuario = usuarios[nome]
    if err:
        return redirect("/")
    return render_template('pedidos_recebidos_abertos.html',pedidos=usuario.pedidos_recebidos,itens=itens)

@app.route('/pedidos_feitos_abertos')
def pedidos_feitos_abertos():
    nome, err = verifica_usuario()
    usuario = usuarios[nome]
    if err:
        return redirect("/")
    
    return render_template('pedidos_feitos_abertos.html',pedidos=usuario.pedidos_feitos,itens=itens)   

if __name__ == '__main__':
    programadores = [
        Pessoa("joão", "henrrique", "99999999","xavier"),
        Pessoa("guilherme","silva", "88888888","toledo")
    ]
    bananas = [
        Item(1,"banana maçã","joão"),
        Item(2,"banana nanica","joão"),
        Item(3,"maçã","joão"),
        Item(4,"banana prata","joão"),
        Item(5,"banana nevada","guilherme",desc="da gromis",foto="https://receitinhas.com.br/receita/pizza-de-banana-nevada/")
    ]
    bananas[-1].comentarios["carlos"] = Comentario("achei ruim\nbem ruim\nnão é lá essas coisas",2)
    pedido_1 = Pedido('aberto',1,programadores[1].nome,programadores[1].contato,programadores[0].contato)
    pedido_2 = Pedido('aceito',5,programadores[0].nome,programadores[0].contato,programadores[1].contato)
    programadores[0].pedidos_recebidos[(pedido_1.item,pedido_1.interessado)] = pedido_1
    programadores[1].pedidos_feitos[pedido_1.item] = pedido_1
    programadores[1].pedidos_recebidos[(pedido_2.item,pedido_2.interessado)] = pedido_2
    programadores[0].pedidos_feitos[pedido_2.item] = pedido_2

    for p in programadores:
        usuarios[p.nome] = p

    for b in bananas:
        itens[b.id] = b
        usuarios[b.dono_id].itens[b.id] = b

    engine = Engine(bananas)
    app.run()