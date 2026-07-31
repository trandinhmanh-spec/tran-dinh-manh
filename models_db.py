from typing import Optional, Any
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(100), unique=True)
    password: Mapped[str] = mapped_column(db.String(100))

    def __init__(self, username: str, password: str, **kwargs: Any):
        # pyrefly: ignore [unexpected-keyword]
        super().__init__(username=username, password=password, **kwargs)

class AlertEvent(db.Model):
    __tablename__ = 'alert_event'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    alert_type: Mapped[str] = mapped_column(db.String(50))  # FIRE or SMOKE
    confidence: Mapped[int] = mapped_column()     # Tỷ lệ %
    image_path: Mapped[Optional[str]] = mapped_column(db.String(255), nullable=True)  # Tên file ảnh đã lưu
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now)

    def __init__(self, alert_type: str, confidence: int, image_path: Optional[str] = None, **kwargs: Any):
        # pyrefly: ignore [unexpected-keyword]
        super().__init__(alert_type=alert_type, confidence=confidence, image_path=image_path, **kwargs)

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'alert_type': self.alert_type,
            'confidence': self.confidence,
            'image_path': self.image_path,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }

