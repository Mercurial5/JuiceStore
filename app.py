from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class TestEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/add', methods=['POST'])
def add_entry():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'name is required'}), 400

    entry = TestEntry(name=name)
    db.session.add(entry)
    db.session.commit()
    return jsonify({'message': f'Added {name}'}), 201


@app.route('/delete/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    entry = TestEntry.query.get(entry_id)
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404

    db.session.delete(entry)
    db.session.commit()
    return jsonify({'message': f'Entry {entry_id} deleted'}), 200


@app.route('/entries', methods=['GET'])
def get_entries():
    entries = TestEntry.query.all()
    return jsonify([{'id': e.id, 'name': e.name} for e in entries])


@app.route('/')
def hello_world():  # put application'database.db code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
