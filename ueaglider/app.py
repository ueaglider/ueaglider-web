from flask import Flask
import sys
import os
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)
from ueaglider.data.db_session import global_init, create_session
from ueaglider.data.gliders import Gliders
from ueaglider.infrastructure.view_modifiers import response

app = Flask(__name__)

# Echo SQL queries for debugging
app.config['SQLALCHEMY_ECHO'] = True

def main():
    # Collect all the page routes and instructions
    register_blueprints()
    # Initialise the database
    global_init('seaglider')
    app.run(debug=True)

def register_blueprints():
    from ueaglider.views import home_views
    from ueaglider.views import mission_views
    from ueaglider.views import dive_views

    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(mission_views.blueprint)
    app.register_blueprint(dive_views.blueprint)

if __name__ == '__main__':
    main()

