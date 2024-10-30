from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from jwt import ExpiredSignatureError, InvalidTokenError
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User, db
from app.utils import jwt_required_custom

bp = Blueprint('auth', __name__)


@bp.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        if not user.is_active:
            return jsonify({"msg": "Account is deactivated"}), 403

        access_token = create_access_token(identity=user.id)

        # 确定用户角色
        role = 'admin' if user.is_admin else 'user'

        return jsonify({
            "user": user.username,
            "role": role,
            "token": access_token
        }), 200
    return jsonify({"msg": "Bad username or password"}), 401


@bp.route('/api/auth/deactivate/<int:user_id>', methods=['POST'])
@jwt_required_custom
def deactivate_user(user_id):
    try:
        current_user = User.query.get(get_jwt_identity())
        if not current_user.is_admin:
            return jsonify({"msg": "Admin privileges required"}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": "User not found"}), 404

        user.is_active = False
        db.session.commit()
        return jsonify({"msg": "User deactivated successfully"}), 200
    except (ExpiredSignatureError, InvalidTokenError):
        return jsonify({"msg": "Login session expired"}), 440


@bp.route('/api/auth/activate/<int:user_id>', methods=['POST'])
@jwt_required_custom
def activate_user(user_id):
    try:
        current_user = User.query.get(get_jwt_identity())
        if not current_user.is_admin:
            return jsonify({"msg": "Admin privileges required"}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": "User not found"}), 404

        user.is_active = True
        db.session.commit()
        return jsonify({"msg": "User activated successfully"}), 200
    except (ExpiredSignatureError, InvalidTokenError):
        return jsonify({"msg": "Login session expired"}), 440


@bp.route('/api/auth/change-password', methods=['POST'])
@jwt_required_custom
def change_password():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"msg": "User not found"}), 404

        data = request.get_json()
        new_password = data.get('newPassword')

        if not new_password:
            return jsonify({"msg": "New password is required"}), 400

        user.password = generate_password_hash(new_password)
        db.session.commit()

        return jsonify({"msg": "Password changed successfully"}), 200
    except (ExpiredSignatureError, InvalidTokenError):
        return jsonify({"msg": "Login session expired"}), 440
