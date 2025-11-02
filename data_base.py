from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userinfo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.username} {self.email}>"

class User_info(db.Model):
    __tablename__ = "user_info"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    from_country = db.Column(db.String(100), nullable=False)
    to_country = db.Column(db.String(100), nullable=False)
    travel_date = db.Column(db.String(100), nullable=False)
    depature_date = db.Column(db.String(100), nullable=False)
    nonstop = db.Column(db.String(100), nullable=False)
    from_iata = db.Column(db.String(100), nullable=False)
    to_iata = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User_info {self.first_name} {self.last_name}>"
        
import server
