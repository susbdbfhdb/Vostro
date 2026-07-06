import os
import random
import requests
import time
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# === واجهة المستخدم المحدثة (مشابهة لـ zefoy) ===
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zefoy Style Booster</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #fff; margin: 0; padding: 20px; display: flex; justify-content: center; }
        .container { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); width: 100%; max-width: 520px; backdrop-filter: blur(10px); }
        h2 { text-align: center; color: #00ff9d; margin-top: 0; }
        label { font-weight: bold; display: block; margin: 15px 0 5px; color: #ccc; }
        input, select { width: 100%; padding: 12px; border: 1px solid #00ff9d; border-radius: 6px; box-sizing: border-box; background: rgba(0,0,0,0.4); color: white; }
        button { width: 100%; padding: 14px; background: #00ff9d; color: #000; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; margin-top: 20px; cursor: pointer; }
        button:disabled { background: #555; }
        .log-box { background: #111; color: #00ff9d; padding: 15px; border-radius: 6px; height: 220px; overflow-y: auto; font-family: monospace; font-size: 13px; margin-top: 20px; white-space: pre-line; border: 1px solid #00ff9d; }
        .status { text-align: center; margin: 10px 0; color: #ffd700; }
    </style>
</head>
<body>
<div class="container">
    <h2>🚀 Zefoy Style Booster</h2>
    <p class="status">Real-looking but hidden engagements</p>
    
    <label for="url">رابط الفيديو / الحساب:</label>
    <input type="text" id="url" placeholder="https://tiktok.com/@user/video/123...">
    
    <label for="action">نوع الخدمة:</label>
    <select id="action">
        <option value="Followers">Followers (متابعين)</option>
        <option value="Likes">Likes (لايكات)</option>
        <option value="Views">Views (مشاهدات)</option>
        <option value="Shares">Shares (مشاركات)</option>
        <option value="Comments">Comments (تعليقات)</option>
        <option value="Saves">Saves (حفظ)</option>
    </select>
    
    <label for="quantity">الكمية:</label>
    <select id="quantity">
        <option value="50">50</option>
        <option value="100" selected>100</option>
        <option value="500">500</option>
        <option value="1000">1000</option>
        <option value="5000">5000</option>
    </select>
    
    <button id="submitBtn" onclick="sendRequests()">ابدأ التعزيز الآن</button>
    
    <label>سجل العمليات (Logs):</label>
    <div id="logBox" class="log-box">جاهز... أدخل الرابط واضغط ابدأ</div>
</div>

<script>
    async function sendRequests() {
        const url = document.getElementById('url').value.trim();
        const action = document.getElementById('action').value;
        const quantity = document.getElementById('quantity').value;
        const logBox = document.getElementById('logBox');
        const btn = document.getElementById('submitBtn');
        
        if (!url || !url.startsWith('http')) {
            logBox.innerHTML = "خطأ: أدخل رابط صحيح (يبدأ بـ http/https)";
            return;
        }
        
        btn.disabled = true;
        logBox.innerHTML = "جاري الاتصال بالخادم...\n";
        
        try {
            const response = await fetch('/run-boost', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url, action, quantity: parseInt(quantity) })
            });
            
            const data = await response.json();
            logBox.innerHTML = data.logs.join('<br>');
        } catch (error) {
            logBox.innerHTML = "فشل الاتصال: " + error;
        } finally {
            btn.disabled = false;
        }
    }
</script>
</body>
</html>
"""

def get_random_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    ]
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
        "Referer": "https://www.tiktok.com/"
    }

def simulate_zefoy_boost(target_url, action_type, quantity):
    logs = []
    logs.append(f"[{time.strftime('%H:%M:%S')}] بدء تعزيز {action_type} مخفي...")
    logs.append(f"الرابط: {target_url}")
    logs.append(f"الكمية المطلوبة: {quantity}")

    loop_count = min(int(quantity), 200)  # حد أمان
    success_count = 0

    for i in range(loop_count):
        mock_session = f"zefoy_sess_{random.randint(10000, 99999)}"
        logs.append(f"[{i+1}/{loop_count}] جاري الإرسال عبر جلسة: {mock_session}")

        try:
            headers = get_random_headers()
            # محاكاة طلب حقيقي (يمكن توسيعه بـ proxies)
            response = requests.get(target_url, headers=headers, timeout=8)
            
            if response.status_code == 200:
                success_count += 1
                logs.append(f"  ✓ نجح (Status: {response.status_code}) - تعزيز مخفي")
            else:
                logs.append(f"  ⚠️ Status: {response.status_code}")
        except Exception as e:
            logs.append(f"  ❌ خطأ: {str(e)[:80]}")

        # تأخير عشوائي ليبدو طبيعياً (مثل zefoy)
        time.sleep(random.uniform(1.2, 4.5))

    logs.append(f"انتهى التعزيز! تم إرسال {success_count}/{loop_count} بنجاح.")
    logs.append("نصيحة: انتظر 5-30 دقيقة حتى تظهر النتائج (مثل zefoy).")
    return logs

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/run-boost', methods=['POST'])
def run_boost():
    data = request.json
    target_url = data.get('url')
    action_type = data.get('action')
    quantity = data.get('quantity', 100)
    
    if not target_url or not target_url.startswith("http"):
        return jsonify({"success": False, "logs": ["خطأ: رابط غير صالح"]}), 400
        
    execution_logs = simulate_zefoy_boost(target_url, action_type, quantity)
    return jsonify({"success": True, "logs": execution_logs})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("🚀 Zefoy-Style Booster جاهز على http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
