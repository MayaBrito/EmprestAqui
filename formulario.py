from wtforms import Form, StringField, SelectField

class Formulario(Form):
    escolha = [('ferramenta', 'ferramenta'),
               ('utensilho domestico', 'utensilho'),
               ('brinquedo', 'brinquedo')]
    filtro = SelectField('oque proucura?:', choices=escolha)
    pesquisa = StringField('')
