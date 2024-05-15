from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from database import db

class User(UserMixin, db.Model):
    __tablename__ = "users"

    # Define las columnas de la tabla `users`
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
      # Inicializa la clase `User`
    def __init__(self, username, password):

        self.username = username
        self.password_hash=generate_password_hash(password)



    # Guarda un usuario en la base de datos
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    # Obtiene un usuario por su nombre de usuario
    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()