"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User , Planeta, Personaje, Favorito
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)
# aqui se empieza


@app.route('/user', methods=['GET'])
def handle_hello():
    all_user = User.query.all()
    print(all_user)
    result = list(map(lambda item: item.serialize(), all_user))
    response_body = {
        "msg": "Prueba "
    }

    return jsonify(result), 200

@app.route('/planeta', methods=['GET'])
def handle_helloone():
    all_planet = Planeta.query.all()
    print(all_planet)
    result = list(map(lambda item: item.serialize(), all_planet))
    response_body = {
        "msg": "Prueba planeta "
    }

    return jsonify(result), 200

@app.route('/planeta/<int:position>', methods=['GET'])
def planeta_uno(position):
    planeta = Planeta.query.get(position)
    if planeta:
        return jsonify(planeta.serialize())
    else:
        return jsonify({'message': 'Planeta no encontrado'}), 404
    

@app.route('/personaje', methods=['GET'])
def handle_hellotwo():
    all_personaje = Personaje.query.all()
    print(all_personaje)
    result = list(map(lambda item: item.serialize(), all_personaje))
    response_body = {
        "msg": "Prueba personaje "
    }

    return jsonify(result), 200

@app.route('/personaje/<int:position>', methods=['GET'])
def personaje_uno(position):
    personaje = Personaje.query.get(position)
    if personaje:
        return jsonify(personaje.serialize())
    else:
        return jsonify({'message': 'Personaje no encontrado'}), 404

@app.route('/favorito', methods=['GET'])
def handle_hellotres():
    all_favorito = Favorito.query.all()
    print(all_favorito)
    result = list(map(lambda item: item.serialize(), all_favorito))
    response_body = {
        "msg": "Prueba Favoritos "
    }

    return jsonify(result), 200

@app.route('/favorito/<int:position>', methods=['GET'])
def favorito_uno(position):
    favorito_one = Favorito.query.get(position)
    if favorito_one:
        return jsonify(favorito_one.serialize())
    else:
        return jsonify({'message': 'No se encontro los datos'}), 404


@app.route('/user/favorito/<int:position>', methods=['GET'])
def favoritos_usuario(position):
    usuario = User.query.get(position)
    if usuario:
        favoritos = usuario.favoritos
        return jsonify([favorito.serialize() for favorito in favoritos])
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    

@app.route('/favorito/planeta/<int:position>', methods=['POST'])
def crear_planeta_favorito(position):
    data = request.get_json()  # Obtener los datos enviados en el cuerpo de la solicitud POST
    user_id = data.get('id')  # Obtener el ID del usuario desde los datos
    
    usuario = User.query.get(user_id)  # Buscar el usuario por su ID
    if usuario:
        planeta = Planeta.query.get(position)  # Obtener el planeta por su ID
        if planeta:
            # Crear un nuevo favorito asociado al usuario y al planeta
            nuevo_favorito = Favorito(id_planeta=planeta.id, id_user=usuario.id)
            db.session.add(nuevo_favorito)
            db.session.commit()
            
            return jsonify({'message': 'Planeta favorito creado exitosamente.'}), 200
        else:
            return jsonify({'message': 'Planeta no encontrado'}), 404
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404


@app.route('/favorito/personaje/<int:position>', methods=['POST'])
def crear_personaje_favorito(position):
    data = request.get_json()  # Obtener los datos enviados en el cuerpo de la solicitud POST
    user_id = data.get('id')  # Obtener el ID del usuario desde los datos
    
    usuario = User.query.get(user_id)  # Buscar el usuario por su ID
    if usuario:
        personaje = Personaje.query.get(position)  # Obtener el planeta por su ID
        if personaje:
            # Crear un nuevo favorito asociado al usuario y al planeta
            nuevo_favorito = Favorito(id_personaje=personaje.id, id_user=usuario.id)
            db.session.add(nuevo_favorito)
            db.session.commit()
            
            return jsonify({'message': 'Personaje favorito creado exitosamente.'}), 200
        else:
            return jsonify({'message': 'Personaje no encontrado'}), 404
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    
    
@app.route('/favorito/personaje/<int:position>', methods=['DELETE'])
def eliminar_personaje_favorito(position):
    data = request.get_json()  # Obtener los datos enviados en el cuerpo de la solicitud DELETE
    user_id = data.get('id')  # Obtener el ID del usuario desde los datos
    
    usuario = User.query.get(user_id)  # Buscar el usuario por su ID
    if usuario:
        favorito = Favorito.query.filter_by(id_personaje=position, id_user=usuario.id).first()  # Buscar el favorito por el ID del personaje y el ID del usuario
        if favorito:
            db.session.delete(favorito)  # Eliminar el favorito de la base de datos
            db.session.commit()
            
            return jsonify({'message': 'Favorito eliminado exitosamente.'}), 200
        else:
            return jsonify({'message': 'Favorito no encontrado'}), 404
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

@app.route('/favorito/planeta/<int:position>', methods=['DELETE'])
def eliminar_planeta_favorito(position):
    data = request.get_json()  # Obtener los datos enviados en el cuerpo de la solicitud DELETE
    user_id = data.get('id')  # Obtener el ID del usuario desde los datos
    
    usuario = User.query.get(user_id)  # Buscar el usuario por su ID
    if usuario:
        favorito = Favorito.query.filter_by(id_planeta=position, id_user=usuario.id).first()  # Buscar el favorito por el ID del personaje y el ID del usuario
        if favorito:
            db.session.delete(favorito)  # Eliminar el favorito de la base de datos
            db.session.commit()
            
            return jsonify({'message': 'Favorito eliminado exitosamente.'}), 200
        else:
            return jsonify({'message': 'Favorito no encontrado'}), 404
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
