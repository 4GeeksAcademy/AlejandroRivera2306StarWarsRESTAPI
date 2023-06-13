
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favoritos = relationship("Favorito", back_populates="user")

    def __repr__(self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, it's a security breach
        }


class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_planeta = db.Column(db.Integer, ForeignKey('planeta.id'))
    id_personaje = db.Column(db.Integer, ForeignKey('personaje.id'))
    id_user = db.Column(db.Integer, ForeignKey('user.id'))
    planeta = relationship("Planeta", back_populates="favoritos")
    personaje = relationship("Personaje", back_populates="favoritos")
    user = relationship("User", back_populates="favoritos")

    def __repr__(self):
        return '%r' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name_planeta": self.planeta.name,
            "name_personaje": self.personaje.name,
            # do not serialize the password, it's a security breach
        }


class Personaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    favoritos = relationship("Favorito", back_populates="personaje")

    def __repr__(self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            # do not serialize the password, it's a security breach
        }


class Planeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    favoritos = relationship("Favorito", back_populates="planeta")

    def __repr__(self):
        # return '<Planeta %r>' % self.id
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "climate": self.climate,
            # do not serialize the password, it's a security breach
        }
