from flask import Flask
from models import *

app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./chroniclingamerica.sqlite' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    # db.drop_all()
    db.create_all()

@app.route('/')
def index():
    return "Hello! This is a test that the app runs correctly."

if __name__ == "__main__":
    app.run()
