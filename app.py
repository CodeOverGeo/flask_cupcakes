"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'carrot'

connect_db(app)


@app.route('/')
def index():
    """Show homepage"""

    return render_template("index.html")


@app.route('/api/cupcakes')
def list_cupcakes():
    """Return cupcakes in database

    Returns in JSON:
        {cupcakes: [{id, flavor, rating, size, image}, ...]}
    """

    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Return data on specific cupcake

    Returns in JSON:
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a new cupcake, returns data about new cupcake

    Returns in JSON
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data.get('image', None))

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 201)


@ app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update cupcake data from request, returns updated data

    Returns in JSON
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data.get('image', cupcake.image)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@ app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def remove_cupcake(cupcake_id):
    """Delete cupcake and returns verification

    Returns JSON of {message: 'Deleted'}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(mesage='Deleted')
