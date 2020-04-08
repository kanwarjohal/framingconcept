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

    from sqlalchemy.engine.url import make_url
    url = make_url(os.environ.get('DATABASE_URL'))
    env = f'''PG_USER={url.username}
    PG_PASSWORD={url.password}    PG_HOST={url.host}
    PG_PORT={url.port}
    PG_DBNAME={url.database}'''

    app.config['SQLALCHEMY_DATABASE_URI'] = F'postgres://{url.username}:{url.password}@{url.host}:{url.port}/{url.database}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Loading(db.Model):
    __tablename__ = 'asceloading'

    id = db.Column(db.Integer, primary_key=True)
    occupency = db.Column(db.String(), unique=True)
    use = db.Column(db.String(), unique=True)
    uniformloadpsf = db.Column(db.String)

    def __init__(self, occupency, use, uniformloadpsf):
        self.occupency = occupency
        self.use = use
        self.uniformloadpsf = uniformloadpsf

    def __repr__(self):
        return '<id {}>'.format(self.id)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/asceloading', methods=['POST', 'GET'])
def handle_loading():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_loading = Loading(occupency=data['occupency'], use=data['use'], uniformloadpsf=data['uniformloadpsf'])
            db.session.add(new_loading)
            db.session.commit()
            return {"message": f"loading {new_loading.loading_type} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        asceloading = Loading.query.all()
        results = [
            {
                "occupency": loading.loading_type,
                "use": loading.loading,
                "uniformloadpsf": loading.uniformloadpsf
            } for loading in asceloading]

        return {"count": len(results), "loading": results}


if __name__ == '__main__':
    app.run()
