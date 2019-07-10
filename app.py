from flask import Flask, render_template, redirect, Response
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
    return render_template('index.html')


@app.route('/music/')
def music():
    form = MyForm()
    return render_template('search.html', form=form)


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect(f'/show/{form.name.data}')
    return render_template('search.html', form=form)


@app.route('/show/', methods=('GET', 'POST'))
def show():
    form = MyForm()
    return render_template('search.html', form=form)


@app.route('/show/<name>', methods=('GET', 'POST'))
def show_name(name):
    result = parser.main(parser.g_object, name)
    return render_template('result.html', artists=result[0], genres=result[1])


@app.route('/getInfo/<artist_id>', methods=('GET', 'POST'))
def get_info(artist_id):
    ret = parser.sub_query(parser.g_object, artist_id)
    return Response(response=ret, status=200, mimetype="application/json")


if __name__ == '__main__':
    app.run()








