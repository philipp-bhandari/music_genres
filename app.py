from flask import Flask, url_for, request, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class MyForm(FlaskForm):
    name = StringField('Логин', validators=[DataRequired()])


app = Flask(__name__)
app.secret_key = b'\xb6V\x07sx\xbc8=^\xd1-\xa8\x9c\xd0"H'

bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('content.html')


@app.route('/hello/')
def stranger():
    form = MyForm()
    return render_template('temp.html', name='странник', form=form)


@app.route('/hello/<name>')
def hello(name):
    form = MyForm()
    return render_template('temp.html', name=name, form=form)


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success') #обработка формы <---------------------------------------------------------------
    return render_template('submit.html', form=form)








if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)  # Опция debug включает перезагрузку сервера при изменении кода.












