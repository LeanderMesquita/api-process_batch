from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()
db_url = os.getenv('DB_URL')
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
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

@app.route('/api/users/batch', methods=['POST'])
def insert_data():
    data = request.json.get('payload', [])
    
    if not data:
        
        return jsonify({'error': 'No data in payload'}), 400
    
    session = Session()
    try:
        users = [User(**item['body']) for item in data]
        
        session.bulk_save_objects(users)
        session.commit()
        
       
        return jsonify({'message': 'Data successfully inserted'}), 200
    except Exception as e:
        session.rollback()
       
        return jsonify({'error': 'Failed to insert data', 'details': str(e)}), 500
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True)
