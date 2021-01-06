from flask import Flask
from ueaglider.infrastructure.view_modifiers import response

app = Flask(__name__)


@app.route('/')
@response(template_file='home/index.html')
def index():
    return {'title': 'My awesome title'}


if __name__ == '__main__':
    app.run(debug=True)
