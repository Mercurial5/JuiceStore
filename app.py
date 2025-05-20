from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Juice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.String(50), nullable=False)
    volume = db.Column(db.Float, nullable=False)


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    juice_id = db.Column(db.Integer, db.ForeignKey('juice.id'), nullable=False)

    user = db.Relationship('User', backref=db.backref('purchases', lazy=True))
    juice = db.Relationship('Juice', backref=db.backref('purchases', lazy=True))


with app.app_context():
    db.create_all()


@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    user = User(name=data['name'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User added', 'id': user.id})


@app.route('/juice', methods=['POST'])
def add_juice():
    data = request.get_json()
    juice = Juice(flavor=data['flavor'], volume=data['volume'])
    db.session.add(juice)
    db.session.commit()

    return jsonify({'message': 'Juice added', 'id': juice.id})


@app.route('/purchase', methods=['POST'])
def add_purchase():
    data = request.get_json()
    purchase = Purchase(user_id=data['user_id'], juice_id=data['juice_id'])
    db.session.add(purchase)
    db.session.commit()

    return jsonify({'message': 'Purchase completed', 'id': purchase.id})


@app.route('/purchases', methods=['GET'])
def list_purchases():
    purchases = Purchase.query.all()
    result = []
    for p in purchases:
        result.append({
            'id': p.id,
            'user': p.user.name,
            'juice': f"{p.juice.flavor},{p.juice.volume}L"
        })
    return jsonify(result)


@app.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_entry(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User {user_id} deleted'}), 200


@app.route('/')
def hello_world():  # put application'database.db code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
