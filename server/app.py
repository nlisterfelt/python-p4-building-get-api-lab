#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    resp = [response.to_dict() for response in Bakery.query.all()]
    return make_response(resp, 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    if bakery:
        resp = bakery.to_dict()
        status = 200
    else:
        resp = {"message": "bakery not found"}
        status = 404
    return make_response(resp,status)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    resp = [good.to_dict() for good in BakedGood.query.order_by(BakedGood.price.desc()).all()]
    return make_response(resp, 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return make_response(good.to_dict(), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
