import os
import secrets

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = 'mysql://xiaofeixia-dev:%40XiaoFeiXia2024@119.45.18.148:3306/xiaofeixia-dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(16)
    STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static')
    TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'templates')
