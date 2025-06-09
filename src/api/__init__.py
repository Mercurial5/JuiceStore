from flask import Flask

from juices import get_db_session
from juices.repositories import JuiceRepository
from juices.services.services import JuiceService


def create_app() -> Flask:
    app = Flask(__name__)

    app.config['juice_service'] = JuiceService(JuiceRepository(get_db_session()))
    from api.routes.juices import juice_api
    app.register_blueprint(juice_api)

    return app
