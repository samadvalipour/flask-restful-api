from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from src.config import Development

app = Flask(__name__)
app.config.from_object(Development)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
jwtmanager = JWTManager(app)

@app.route("/",methods=["GET"])
def home():
    return "here is home"
from src.apps.users_app import users
from src.apps.site_app import site
app.register_blueprint(users)
app.register_blueprint(site)