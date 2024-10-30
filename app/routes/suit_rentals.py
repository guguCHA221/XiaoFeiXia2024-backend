from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import or_
from app.models import SuitRental
from app import db
from app.utils import jwt_required_custom, get_current_time

bp = Blueprint('suit_rentals', __name__)


@bp.route('/api/suit_rentals', methods=['GET'])
@jwt_required_custom
def get_suit_rentals():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    status = request.args.get('status')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    search = request.args.get('search')

    query = SuitRental.query

    if status:
        query = query.filter(SuitRental.status == status)

    if start_date and end_date:
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        query = query.filter(SuitRental.rental_time.between(start_datetime, end_datetime))

    if search:
        search_term = f"%{search}%"
        query = query.filter(or_(
            SuitRental.suit_number.ilike(search_term),
            SuitRental.student_name.ilike(search_term),
            SuitRental.student_id.ilike(search_term)
        ))

    total = query.count()
    rentals = query.order_by(SuitRental.rental_time.desc()).paginate(page=page, per_page=page_size, error_out=False)

    return jsonify({
        'rentals': [rental.to_dict() for rental in rentals.items],
        'total': total
    }), 200


@bp.route('/api/suit_rentals', methods=['POST'])
@jwt_required_custom
def create_suit_rental():
    data = request.get_json()
    data.pop('creator_username', None)
    data.pop('updater_username', None)

    data['created_by'] = get_jwt_identity()
    data['updated_by'] = get_jwt_identity()
    data['created_at'] = get_current_time()
    data['updated_at'] = get_current_time()

    new_rental = SuitRental(**data)
    db.session.add(new_rental)
    db.session.commit()

    return jsonify(new_rental.to_dict()), 201


@bp.route('/api/suit_rentals/<string:id>', methods=['PUT'])
@jwt_required_custom
def update_suit_rental(id):
    rental = SuitRental.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        if key not in ['updated_at', 'updated_by', 'created_at']:
            setattr(rental, key, value)
    rental.updated_by = get_jwt_identity()
    rental.updated_at = get_current_time()
    print(rental)
    db.session.commit()
    return jsonify(rental.to_dict()), 200


@bp.route('/api/suit_rentals/<string:id>', methods=['DELETE'])
@jwt_required_custom
def delete_suit_rental(id):
    rental = SuitRental.query.get_or_404(id)
    db.session.delete(rental)
    db.session.commit()
    return '', 204
