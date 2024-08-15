from wtforms import Form, StringField, SelectField

class Forms(Form):
    escolha = [('ferramenta', 'ferramenta'),
               ('utensilho domestico', 'utensilho'),
               ('brinquedo', 'brinquedo')]
    filter = SelectField('oque proucura?:', choices=escolha)
    search = StringField('')
