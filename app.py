from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///portfolio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from sqlalchemy.pool import NullPool

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "poolclass": NullPool
}

db = SQLAlchemy(app)


# Update CORS to allow your Vercel frontend
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "https://portfolio-frontend-eight-iota.vercel.app"
        ]
    }
})

# Database Models
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))
    tags = db.Column(db.Text)  # Store as JSON string
    status = db.Column(db.String(50))
    imageUrl = db.Column(db.String(500))
    demoUrl = db.Column(db.String(500))
    githubUrl = db.Column(db.String(500))
    date = db.Column(db.String(20))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'tags': json.loads(self.tags) if self.tags else [],
            'status': self.status,
            'imageUrl': self.imageUrl,
            'demoUrl': self.demoUrl,
            'githubUrl': self.githubUrl,
            'date': self.date
        }

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=False)
    credentialUrl = db.Column(db.String(500))
    imageUrl = db.Column(db.String(500))
    date = db.Column(db.String(20))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'issuer': self.issuer,
            'description': self.description,
            'credentialUrl': self.credentialUrl,
            'imageUrl': self.imageUrl,
            'date': self.date
        }

class Accomplishment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))
    imageUrl = db.Column(db.String(500))
    date = db.Column(db.String(20))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'imageUrl': self.imageUrl,
            'date': self.date
        }

# Initialize database and add sample data
with app.app_context():
    db.create_all()
    
    # Add sample data only if tables are empty
    if Project.query.count() == 0:
        sample_project = Project(
            title='E-Commerce Platform',
            description='A full-stack e-commerce solution with payment integration and inventory management.',
            category='Web Development',
            tags=json.dumps(['React', 'Node.js', 'MongoDB', 'Stripe']),
            status='completed',
            imageUrl='https://images.unsplash.com/photo-1661956602116-aa6865609028?w=800&q=80',
            demoUrl='https://demo.example.com',
            githubUrl='https://github.com/example',
            date='2024-10'
        )
        db.session.add(sample_project)
    
    if Certificate.query.count() == 0:
        sample_cert = Certificate(
            title='AWS Certified Solutions Architect',
            issuer='Amazon Web Services',
            description='Professional certification for designing distributed systems on AWS.',
            credentialUrl='https://aws.amazon.com/verification',
            imageUrl='https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800&q=80',
            date='2024-08'
        )
        db.session.add(sample_cert)
    
    if Accomplishment.query.count() == 0:
        sample_acc = Accomplishment(
            title='Hackathon Winner - TechCrunch Disrupt',
            description='First place winner for developing an innovative AI-powered code review tool.',
            category='Competition',
            imageUrl='https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&q=80',
            date='2024-09'
        )
        db.session.add(sample_acc)
    
    db.session.commit()

# ============= PROJECTS ENDPOINTS =============

@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([p.to_dict() for p in projects])

@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get(project_id)
    if project:
        return jsonify(project.to_dict())
    return jsonify({'error': 'Project not found'}), 404

@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    
    if not data.get('title') or not data.get('description'):
        return jsonify({'error': 'Title and description are required'}), 400
    
    new_project = Project(
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category', 'Other'),
        tags=json.dumps(data.get('tags', [])),
        status=data.get('status', 'in-progress'),
        imageUrl=data.get('imageUrl', ''),
        demoUrl=data.get('demoUrl', ''),
        githubUrl=data.get('githubUrl', ''),
        date=data.get('date', datetime.now().strftime('%Y-%m'))
    )
    
    db.session.add(new_project)
    db.session.commit()
    
    return jsonify(new_project.to_dict()), 201

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    project = Project.query.get(project_id)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    data = request.get_json()
    
    project.title = data.get('title', project.title)
    project.description = data.get('description', project.description)
    project.category = data.get('category', project.category)
    project.tags = json.dumps(data.get('tags', json.loads(project.tags) if project.tags else []))
    project.status = data.get('status', project.status)
    project.imageUrl = data.get('imageUrl', project.imageUrl)
    project.demoUrl = data.get('demoUrl', project.demoUrl)
    project.githubUrl = data.get('githubUrl', project.githubUrl)
    project.date = data.get('date', project.date)
    
    db.session.commit()
    
    return jsonify(project.to_dict())

@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = Project.query.get(project_id)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    db.session.delete(project)
    db.session.commit()
    
    return jsonify({'message': 'Project deleted successfully'})

# ============= CERTIFICATES ENDPOINTS =============

@app.route('/api/certificates', methods=['GET'])
def get_certificates():
    certificates = Certificate.query.all()
    return jsonify([c.to_dict() for c in certificates])

@app.route('/api/certificates/<int:cert_id>', methods=['GET'])
def get_certificate(cert_id):
    certificate = Certificate.query.get(cert_id)
    if certificate:
        return jsonify(certificate.to_dict())
    return jsonify({'error': 'Certificate not found'}), 404

@app.route('/api/certificates', methods=['POST'])
def create_certificate():
    data = request.get_json()
    
    if not data.get('title') or not data.get('description'):
        return jsonify({'error': 'Title and description are required'}), 400
    
    new_certificate = Certificate(
        title=data.get('title'),
        issuer=data.get('issuer', ''),
        description=data.get('description'),
        credentialUrl=data.get('credentialUrl', ''),
        imageUrl=data.get('imageUrl', ''),
        date=data.get('date', datetime.now().strftime('%Y-%m'))
    )
    
    db.session.add(new_certificate)
    db.session.commit()
    
    return jsonify(new_certificate.to_dict()), 201

@app.route('/api/certificates/<int:cert_id>', methods=['PUT'])
def update_certificate(cert_id):
    certificate = Certificate.query.get(cert_id)
    
    if not certificate:
        return jsonify({'error': 'Certificate not found'}), 404
    
    data = request.get_json()
    
    certificate.title = data.get('title', certificate.title)
    certificate.issuer = data.get('issuer', certificate.issuer)
    certificate.description = data.get('description', certificate.description)
    certificate.credentialUrl = data.get('credentialUrl', certificate.credentialUrl)
    certificate.imageUrl = data.get('imageUrl', certificate.imageUrl)
    certificate.date = data.get('date', certificate.date)
    
    db.session.commit()
    
    return jsonify(certificate.to_dict())

@app.route('/api/certificates/<int:cert_id>', methods=['DELETE'])
def delete_certificate(cert_id):
    certificate = Certificate.query.get(cert_id)
    
    if not certificate:
        return jsonify({'error': 'Certificate not found'}), 404
    
    db.session.delete(certificate)
    db.session.commit()
    
    return jsonify({'message': 'Certificate deleted successfully'})

# ============= ACCOMPLISHMENTS ENDPOINTS =============

@app.route('/api/accomplishments', methods=['GET'])
def get_accomplishments():
    accomplishments = Accomplishment.query.all()
    return jsonify([a.to_dict() for a in accomplishments])

@app.route('/api/accomplishments/<int:acc_id>', methods=['GET'])
def get_accomplishment(acc_id):
    accomplishment = Accomplishment.query.get(acc_id)
    if accomplishment:
        return jsonify(accomplishment.to_dict())
    return jsonify({'error': 'Accomplishment not found'}), 404

@app.route('/api/accomplishments', methods=['POST'])
def create_accomplishment():
    data = request.get_json()
    
    if not data.get('title') or not data.get('description'):
        return jsonify({'error': 'Title and description are required'}), 400
    
    new_accomplishment = Accomplishment(
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category', 'Other'),
        imageUrl=data.get('imageUrl', ''),
        date=data.get('date', datetime.now().strftime('%Y-%m'))
    )
    
    db.session.add(new_accomplishment)
    db.session.commit()
    
    return jsonify(new_accomplishment.to_dict()), 201

@app.route('/api/accomplishments/<int:acc_id>', methods=['PUT'])
def update_accomplishment(acc_id):
    accomplishment = Accomplishment.query.get(acc_id)
    
    if not accomplishment:
        return jsonify({'error': 'Accomplishment not found'}), 404
    
    data = request.get_json()
    
    accomplishment.title = data.get('title', accomplishment.title)
    accomplishment.description = data.get('description', accomplishment.description)
    accomplishment.category = data.get('category', accomplishment.category)
    accomplishment.imageUrl = data.get('imageUrl', accomplishment.imageUrl)
    accomplishment.date = data.get('date', accomplishment.date)
    
    db.session.commit()
    
    return jsonify(accomplishment.to_dict())

@app.route('/api/accomplishments/<int:acc_id>', methods=['DELETE'])
def delete_accomplishment(acc_id):
    accomplishment = Accomplishment.query.get(acc_id)
    
    if not accomplishment:
        return jsonify({'error': 'Accomplishment not found'}), 404
    
    db.session.delete(accomplishment)
    db.session.commit()
    
    return jsonify({'message': 'Accomplishment deleted successfully'})

# ============= HEALTH CHECK =============

@app.route('/')
def index():
    return jsonify({
        'message': 'Portfolio API is running',
        'status': 'ok',
        'endpoints': {
            'projects': '/api/projects',
            'certificates': '/api/certificates',
            'accomplishments': '/api/accomplishments'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)