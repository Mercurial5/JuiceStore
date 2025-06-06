from flask import Blueprint, request, jsonify
from flask_pydantic import validate

from src.juices.service.service import JuiceService
from src.juices.shemas import JuiceRequestCreate, JuiceRequestPriceUpdate

juice_api = Blueprint('juice_api', __name__)
juice_service = JuiceService()


@juice_api.route('/api/juices', methods=['GET'])
def get_juices_route():
    return juice_service.get_all_juices(), 200


@juice_api.route('/api/juices', methods=['POST'])
@validate()
def create_juice_route(body: JuiceRequestCreate):
    try:
        juice_service.add_juice(body)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"message": "Juice created"}), 201


@juice_api.route('/api/juices/<int:juice_id>', methods=['PATCH'])
@validate()
def change_juice_price_route(juice_id: int, body: JuiceRequestPriceUpdate):
    try:
        juice_service.change_juice_price(juice_id, body)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"message": "Price updated"}), 200


@juice_api.route('/api/juices/<int:juice_id>', methods=['DELETE'])
def delete_juice_route(juice_id):
    try:
        juice_service.delete_juice(juice_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"message": "Juice deleted"}), 200
