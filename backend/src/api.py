from crypt import methods
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


# CORS Headers
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers",
                         "Content-Type,Authorization,true")
    response.headers.add("Access-Control-Allow-Methods",
                         "GET,PUT,POST,DELETE,OPTIONS,PATCH")
    return response


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_drinks_short():
    return jsonify({
        "success": True,
        "drinks": [drink.short() for drink in Drink.query.all()]
    }), 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    return jsonify({
        "success": True,
        "drinks": [drink.long() for drink in Drink.query.all()]
    })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth("post:drinks")
def add_new_drink(payload):
    data = request.json
    try:
        title = data["title"]
        recipe = json.dumps(data["recipe"])
        toSave = Drink(title=title, recipe=recipe)
        Drink.insert(toSave)
        return jsonify({"success": True, "drinks": toSave.short()})
    except Exception as e:
        return jsonify(
            {"message": "There was an error proccessing your request"}), 400


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def update_drink(payload, id):
    data = request.json
    try:
        title = data["title"]
        recipe = json.dumps(data["recipe"])
        toSave = Drink.query.get(id)
        if (toSave):
            toSave.title = title
            toSave.recipe = recipe
            toSave.update()
            return jsonify({"success": True, "drinks": toSave.short()})
        else:
            return jsonify({
                "success": False,
                "message": "Drink not found"
            }), 404
    except Exception as e:
        message = e.orig.args
        if message[0] == 'UNIQUE constraint failed: drink.title':
            return jsonify({"message": "Duplicate entry for title"}), 409
        return jsonify(
            {"message": "There was an error proccessing your request"}), 400


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(payload, id):
    try:
        Todelete = Drink.query.get(id)
        if (Todelete):
            Drink.delete(Todelete)
            return jsonify({"success": True, "delete": id})
        else:
            return jsonify({
                "success": False,
                "message": "Drink not found"
            }), 404
    except Exception as e:
        return jsonify(
            {"message": "There was an error proccessing your request"}), 400


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def no_ressource_found(e):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found",
    }), 404


@app.errorhandler(500)
def server_error():
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error",
    }), 500


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def handle_auth_error(e):
    return jsonify({"message": e.error}), e.status_code


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
