from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Routes and functionalities here

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])
