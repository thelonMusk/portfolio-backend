from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Simple file-based storage (use a real database in production)
DATA_FILE = 'projects.json'

def load_projects():
    """Load projects from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_projects(projects):
    """Save projects to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(projects, f, indent=2)

# Initialize with sample data if file doesn't exist
if not os.path.exists(DATA_FILE):
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
        },
        {
            'id': 2,
            'title': 'AI Chat Application',
            'description': 'Real-time chat application with AI-powered responses and sentiment analysis.',
            'category': 'AI/ML',
            'tags': ['Python', 'Flask', 'OpenAI', 'WebSocket'],
            'status': 'in-progress',
            'imageUrl': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80',
            'demoUrl': '',
            'githubUrl': 'https://github.com/example',
            'date': '2024-11'
        },
        {
            'id': 3,
            'title': 'Portfolio Website',
            'description': 'Modern portfolio website with interactive animations and smooth transitions.',
            'category': 'Web Development',
            'tags': ['React', 'Tailwind', 'Framer Motion'],
            'status': 'completed',
            'imageUrl': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80',
            'demoUrl': 'https://demo.example.com',
            'githubUrl': '',
            'date': '2024-09'
        }
    ]
    save_projects(sample_projects)

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    projects = load_projects()
    return jsonify(projects)

@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get a single project by ID"""
    projects = load_projects()
    project = next((p for p in projects if p['id'] == project_id), None)
    if project:
        return jsonify(project)
    return jsonify({'error': 'Project not found'}), 404

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    data = request.get_json()
    
    # Validate required fields
    if not data.get('title') or not data.get('description'):
        return jsonify({'error': 'Title and description are required'}), 400
    
    projects = load_projects()
    
    # Generate new ID
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
    """Update an existing project"""
    data = request.get_json()
    projects = load_projects()
    
    project_index = next((i for i, p in enumerate(projects) if p['id'] == project_id), None)
    
    if project_index is None:
        return jsonify({'error': 'Project not found'}), 404
    
    # Update project fields
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
    """Delete a project"""
    projects = load_projects()
    
    project = next((p for p in projects if p['id'] == project_id), None)
    
    if project is None:
        return jsonify({'error': 'Project not found'}), 404
    
    projects = [p for p in projects if p['id'] != project_id]
    save_projects(projects)
    
    return jsonify({'message': 'Project deleted successfully'})

@app.route('/api/projects/search', methods=['GET'])
def search_projects():
    """Search projects by query"""
    query = request.args.get('q', '').lower()
    category = request.args.get('category', 'all')
    
    projects = load_projects()
    
    # Filter by search query
    if query:
        projects = [p for p in projects if 
                   query in p['title'].lower() or 
                   query in p['description'].lower() or
                   any(query in tag.lower() for tag in p['tags'])]
    
    # Filter by category
    if category != 'all':
        projects = [p for p in projects if p['category'] == category]
    
    return jsonify(projects)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all unique categories"""
    projects = load_projects()
    categories = list(set(p['category'] for p in projects))
    return jsonify(categories)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get portfolio statistics"""
    projects = load_projects()
    
    stats = {
        'total': len(projects),
        'completed': len([p for p in projects if p['status'] == 'completed']),
        'in_progress': len([p for p in projects if p['status'] == 'in-progress']),
        'planned': len([p for p in projects if p['status'] == 'planned']),
        'categories': {}
    }
    
    # Count by category
    for project in projects:
        category = project['category']
        stats['categories'][category] = stats['categories'].get(category, 0) + 1
    
    return jsonify(stats)

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'message': 'Project Portfolio API',
        'version': '1.0',
        'endpoints': {
            'GET /api/projects': 'Get all projects',
            'GET /api/projects/<id>': 'Get project by ID',
            'POST /api/projects': 'Create new project',
            'PUT /api/projects/<id>': 'Update project',
            'DELETE /api/projects/<id>': 'Delete project',
            'GET /api/projects/search': 'Search projects',
            'GET /api/categories': 'Get all categories',
            'GET /api/stats': 'Get portfolio statistics'
        }
    })

if __name__ == '__main__':
    # Get port from environment variable (Render provides this)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)