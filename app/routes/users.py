from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc
from werkzeug.security import generate_password_hash
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from app.models import User
from app import db
from app.utils import jwt_required_custom

bp = Blueprint('users', __name__)


@bp.route('/api/users', methods=['GET'])
@jwt_required_custom
def get_users():
    try:
        users = User.query.order_by(desc(User.is_active), User.username).all()
        return jsonify({
            'users': [
                {
                    'id': user.id,
                    'username': user.username,
                    'is_admin': user.is_admin,
                    'is_active': user.is_active
                } for user in users
            ]
        }), 200
    except (ExpiredSignatureError, InvalidTokenError):
        return jsonify({"msg": "Login session expired"}), 440


@bp.route('/api/users/<int:id>', methods=['PUT'])
@jwt_required_custom
def update_user(id):
    try:
        user = User.query.get_or_404(id)
        data = request.get_json()
        current_user_id = get_jwt_identity()

        if current_user_id == user.id:
            return jsonify({"message": "Permission denied"}), 403

        if 'is_admin' in data:
            user.is_admin = data['is_admin']
        if 'is_active' in data:
            user.is_active = data['is_active']

        db.session.commit()

        return jsonify({
            'id': user.id,
            'username': user.username,
            'is_admin': user.is_admin,
            'is_active': user.is_active
        }), 200
    except (ExpiredSignatureError, InvalidTokenError):
        return jsonify({"msg": "Login session expired"}), 440


@bp.route('/api/users/batch', methods=['POST'])
@jwt_required_custom
def add_users():
    try:
        data = request.get_json()
        usernames = data.get('usernames', [])
        print(usernames)

        new_users = []
        for username in usernames:
            user = User(
                username=username,
                password=generate_password_hash(username),  # 使用用户名作为初始密码
                is_admin=False,
                is_active=True
            )
            db.session.add(user)
            new_users.append(user)

        db.session.commit()

        return jsonify({
            'users': [
                {
                    'id': user.id,
                    'username': user.username,
                    'is_admin': user.is_admin,
                    'is_active': user.is_active
                } for user in new_users
            ]
        }), 201
    except (ExpiredSignatureError, InvalidTokenError):
        return jsonify({"msg": "Login session expired"}), 440
