from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import psycopg2
from flask import jsonify
import json

from stubbeshollowcore import *

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
    PG_PASSWORD={url.password}    
    PG_HOST={url.host}
    PG_PORT={url.port}
    PG_DBNAME={url.database}'''

    app.config['SQLALCHEMY_DATABASE_URI'] = F'postgres://{url.username}:{url.password}@{url.host}:{url.port}/{url.database}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Loading(db.Model):
    __tablename__ = 'asceloading'

    id = db.Column(db.Integer, primary_key=True)
    occupancy = db.Column(db.String(), unique=True)
    use = db.Column(db.String(), unique=True)
    uniformloadpsf = db.Column(db.String)

    def __init__(self, occupancy, use, uniformloadpsf):
        self.occupancy = occupancy
        self.use = use
        self.uniformloadpsf = uniformloadpsf

    def __repr__(self):
        return '<id {}>'.format(self.id)

class StubbesHollowCore(db.Model):
    __tablename__ = 'stubbeshollowcore'
    id = db.Column(db.Integer, primary_key=True)
    depthmm = db.Column(db.Float())
    amm2 = db.Column(db.Float())
    ixmm4 = db.Column(db.Float())
    ybmm = db.Column(db.Float())
    bwmm = db.Column(db.Float())
    fpumpa = db.Column(db.Float())
    fcmpa = db.Column(db.Float())
    fcimpa = db.Column(db.Float())
    swkpa = db.Column(db.Float())
    strands13mm = db.Column(db.Float())
    mrnmm = db.Column(db.Float())

    def __init__(self, depthmm, amm2, ixmm4, ybmm, bwmm, fpumpa, fcmpa, fcimpa, swkpa, strands13mm, mrnmm):
        self.depthmm = depthmm
        self.amm2 = amm2
        self.ixmm4 = ixmm4
        self.ybmm = ybmm
        self.bwmm = bwmm
        self.fpumpa = fpumpa
        self.fcmpa = fcmpa
        self.fcimpa = fcimpa
        self.swkpa = swkpa
        self.strands13mm = strands13mm
        self.mrnmm = mrnmm

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
            new_loading = Loading(occupancy=data['occupancy'], use=data['use'], uniformloadpsf=data['uniformloadpsf'])
            db.session.add(new_loading)
            db.session.commit()
            return {"message": f"loading {new_loading.occupancy} {new_loading.use} {new_loading.uniformloadpsf} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        asceloading = Loading.query.all()

        for loading in asceloading:
            if loading.use == None:
                loading.use = ""

        results = [
            {
                "occupancy": loading.occupancy,
                "use": loading.use,
                "uniformloadpsf": loading.uniformloadpsf
            } for loading in asceloading]

        return {"count": len(results), "loading": results}

@app.route('/framingrequest', methods=['POST'])
def handle_framing_request():
    if request.method == 'POST':
        if request.is_json:
            req = request.get_json()
            # req = {'userinput': ['Assembly areas', 'Platforms', 100], 'span': '61'}
            design_array = designstubbeshc(fl_uniform_live_load=float(req.get('userinput')[2]),
                                          fl_span=float(req.get('span')),
                                          str_units='imperial',
                                          db_hollowcore=StubbesHollowCore)

            return json.dumps(design_array)
        else:
            return {"error": "The request payload is not in JSON format"}


if __name__ == '__main__':
    app.run()
