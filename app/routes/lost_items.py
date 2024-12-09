from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import or_
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime
from sqlalchemy.orm import joinedload

from app.models import LostItem
from app import db
from app.utils import jwt_required_custom, get_current_time

bp = Blueprint('lost_items', __name__)


@bp.route('/api/lost_items', methods=['GET'])
@jwt_required_custom
def get_lost_items():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    status = request.args.get('status')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    search = request.args.get('search')

    query = LostItem.query.options(joinedload(LostItem.item_type_rel))

    if status:
        query = query.filter(LostItem.status == status)

    if start_date and end_date:
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        query = query.filter(LostItem.created_at.between(start_datetime, end_datetime))

    if search:
        search_term = f"%{search}%"
        query = query.filter(or_(
            LostItem.id.ilike(search_term),
            LostItem.name.ilike(search_term),
            LostItem.public_info.ilike(search_term),
            LostItem.private_info.ilike(search_term),
            LostItem.found_location.ilike(search_term)
        ))

    total = query.count()
    items = query.order_by(LostItem.created_at.desc()).paginate(page=page, per_page=page_size, error_out=False)

    return jsonify({
        'items': [item.to_dict() for item in items.items],
        'total': total
    }), 200


@bp.route('/api/lost_items', methods=['POST'])
@jwt_required_custom
def create_lost_item():
    data = request.get_json()
    data.pop('updater_username', None)

    new_id, new_type_id = LostItem.generate_new_id(data['item_type'])

    data['id'] = new_id
    data['type_id'] = new_type_id
    data['created_by'] = get_jwt_identity()
    data['updated_by'] = get_jwt_identity()
    data['created_at'] = get_current_time()
    data['updated_at'] = get_current_time()

    new_item = LostItem(**data)
    db.session.add(new_item)
    db.session.commit()

    return jsonify(new_item.to_dict()), 201


@bp.route('/api/lost_items/<string:id>', methods=['PUT'])
@jwt_required_custom
def update_lost_item(id):
    item = LostItem.query.get_or_404(id)
    data = request.get_json()
    data.pop('updater_username', None)

    # 如果 item_type 发生变化，重新生成 id 和 type_id
    if data.get('item_type') and data['item_type'] != item.item_type:
        new_id, new_type_id = LostItem.generate_new_id(data['item_type'])
        data['id'] = new_id
        data['type_id'] = new_type_id

    for key, value in data.items():
        if key not in ['updated_at', 'updated_by']:
            setattr(item, key, value)

    item.updated_by = get_jwt_identity()
    item.updated_at = get_current_time()
    db.session.commit()
    return jsonify(item.to_dict()), 200


@bp.route('/api/lost_items/<string:id>', methods=['DELETE'])
@jwt_required_custom
def delete_lost_item(id):
    item = LostItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return '', 204
