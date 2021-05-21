""" api.py - python/flask script for running drinkBase back end"""

from drinkbase import DrinkBase
from flask import Flask, request, make_response, jsonify

ds = DrinkBase("drinkbase")
app = Flask(__name__)


@app.route("/drinkbase/v1.2/allDrinks/", methods=["GET"])
def get_all_drinks():
    """sends entire database as JSON"""
    drinks = ds.allDrinks
    drinks_json = ds.sendRecipe(drinks)
    return drinks_json


@app.route("/drinkbase/v1.2/ingreds/", methods=["GET"])
def get_ingredients():
    """querying the database by ingredient"""
    incl = request.args.get("incl")
    excl = request.args.get("excl")
    drinks = ds.allDrinks
    if incl:
        incl = incl.split(", ")
        for i in incl:
            temp_set = set(ds.ingSearch(i))
            drinks = drinks & temp_set
    if excl:
        excl = excl.split(", ")
        for i in excl:
            temp_set = set(ds.ingSearch(i))
            drinks = drinks - temp_set
    drinks = jsonify({"Names": sorted(list(drinks))})
    return drinks


@app.route("/drinkbase/v1.2/names/", methods=["GET"])
def get_name():
    """querying the database by drink name"""
    name = request.args.get("name")
    drinks = ds.nameSearch(name)
    drinks_json = jsonify({"Names": drinks})
    return drinks_json


@app.errorhandler(500)
def not_found():
    """returns 500 page"""
    return make_response(jsonify({"error": "Internal Service Error"}), 500)


@app.errorhandler(404)
def not_found():
    """returns 404 page"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(debug=False, use_reloader=True)
