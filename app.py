from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from music_parser import parser


def page_not_found(e):
    return render_template('404.html'), 404


class MyForm(FlaskForm):
    name = StringField('Логин', validators=[DataRequired()])


app = Flask(__name__)
app.secret_key = b'\xb6V\x07sx\xbc8=^\xd1-\xa8\x9c\xd0"H'
app.register_error_handler(404, page_not_found)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html', url=url_for('music'))


@app.route('/music/')
def music():
    form = MyForm()
    return render_template('search.html', name='странник', form=form, url=url_for('submit'))


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect(f'/show/{form.name.data}')
    return render_template('search.html', form=form)


@app.route('/show/', methods=('GET', 'POST'))
def show():
    form = MyForm()
    return render_template('search.html', name='странник', form=form, url=url_for('submit'))


@app.route('/show/<name>', methods=('GET', 'POST'))
def show_name(name):
    result = parser.main(parser.g_object, name)
    return render_template('result.html', artists=result[0], genres=result[1])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)  # Опция debug включает перезагрузку сервера при изменении кода.

url_for()










