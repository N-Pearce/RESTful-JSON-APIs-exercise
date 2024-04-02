"""Flask app for Cupcakes"""

from flask import Flask, request, render_template, redirect, jsonify
from models import db, connect_db, Cupcake, serialize_cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# app.config['SECRET_KEY'] = 'pwab'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/cupcakes')
def GET_cupcakes():
    cupcakes = Cupcake.query.order_by(Cupcake.id).all()
    serialized = [serialize_cupcake(c) for c in cupcakes]
    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cupk_id>')
def GET_cupcake_id(cupk_id):
    cupcake = Cupcake.query.get_or_404(cupk_id)
    serialized = serialize_cupcake(cupcake)
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def POST_cupcake():
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']

    new_cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image=image
    )
    db.session.add(new_cupcake)
    db.session.commit()
    
    serialized = serialize_cupcake(new_cupcake)
    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<int:cupk_id>', methods=['PATCH'])
def PATCH_cupcake_id(cupk_id):
    cupcake = Cupcake.query.get_or_404(cupk_id)

    cupcake.flavor = request.json['flavor']
    cupcake.size = request.json['size']
    cupcake.rating = request.json['rating']
    cupcake.image = request.json['image']

    db.session.add(cupcake)
    db.session.commit()

    serialized = serialize_cupcake(cupcake)
    return (jsonify(cupcake=serialized), 200)

@app.route('/api/cupcakes/<cupk_id>', methods=['DELETE'])
def DELETE_cupcake(cupk_id):
    cupcake = Cupcake.query.get_or_404(cupk_id)
    db.session.delete(cupcake)
    db.session.commit()
    return '{"message": "Deleted"}'