from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import psycopg2

app = Flask(__name__)
CORS(app)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rawnak88@localhost/test'
else:
    app.debug = False
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xxjlqkvagyjeiv:1f2ac8acf89f9fdad4c3fba88ff4dbb7c2730be534dc80bac14db6514984e525@ec2-54-159-112-44.compute-1.amazonaws.com:5432/db322304ucsitt'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Loading(db.Model):
    __tablename__ = 'floor_loading'

    id = db.Column(db.Integer, primary_key=True)
    loading_type = db.Column(db.String(), unique=True)
    loading = db.Column(db.String)

    def __init__(self, loading_type, loading):
        self.loading_type = loading_type
        self.loading = loading

    def __repr__(self):
        return '<id {}>'.format(self.id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/floor_loading', methods=['POST', 'GET'])
def handle_loading():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_loading = Loading(loading_type=data['loading_type'], loading=data['loading'])
            db.session.add(new_loading)
            db.session.commit()
            return {"message": f"loading {new_loading.loading_type} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        floor_loading = Loading.query.all()
        results = [
            {
                "loading_type": loading.loading_type,
                "loading": loading.loading
            } for loading in floor_loading]

        return {"count": len(results), "loading": results}


if __name__ == '__main__':
    app.run()
