from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../assets',
            static_url_path='/assets')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:root@127.0.0.1/myblog_db'
db = SQLAlchemy(app)

from routes import user_routes
from routes import admin_routes