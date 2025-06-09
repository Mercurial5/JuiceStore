from typing import Tuple

from flask import Blueprint, Response, request, current_app
from flask_pydantic import validate
from pydantic import ValidationError

from juices.schemas import JuiceRequestCreate, JuiceRequestPriceUpdate, PaginationRequest

juice_api = Blueprint('juice_api', __name__, url_prefix='/api/juices')


@juice_api.route('/', methods=['GET'])
def get_juices_route() -> Tuple[dict, int]:
    juice_service = current_app.config['juice_service']
    query_params = request.args.to_dict()
    try:
        body = PaginationRequest(**query_params)
    except ValidationError:
        return {"error": "invalid pagination"}, 400
    return juice_service.get_all_juices(body.page, body.limit), 200


@juice_api.route('/', methods=['POST'])
@validate()
def create_juice_route(body: JuiceRequestCreate) -> Response:
    juice_service = current_app.config['juice_service']
    juice_service.add_juice(body)
    return Response(status=201)


@juice_api.route('/<int:juice_id>', methods=['PATCH'])
@validate()
def change_juice_price_route(juice_id: int, body: JuiceRequestPriceUpdate) -> Response:
    juice_service = current_app.config['juice_service']
    juice_service.change_juice_price(juice_id, body)
    return Response(status=200)


@juice_api.route('/<int:juice_id>', methods=['DELETE'])
def delete_juice_route(juice_id) -> Response:
    juice_service = current_app.config['juice_service']
    juice_service.delete_juice(juice_id)
    return Response(status=204)
