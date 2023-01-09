# importing all libraries for app.py
from flask_sqlalchemy import SQLAlchemy
import api.db_config as db_config

import flask
app = flask.Flask(__name__)


app.config['SECRET_KEY'] = 'thisismysecretkeydonotstealit'
app.config['SQLALCHEMY_DATABASE_URI'] = db_config.db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # TODO: check why is this?
app.config['JSON_SORT_KEYS'] = False # it makes sure that data in JSON is sent/or received as it is passed(not sorted).

# app.config['MYSQL_PORT'] = '3306'

db = SQLAlchemy(app)


# ~~~~~~~~~~~~~~~~~~~~ BluePrints ~~~~~~~~~~~~~~~~~~~~~~
# importiong all bluprints
from api.blueprints.main import main as main_blueprint

# registering all blueprints for api uses
app.register_blueprint(main_blueprint, url_prefix='/api')
# ~~~~~~~~~~~~~~~~~~~~ BluePrints End ~~~~~~~~~~~~~~~~~~~~~~
@app.before_first_request
def create_tables():
    # See important note below
    from api.models.user_model import User
    db.create_all()



with app.app_context():
    db.init_app(app)
    # Added this import just beore create_all
    from api.models import user_model  
    db.create_all()
    db.session.commit()

if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=5000, debug=True)