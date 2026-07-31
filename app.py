import os
import json
import time
from flask import Flask, render_template, Response, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models_db import db, User, AlertEvent
from camera import VideoCamera
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-fire-smoke'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- DATABASE SETUP ---
with app.app_context():
    db.create_all()
    # Tạo user admin mặc định nếu chưa có
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        hashed_pw = generate_password_hash('123456')
        new_admin = User(username='admin', password=hashed_pw)
        db.session.add(new_admin)
        db.session.commit()

# --- CAMERA GLOBAL INSTANCE ---
# Hàm callback khi phát hiện khói/lửa
def save_alert_to_db(alert_type, confidence, image_path):
    with app.app_context():
        new_alert = AlertEvent(alert_type=alert_type, confidence=confidence, image_path=image_path)
        db.session.add(new_alert)
        db.session.commit()

# Chỉ khởi tạo camera khi cần thiết (để tránh lỗi khởi tạo nhiều lần)
video_camera = None

def get_camera():
    global video_camera
    if video_camera is None:
        video_camera = VideoCamera(alert_callback=save_alert_to_db)
    return video_camera

# --- ROUTES ---
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Sai tên đăng nhập hoặc mật khẩu!', 'error')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    recent_alerts = AlertEvent.query.order_by(desc(AlertEvent.id)).limit(5).all()
    return render_template('dashboard.html', recent_alerts=recent_alerts)

@app.route('/history')
@login_required
def history():
    alerts = AlertEvent.query.order_by(desc(AlertEvent.id)).all()
    return render_template('history.html', alerts=alerts)

@app.route('/stats')
@login_required
def stats():
    fire_count = AlertEvent.query.filter_by(alert_type='FIRE').count()
    smoke_count = AlertEvent.query.filter_by(alert_type='SMOKE').count()
    return render_template('stats.html', fire_count=fire_count, smoke_count=smoke_count)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    global video_camera
    settings_file = 'settings.json'
    
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            config = json.load(f)
    else:
        config = {"camera_source": "0"}
        
    if request.method == 'POST':
        new_source = request.form.get('camera_source')
        config['camera_source'] = new_source
        with open(settings_file, 'w') as f:
            json.dump(config, f)
            
        # Restart camera stream with new source
        if video_camera is not None:
            del video_camera
            video_camera = None
            
        flash('Đã cập nhật nguồn camera thành công!', 'success')
        return redirect(url_for('settings'))
        
    return render_template('settings.html', current_source=config['camera_source'])

# --- API ENDPOINTS ---
def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            time.sleep(0.1)

@app.route('/video_feed')
@login_required
def video_feed():
    return Response(gen(get_camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/latest_alert')
@login_required
def latest_alert():
    latest = AlertEvent.query.order_by(desc(AlertEvent.id)).first()
    if latest:
        return jsonify(latest.to_dict())
    return jsonify({})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
