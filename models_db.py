from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class AlertEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(50), nullable=False)  # FIRE or SMOKE
    confidence = db.Column(db.Integer, nullable=False)     # Tỷ lệ %
    image_path = db.Column(db.String(255), nullable=True)  # Tên file ảnh đã lưu
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'alert_type': self.alert_type,
            'confidence': self.confidence,
            'image_path': self.image_path,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
