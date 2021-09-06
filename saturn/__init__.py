from flask import Flask, render_template
from saturn.compile import compile_notebooks


compile_notebooks()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<p>Hello world</p>"

@app.route('/<path:name>')
def main(name):
    with open('site/' + name + '.html', 'r') as f:
        content = f.read()
        return render_template('base.html', content=content)

