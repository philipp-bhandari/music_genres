from flask import Flask, url_for, request, render_template
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('content.html')










if __name__ == '__main__':
    app.run(debug=True)  # Опция debug включает перезагрузку сервера при изменении кода.












