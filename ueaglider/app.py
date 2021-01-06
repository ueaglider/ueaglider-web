from flask import Flask
from ueaglider.data.db_session import global_init, create_session
from ueaglider.data.gliders import Gliders
from ueaglider.infrastructure.view_modifiers import response

app = Flask(__name__)

# Echo SQL queries for debugging
app.config['SQLALCHEMY_ECHO'] = True

def main():
    #register_blueprints()
    global_init('seaglider')
    app.run(debug=True)

def get_glider_count() -> int:
    session = create_session()
    return session.query(Gliders).count()

@app.route('/')
@response(template_file='home/index.html')
def index():
    """Index main page of the site

    :return: dictionary containing title for the main content h1
    """
    return {'title': get_glider_count()}


if __name__ == '__main__':
    main()

