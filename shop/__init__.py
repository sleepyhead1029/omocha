from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Query
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
import os

from flask_msearch import Search
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///omochashop.db'
app.config['SECRET_KEY'] = "omocha"
app.config['UPLOADED_PHOTOS_DEST']= os.path.join(basedir, 'static/images')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
# search.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'customerLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u"Please Login First"


photos = UploadSet('photos', IMAGES)
configure_uploads(app,photos)
patch_request_class(app, 32*1024*1024)

migrate = Migrate(app,db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)






from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customers import routes