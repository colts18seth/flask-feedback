from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to databse."""
    
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User Model """

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name= db.Column(db.String(30), nullable=False)
    
    def __repr__(self):
        """Show User info"""
        u = self
        return f"<User {u.username} - {u.first_name} {u.last_name}>"

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """ Register new user w/hashed password & return user """
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """ Validate that user and password is correct """
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False

class Feedback(db.Model):
    """ Feedback Model """

    __tablename__="feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)
    username = db.Column(db.String,
                                           db.ForeignKey('users.username'), nullable=False)

    user = db.relationship("User", backref="feedback")