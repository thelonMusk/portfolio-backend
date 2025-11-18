from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)

# Update CORS to allow your Vercel frontend
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "https://portfolio-frontend-eight-iota.vercel.app"
        ]
    }
})

# Data files
PROJECTS_FILE = 'projects.json'
CERTIFICATES_FILE = 'certificates.json'
ACCOMPLISHMENTS_FILE = 'accomplishments.json'

# Helper functions for projects
def load_projects():
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_projects(projects):
    with open(PROJECTS_FILE, 'w') as f:
        json.dump(projects, f, indent=2)

# Helper functions for certificates
def load_certificates():
    if os.path.exists(CERTIFICATES_FILE):
        with open(CERTIFICATES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_certificates(certificates):
    with open(CERTIFICATES_FILE, 'w') as f:
        json.dump(certificates, f, indent=2)

# Helper functions for accomplishments
def load_accomplishments():
    if os.path.exists(ACCOMPLISHMENTS_FILE):
        with open(ACCOMPLISHMENTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_accomplishments(accomplishments):
    with open(ACCOMPLISHMENTS_FILE, 'w') as f:
        json.dump(accomplishments, f, indent=2)

# Initialize with sample data
if not os.path.exists(PROJECTS_FILE):
    sample_projects = [
        {
            'id': 1,
            'title': 'E-Commerce Platform',
            'description': 'A full-stack e-commerce solution with payment integration and inventory management.',
            'category': 'Web Development',
            'tags': ['React', 'Node.js', 'MongoDB', 'Stripe'],
            'status': 'completed',
            'imageUrl': 'https://images.unsplash.com/photo-1661956602116-aa6865609028?w=800&q=80',
            'demoUrl': 'https://demo.example.com',
            'githubUrl': 'https://github.com/example',
            'date': '2024-10'
        }
    ]
    save_projects(sample_projects)

if not os.path.exists(CERTIFICATES_FILE):
    sample_certificates = [
        {
            'id': 1,
            'title': 'AWS Certified Solutions Architect',
            'issuer': 'Amazon Web Services',
            'date': '2024-08',
            'credentialUrl': 'https://aws.amazon.com/verification',
            'description': 'Professional certification for designing distributed systems on AWS.',
            'imageUrl': 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800&q=80'
        }
    ]
    save_certificates(sample_certificates)

if not os.path.exists(ACCOMPLISHMENTS_FILE):
    sample_accomplishments = [
        {
            'id': 1,
            'title': 'Hackathon Winner - TechCrunch Disrupt',
            'date': '2024-09',
            'description': 'First place winner for developing an innovative AI-powered code review tool.',
            'category': 'Competition',
            'imageUrl': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&q=80'
        }
    ]
    save_accomplishments(sample_accomplishments)

# ============= PROJECTS ENDPOINTS =============

@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = load_projects()
    return jsonify(projects)

@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    projects = load_projects()
    project = next((p for p in projects if p['id'] == project_id), None)
    if project:
        return jsonify(project)
    return jsonify({'error': 'Project not found'}), 404

@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    
    if not data.get('title') or not data.get('description'):
        return jsonify({'error': 'Title and description are required'}), 400
    
    projects = load_projects()
    new_id = max([p['id'] for p in projects], default=0) + 1
    
    new_project = {
        'id': new_id,
        'title': data.get('title'),
        'description': data.get('description'),
        'category': data.get('category', 'Other'),
        'tags': data.get('tags', []),
        'status': data.get('status', 'in-progress'),
        'imageUrl': data.get('imageUrl', ''),
        'demoUrl': data.get('demoUrl', ''),
        'githubUrl': data.get('githubUrl', ''),
        'date': data.get('date', datetime.now().strftime('%Y-%m'))
    }
    
    projects.append(new_project)
    save_projects(projects)
    
    return jsonify(new_project), 201

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    data = request.get_json()
    projects = load_projects()
    
    project_index = next((i for i, p in enumerate(projects) if p['id'] == project_id), None)
    
    if project_index is None:
        return jsonify({'error': 'Project not found'}), 404
    
    projects[project_index].update({
        'title': data.get('title', projects[project_index]['title']),
        'description': data.get('description', projects[project_index]['description']),
        'category': data.get('category', projects[project_index]['category']),
        'tags': data.get('tags', projects[project_index]['tags']),
        'status': data.get('status', projects[project_index]['status']),
        'imageUrl': data.get('imageUrl', projects[project_index]['imageUrl']),
        'demoUrl': data.get('demoUrl', projects[project_index]['demoUrl']),
        'githubUrl': data.get('githubUrl', projects[project_index]['githubUrl']),
        'date': data.get('date', projects[project_index]['date'])
    })
    
    save_projects(projects)
    return jsonify(projects[project_index])

@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    projects = load_projects()
    project = next((p for p in projects if p['id'] == project_id), None)
    
    if project is None:
        return jsonify({'error': 'Project not found'}), 404
    
    projects = [p for p in projects if p['id'] != project_id]
    save_projects(projects)
    
    return jsonify({'message': 'Project deleted successfully'})

# ============= CERTIFICATES ENDPOINTS =============

@app.route('/api/certificates', methods=['GET'])
def get_certificates():
    certificates = load_certificates()
    return jsonify(certificates)

@app.route('/api/certificates/<int:cert_id>', methods=['GET'])
def get_certificate(cert_id):
    certificates = load_certificates()
    certificate = next((c for c in certificates if c['id'] == cert_id), None)
    if certificate:
        return jsonify(certificate)
    return jsonify({'error': 'Certificate not found'}), 404

@app.route('/api/certificates', methods=['POST'])
def create_certificate():
    data = request.get_json()
    
    if not data.get('title') or not data.get('description'):
        return jsonify({'error': 'Title and description are required'}), 400
    
    certificates = load_certificates()
    new_id = max([c['id'] for c in certificates], default=0) + 1
    
    new_certificate = {
        'id': new_id,
        'title': data.get('title'),
        'issuer': data.get('issuer', ''),
        'description': data.get('description'),
        'credentialUrl': data.get('credentialUrl', ''),
        'imageUrl': data.get('imageUrl', ''),
        'date': data.get('date', datetime.now().strftime('%Y-%m'))
    }
    
    certificates.append(new_certificate)
    save_certificates(certificates)
    
    return jsonify(new_certificate), 201

@app.route('/api/certificates/<int:cert_id>', methods=['PUT'])
def update_certificate(cert_id):
    data = request.get_json()
    certificates = load_certificates()
    
    cert_index = next((i for i, c in enumerate(certificates) if c['id'] == cert_id), None)
    
    if cert_index is None:
        return jsonify({'error': 'Certificate not found'}), 404
    
    certificates[cert_index].update({
        'title': data.get('title', certificates[cert_index]['title']),
        'issuer': data.get('issuer', certificates[cert_index]['issuer']),
        'description': data.get('description', certificates[cert_index]['description']),
        'credentialUrl': data.get('credentialUrl', certificates[cert_index]['credentialUrl']),
        'imageUrl': data.get('imageUrl', certificates[cert_index]['imageUrl']),
        'date': data.get('date', certificates[cert_index]['date'])
    })
    
    save_certificates(certificates)
    return jsonify(certificates[cert_index])

@app.route('/api/certificates/<int:cert_id>', methods=['DELETE'])
def delete_certificate(cert_id):
    certificates = load_certificates()
    certificate = next((c for c in certificates if c['id'] == cert_id), None)
    
    if certificate is None:
        return jsonify({'error': 'Certificate not found'}), 404
    
    certificates = [c for c in certificates if c['id'] != cert_id]
    save_certificates(certificates)
    
    return jsonify({'message': 'Certificate deleted successfully'})

# ============= ACCOMPLISHMENTS ENDPOINTS =============

@app.route('/api/accomplishments', methods=['GET'])
def get_accomplishments():
    accomplishments = load_accomplishments()
    return jsonify(accomplishments)

@app.route('/api/accomplishments/<int:acc_id>', methods=['GET'])
def get_accomplishment(acc_id):
    accomplishments = load_accomplishments()
    accomplishment = next((a for a in accomplishments if a['id'] == acc_id), None)
    if accomplishment:
        return jsonify(accomplishment)
    return jsonify({'error': 'Accomplishment not found'}), 404

@app.route('/api/accomplishments', methods=['POST'])
def create_accomplishment():
    data = request.get_json()
    
    if not data.get('title') or not data.get('description'):
        return jsonify({'error': 'Title and description are required'}), 400
    
    accomplishments = load_accomplishments()
    new_id = max([a['id'] for a in accomplishments], default=0) + 1
    
    new_accomplishment = {
        'id': new_id,
        'title': data.get('title'),
        'description': data.get('description'),
        'category': data.get('category', 'Other'),
        'imageUrl': data.get('imageUrl', ''),
        'date': data.get('date', datetime.now().strftime('%Y-%m'))
    }
    
    accomplishments.append(new_accomplishment)
    save_accomplishments(accomplishments)
    
    return jsonify(new_accomplishment), 201

@app.route('/api/accomplishments/<int:acc_id>', methods=['PUT'])
def update_accomplishment(acc_id):
    data = request.get_json()
    accomplishments = load_accomplishments()
    
    acc_index = next((i for i, a in enumerate(accomplishments) if a['id'] == acc_id), None)
    
    if acc_index is None:
        return jsonify({'error': 'Accomplishment not found'}), 404
    
    accomplishments[acc_index].update({
        'title': data.get('title', accomplishments[acc_index]['title']),
        'description': data.get('description', accomplishments[acc_index]['description']),
        'category': data.get('category', accomplishments[acc_index]['category']),
        'imageUrl': data.get('imageUrl', accomplishments[acc_index]['imageUrl']),
        'date': data.get('date', accomplishments[acc_index]['date'])
    })
    
    save_accomplishments(accomplishments)
    return jsonify(accomplishments[acc_index])

@app.route('/api/accomplishments/<int:acc_id>', methods=['DELETE'])
def delete_accomplishment(acc_id):
    accomplishments = load_accomplishments()
    accomplishment = next((a for a in accomplishments if a['id'] == acc_id), None)
    
    if accomplishment is None:
        return jsonify({'error': 'Accomplishment not found'}), 404
    
    accomplishments = [a for a in accomplishments if a['id'] != acc_id]
    save_accomplishments(accomplishments)
    
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