from app import db

class Users(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique = True)
    password = db.Column(db.String(15), unique = True)

    def __init__(self, username, password):
        self.username = username
        self.password = password