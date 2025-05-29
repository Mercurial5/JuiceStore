from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///fallback.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-fallback-secret')

db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Juice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.String(50), nullable=False)
    volume = db.Column(db.Float, nullable=False)


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    juice_id = db.Column(db.Integer, db.ForeignKey('juice.id'), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    user = db.Relationship('User', backref=db.backref('purchases', lazy=True))
    juice = db.Relationship('Juice', backref=db.backref('purchases', lazy=True))


with app.app_context():
    db.create_all()


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=data['username'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Successfully registered'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_access_token(identity=user.id)
    return jsonify({'access_token': token})


@app.route('/juice', methods=['POST'])
def add_juice():
    data = request.get_json()
    juice = Juice(flavor=data['flavor'], volume=data['volume'])
    db.session.add(juice)
    db.session.commit()

    return jsonify({'message': 'Juice added', 'id': juice.id})

@app.route('/delivery', methods=['POST'])
@jwt_required()
def make_delivery():
    user_id = get_jwt_identity()
    data = request.get_json()

    delivery = Purchase(
        user_id = user_id,
        juice_id=data['juice_id'],
        address=data['address']
    )

    db.session.add(delivery)
    db.session.commit()
    return jsonify({'message': 'Delivery created', 'id': delivery.id})

@app.route('/my_deliveries', methods=['GET'])
@jwt_required()
def my_delivery():
    user_id = get_jwt_identity()
    deliveries = Purchase.query.filter_by(user_id=user_id).all()

    result = []
    for deli in deliveries:
        result.append({
            'id': deli.id,
            'juice': f"{deli.juice.flavor}{deli.juice.volume}",
            'address': deli.address
        })
    return jsonify(result)

# @app.route('/delete/<int:user_id>', methods=['DELETE'])
# def delete_entry(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({'error': 'User not found'}), 404
#
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({'message': f'User {user_id} deleted'}), 200


@app.route('/')
def hello_world():  # put application'database.db code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
