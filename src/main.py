from api import create_app
from src.api.routes.juices import juice_api


def main():
    app = create_app()
    app.register_blueprint(juice_api)

    app.run()


if __name__ == '__main__':
    main()
