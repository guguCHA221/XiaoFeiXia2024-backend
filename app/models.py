from sqlalchemy import func

from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)


class LostItem(db.Model):
    __tablename__ = 'lost_items'
    id = db.Column(db.String(20), primary_key=True)
    item_type = db.Column(db.CHAR(1), db.ForeignKey('item_types.type_code'))
    type_id = db.Column(db.Integer)
    name = db.Column(db.String(100), nullable=False)
    public_info = db.Column(db.Text)
    private_info = db.Column(db.Text)
    found_location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('未领取', '已领取', '过期处理'), default='未领取')
    claimer_name = db.Column(db.String(50))
    claimer_student_id = db.Column(db.String(20))
    claimer_phone = db.Column(db.String(20))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    item_type_rel = db.relationship('ItemType', backref='lost_items')

    def to_dict(self):
        updater = User.query.get(self.updated_by) if self.updated_by else None
        return {
            'id': self.id,
            'item_type': self.item_type,
            'type_id': self.type_id,
            'name': self.name,
            'public_info': self.public_info,
            'private_info': self.private_info,
            'found_location': self.found_location,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status,
            'claimer_name': self.claimer_name,
            'claimer_student_id': self.claimer_student_id,
            'claimer_phone': self.claimer_phone,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'updater_username': updater.username if updater else None
        }

    @classmethod
    def generate_new_id(cls, item_type):
        # 查找同类型的最大type_id
        max_type_id = db.session.query(func.max(cls.type_id)).filter(cls.item_type == item_type).scalar()

        if max_type_id is None:
            new_type_id = 1
        else:
            new_type_id = max_type_id + 1

        # 生成新的ID
        new_id = f"{item_type}{new_type_id}"
        return new_id, new_type_id


class ItemType(db.Model):
    __tablename__ = 'item_types'
    type_code = db.Column(db.CHAR(1), primary_key=True)
    type_name = db.Column(db.String(20), nullable=False)
    current_sequence = db.Column(db.Integer, default=0)


class SuitRental(db.Model):
    __tablename__ = 'suit_rentals'
    id = db.Column(db.Integer, primary_key=True)
    suit_number = db.Column(db.String(50), nullable=False)
    student_name = db.Column(db.String(50), nullable=False)
    student_id = db.Column(db.String(20), nullable=False)
    contact_info = db.Column(db.String(50), nullable=False)
    rental_time = db.Column(db.DateTime, nullable=False)
    expected_return_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('已预约', '未归还', '已归还'), default='已预约')
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        updater = User.query.get(self.updated_by) if self.updated_by else None
        creator = User.query.get(self.created_by) if self.created_by else None
        return {
            'id': self.id,
            'suit_number': self.suit_number,
            'student_name': self.student_name,
            'student_id': self.student_id,
            'contact_info': self.contact_info,
            'rental_time': self.rental_time.isoformat() if self.rental_time else None,
            'expected_return_time': self.expected_return_time.isoformat() if self.expected_return_time else None,
            'status': self.status,
            'notes': self.notes,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'updater_username': updater.username if updater else None,
            'creator_username': creator.username if creator else None
        }