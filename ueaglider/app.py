from flask import Flask
import sys
import os

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)
from ueaglider.data.db_session import global_init

app = Flask(__name__)


def main():
    configure()
    app.run(debug=True, port=5006)


def configure():
    print("Configuring Flask app:")

    register_blueprints()
    print("Registered blueprints")

    global_init('seaglider')
    print("DB setup completed.")
    print("", flush=True)


def register_blueprints():
    from ueaglider.views import home_views
    from ueaglider.views import mission_views
    from ueaglider.views import dive_views

    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(mission_views.blueprint)
    app.register_blueprint(dive_views.blueprint)


if __name__ == '__main__':
    main()
else:
    configure()
