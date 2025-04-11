from flask import Flask
import os


SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


from .views import views
app.register_blueprint(views, url_prefix="/")