# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake   # Adjusted model name to match the one in models.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_eartquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        body = {
            'id': earthquake.id,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location,
            'year' : earthquake.year
        }
        return make_response(jsonify(body), 200)
    else:
        error_message = {'message' : 'Earthquake 9999 not found.'}
        return make_response(jsonify(error_message), 404)
    

@app.route('/earthquakes/magnitude/"float:magnitude')
def get_eartquake_by_magnitude(magnitude):
    earthquake = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    quakes_data = [
        {
            'id': quake.id,
            'magnitude': quake.magnitude,
            'location': quake.location,
            'year': quake.year
        }
        for quake in earthquake
    ]
    return make_response(jsonify(quakes_data), 200) if earthquake else make_response(jsonify({'message': 'No earthquakes found with that magnitude.'}), 404)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
