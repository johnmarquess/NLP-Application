from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Routes and functionalities here

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])
