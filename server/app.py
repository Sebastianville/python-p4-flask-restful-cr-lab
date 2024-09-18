#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        que = Plant.query.all()
        if(not que):
            return make_response({'message': 'plant not found'}, 404)
        plant_dict = [r.to_dict() for r in que]
        return make_response(plant_dict, 200)
    
    def post(self):
        data = request.get_json()
        try:
            plant = Plant(name=data.get('name'), image=data.get('image'), price=data.get('price'))
            db.session.add(plant)
            db.session.commit()
            return make_response(plant.to_dict(), 201)
        except: 
            return make_response({'message': 'Post did not go through, plant was not added'}, 422)

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
     def get(self, id):
        que = Plant.query.filter_by(id=id).first()
        if(not que):
            return make_response({'message': f'plant {id} not found'}, 404)
        return make_response(que.to_dict(), 200)

api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
