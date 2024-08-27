from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:leanderlopes87372661@localhost:5432/flask_api_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)  
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    
with app.app_context():    
    db.create_all()

def generator(list):
    for data in list:
        yield data


@app.route('/api/users/batch', methods=['POST'])
def process_batch():
    data = request.json
    
    if not data or 'payload' not in data:
        return jsonify({"error": "Payload inválido ou não encontrado"}), 400

    payload = data['payload']
    users_created = []
    errors = []
    
    
    

    for user_data in generator(payload):
        try:
            user_info = user_data.get("body")
            
            if not user_info:
                errors.append({"error": "Dados do usuário faltando", "data": user_data})
                continue

            new_user = User(
                name=user_info.get('name'),
                last_name=user_info.get('lastName'),
                email=user_info.get('email'),
                password=user_info.get('password'),
                role=user_info.get('role'),
                sector=user_info.get('sector'),
                state=user_info.get('state')
            )

            db.session.add(new_user)
            db.session.commit()
            users_created.append(new_user.id)

        except IntegrityError as e:
            db.session.rollback()
            errors.append({"error": str(e.orig), "data": user_info})
        except Exception as e:
            db.session.rollback()
            errors.append({"error": str(e), "data": user_info})

    return jsonify({
        "created_users": users_created,
        "errors": errors
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
