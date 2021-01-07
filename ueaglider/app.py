from flask import Flask
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

    app.register_blueprint(home_views.blueprint)

if __name__ == '__main__':
    main()

