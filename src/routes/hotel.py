
import json
import flask

from bson.objectid import ObjectId
from datetime import datetime
from pymongo.collection import Collection, ReturnDocument
from pymongo.errors import DuplicateKeyError
from src.models.pyObjectId import PyObjectId
from src.models.hotel import Hotel


def create_blueprint(mongo):
    """
    Generate the different endpoints related to the hotel resource
    @param {mongo}: Pymongo
    returns: Blueprint
    """
    hotels_db: Collection = mongo.db.hotel
    hotel_endpoint = flask.Blueprint(
        name="hotel_endpoint", import_name=__name__)

    @hotel_endpoint.route('/hotels', methods=['POST'])
    def add_hotel():
        """
        POST:
            description: 
                add new hotel
            request_body:
                content:
                    application/json
                schema: 
                    name: string, required
                    city: string, required
                    address: string, required
                    contact_email: string, required
                    image_url: string, required
            responses:
                '200':
                description: 
                    hotel added succesfully
                content:
                    application/json
                schema: 
                    _id: id
                    name: string
                    city: string
                    address: string
                    contact_email: string
                    image_url: string
                    created_at: datetime
                    updated_at: datetime
            example_request:
                endpoint: 
                    http://localhost:5000/api/v1/hotels 
                body:
                    {
                        "name": "Hotel Prueba Bogota",
                        "city": "Bogota",
                        "address": "Calle Falsa 123",
                        "contact_email": "test@test.com",
                        "image_url": "https://i.blogs.es/6c558d/luna-400mpx/450_1000.jpg"
                    }
        """
        json_data = flask.request.json
        json_data["created_at"] = json_data["updated_at"] = datetime.utcnow()
        hotel = Hotel(**json_data)

        errors = hotel.validate_fields()

        if len(errors) == 0:
            hotel_new = hotels_db.insert_one(hotel.to_bson_object())
            hotel.id = PyObjectId(str(hotel_new.inserted_id))

            return flask.Response(hotel.to_json_object(), mimetype='application/json')
        else:
            flask.abort(400, "Input data is incorrect: " + ', '.join(errors)) 

    @hotel_endpoint.route('/hotels')
    def get_hotels():
        """
        GET:
            description: 
                get hotels collection, including filters
            parameters:
                name: string, optional
                city: string, optional
                address: string, optional
                contact_email: string, optional
                image_url: string, optional
                created_at: string, optional
                updated_at: string, optional
            responses:
                '200':
                description: 
                    list of hotel json objects
                content:
                    application/json:
                schema: 
                    [
                        {                        
                            _id: string
                            name: string
                            city: string
                            address: string
                            contact_email: string
                            image_url: string
                            created_at: datetime
                            updated_at: datetime
                        }
                    ]
            example_request:
                endpoint:
                    http://localhost:5000/api/v1/hotels?city=Bogota
        """
        args = flask.request.args
        hotels_data = hotels_db.find(args.to_dict())

        return flask.Response(json.dumps([Hotel(**hotel).__dict__ for hotel in hotels_data], default=str), mimetype='application/json')

    @hotel_endpoint.route('/hotels/<id>')
    def get_hotel(id):
        """
        GET:
            description: 
                get hotel by id
            parameters:
                <id>: string, required
            responses:
                '200':
                description: 
                    hotel json object
                content:
                    application/json:
                schema: 
                    {
                        _id: id
                        name: string
                        city: string
                        address: string
                        contact_email: string
                        image_url: string
                        created_at: datetime
                        updated_at: datetime
                    }
            example_request:
                endpoint:
                    http://localhost:5000/api/v1/hotels/6247ccb203ae3b1961d16770
        """
        try:
            hotel = hotels_db.find_one({'_id': ObjectId(id)})
        except:
            flask.abort(400, "ID is not valid")

        if hotel:
            return flask.Response(Hotel(**hotel).to_json_object(), mimetype='application/json')
        else:
            flask.abort(404, "Hotel not found")

    @hotel_endpoint.route('/hotels', methods=['PUT'])
    def update_hotel():
        """
        PUT:
            description: 
                update hotel entry in db
            request_body:
                content:
                    application/json
                schema: 
                    id: string, required
                    name: string, required
                    city: string, required
                    address: string, required
                    contact_email: string, required
                    image_url: string, required
            responses:
                '200':
                description: 
                    hotel json object
                content:
                    application/json:
                schema: 
                    {
                        _id: id
                        name: string
                        city: string
                        address: string
                        contact_email: string
                        image_url: string
                        created_at: datetime
                        updated_at: datetime
                    }
            example_request:
                endpoint:
                    http://localhost:5000/api/v1/hotels
                body:
                    {
                        "_id": "6247ccb203ae3b1961d16770",
                        "name": "Hotel Sunrise 2",
                        "city": "Medellin",
                        "address": "Calle 123",
                        "contact_email": "test@test.com",
                        "image_url": "https://i.blogs.es/6c558d/luna-400mpx/450_1000.jpg"
                    }
        """
        json_data = flask.request.json
        json_data["updated_at"] = datetime.utcnow()
        hotel = Hotel(**json_data)
        hotel_updated = hotels_db.find_one_and_update({'_id': ObjectId(hotel.id)}, {
            '$set': hotel.to_bson_object()}, return_document=ReturnDocument.AFTER)

        if hotel_updated:
            return flask.Response(Hotel(**hotel_updated).to_json_object(), mimetype='application/json')
        else:
            flask.abort(404, "Hotel not found")

    @hotel_endpoint.route('/hotels/<id>', methods=['DELETE'])
    def delete_hotel(id):
        """
        DELETE:
            description: 
                delete hotel by id
            parameters:
                <id>: string, required
            responses:
                '200':
                description: 
                    hotel json object
                content:
                    application/json:
                schema: 
                    {
                        _id: id
                        name: string
                        city: string
                        address: string
                        contact_email: string
                        image_url: string
                        created_at: datetime
                        updated_at: datetime
                    }
            example_request:
                endpoint:
                    http://localhost:5000/api/v1/hotels/6247ee27faa1d5a115e89819
        """
        try:
            hotel_deleted = hotels_db.find_one_and_delete(
                {'_id': ObjectId(id)})
        except:
            flask.abort(400, "ID is not valid")

        if hotel_deleted:
            return flask.Response(Hotel(**hotel_deleted).to_json_object(), mimetype='application/json')
        else:
            flask.abort(404, "Hotel not found")

    @hotel_endpoint.errorhandler(500)
    def server_error(e):
        """
        Error handler for 500 errors
        """

        response = flask.jsonify(error=str(e))
        response.status_code = 500

        return response

    @hotel_endpoint.errorhandler(400)
    def invalid_client(e):
        """
        Error handler for 400 errors
        """

        response = flask.jsonify(error=str(e))
        response.status_code = 400

        return response

    @hotel_endpoint.errorhandler(404)
    def not_found(e):
        """
        Error handler for 404 errors
        """

        response = flask.jsonify(error=str(e))
        response.status_code = 404

        return response

    @hotel_endpoint.errorhandler(DuplicateKeyError)
    def not_found_duplicated(e):
        """
        Error handler for MongoDB duplicated key errors
        """
        response = flask.jsonify(error=str(e))
        response.status_code = 400

        return response

    return hotel_endpoint
