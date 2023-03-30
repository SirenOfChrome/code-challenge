#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Sweet, Vendor, VendorSweet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/vendors', methods=['GET'])
def get_vendors():
    vendors = Vendor.query.all()
    vendor_list = [{'id': vendor.id, 'name': vendor.name} for vendor in vendors]
    return jsonify(vendor_list)

@app.route('/vendors/<int:id>', methods=['GET', 'DELETE'])
def vendor_by_id(id):
    vendor = Vendor.query.get(id)

    if vendor:

        if request.method == 'GET':
            vendor_dict = {
                'id': vendor.id,
                'name': vendor.name,
                'vendor_sweets': [vs.serialize() for vs in vendor.vendor_sweets]
            }

            response = make_response(jsonify(vendor_dict), 200)

        elif request.method == 'DELETE':
            db.session.delete(vendor)
            db.session.commit()

            response = make_response({}, 200)

    else:
        response = make_response({'error': 'Vendor not found'}, 404)

    return response


@app.route('/sweets', methods=['GET'])
def get_sweets():
    sweets = Sweet.query.all()

    if sweets:
        sweet_list = [{'id': sweet.id, 'name': sweet.name} for sweet in sweets]
        response = make_response(jsonify(sweet_list), 200)
    else:
        response = make_response({'error': 'No sweets found'}, 404)

    return response


@app.route('/sweets/<int:id>', methods=['GET'])
def get_sweet(id):
    sweet = Sweet.query.get(id)

    if sweet:
        sweet_dict = {
            'id': sweet.id,
            'name': sweet.name
        }

        response = make_response(jsonify(sweet_dict), 200)
    else:
        response = make_response({'error': 'Sweet not found'}, 404)

    return response


@app.route('/vendor_sweets', methods=['POST'])
def create_vendor_sweet():
    data = request.get_json()

    if not all(key in data for key in ['price', 'vendor_id', 'sweet_id']):
        return make_response(jsonify({'error': 'Validation errors'}), 400)

    if data['price'] < 0:
        return make_response(jsonify({'error': 'Validation errors'}), 400)

    vendor = Vendor.query.get(data['vendor_id'])
    sweet = Sweet.query.get(data['sweet_id'])

    if not vendor or not sweet:
        return make_response(jsonify({'error': 'Invalid vendor or sweet id'}), 400)

    vendor_sweet = VendorSweet(price=data['price'], vendor=vendor, sweet=sweet)

    try:
        db.session.add(vendor_sweet)
        db.session.commit()

        vendor_sweet_dict = {
            'id': vendor_sweet.id,
            'price': vendor_sweet.price,
            'sweet': {
                'id': sweet.id,
                'name': sweet.name
            },
            'vendor': {
                'id': vendor.id,
                'name': vendor.name
            }
        }

        return make_response(jsonify(vendor_sweet_dict), 201)

    except:
        db.session.rollback()

        return make_response(jsonify({'error': 'Validation errors'}), 400)
        
@app.route('/vendor_sweets/<int:id>', methods=['DELETE'])
def delete_vendor_sweet(id):
    vendor_sweet = VendorSweet.query.get(id)

    if vendor_sweet:
        db.session.delete(vendor_sweet)
        db.session.commit()

        return make_response(jsonify({}), 200)
    else:
        return make_response(jsonify({'error': 'VendorSweet not found'}), 404)


    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
