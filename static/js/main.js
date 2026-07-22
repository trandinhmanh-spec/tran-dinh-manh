let lastAlertId = 0;
let isPolling = false;

// Âm thanh cảnh báo
const alarmSound = new Audio('/static/sounds/alarm.mp3'); 
// (Cần có 1 file âm thanh thực tế trong static/sounds, hoặc dùng Web Audio API để phát bíp bíp)

function playBeep() {
    // Dùng Web Audio API để phát âm thanh Bíp đơn giản nếu không có mp3
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    osc.type = 'square';
    osc.frequency.setValueAtTime(1000, ctx.currentTime);
    osc.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 1);
}

function showPopup(type, confidence) {
    let popup = document.getElementById('global-popup');
    if (!popup) {
        popup = document.createElement('div');
        popup.id = 'global-popup';
        popup.className = 'popup-notification';
        document.body.appendChild(popup);
    }
    
    popup.innerHTML = `
        <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>
        <span>CẢNH BÁO PHÁT HIỆN ${type} (${confidence}%)</span>
    `;
    
    // Đổi màu tuỳ theo Khói hay Lửa
    if (type === 'SMOKE') {
        popup.classList.add('smoke-alert');
    } else {
        popup.classList.remove('smoke-alert');
    }
    
    // Hiện popup
    setTimeout(() => popup.classList.add('show'), 100);
    
    // Tự tắt sau 4 giây
    setTimeout(() => {
        popup.classList.remove('show');
    }, 4000);
}

function checkLatestAlert() {
    fetch('/api/latest_alert')
        .then(res => res.json())
        .then(data => {
            if (data.id && data.id !== lastAlertId) {
                // Có cảnh báo mới
                if (lastAlertId !== 0) { // Không báo lúc mới load trang
                    if (data.alert_type === 'FIRE') {
                        playBeep();
                        showPopup('FIRE', data.confidence);
                    } else if (data.alert_type === 'SMOKE') {
                        showPopup('SMOKE', data.confidence);
                    }
                    
                    // Nếu đang ở trang dashboard, reload list cảnh báo
                    if (window.location.pathname === '/dashboard') {
                        // Reload trang hoặc gọi API append vào list (đơn giản nhất là reload hoặc chờ người dùng f5)
                        // Để trải nghiệm tốt hơn, reload nhẹ phần alerts
                        window.location.reload(); 
                    }
                }
                lastAlertId = data.id;
                
                // Đổi trạng thái hiển thị
                const statusBadge = document.getElementById('system-status');
                if (statusBadge) {
                    statusBadge.className = 'status-badge status-warning';
                    statusBadge.innerHTML = 'Warning: ' + data.alert_type + ' Detected!';
                }
            }
        })
        .catch(err => console.error(err));
}

// Chạy polling 0.5 giây / lần (siêu nhạy)
if (window.location.pathname !== '/login' && window.location.pathname !== '/') {
    setInterval(checkLatestAlert, 500);
}
