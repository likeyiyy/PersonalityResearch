from flask import Blueprint, request, jsonify
from ..services.character_service import CharacterService
from ..database import get_db

character_api = Blueprint('character', __name__)

@character_api.route('/api/characters', methods=['GET'])
def get_characters():
    db = get_db()
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 10))
        category = request.args.get('category', '')
        
        service = CharacterService(db)
        result = service.get_characters_page(page, page_size, category)
        
        return jsonify(result)
    finally:
        db.close()

@character_api.route('/api/characters/categories', methods=['GET'])
def get_character_categories():
    db = get_db()
    try:
        service = CharacterService(db)
        category_tree = service.get_category_stats()
        return jsonify(category_tree)
    finally:
        db.close() 