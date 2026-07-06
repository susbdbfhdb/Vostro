import os
import random
import requests
import time
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# === واجهة Zefoy Style (مُحدثة ومُصححة) ===
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
        .log-box { background: #111; color: #00ff9d; padding: 15px; border-radius: 6px; height: 260px; overflow-y: auto; font-family: monospace; font-size: 13px; margin-top: 20px; white-space: pre-line; border: 1px solid #00ff9d; }
    </style>
</head>
<body>
<div class="container">
    <h2>🚀 Zefoy Style Booster</h2>
    
    <label for="url">رابط الفيديو / الحساب:</label>
    <input type="text" id="url" value="https://vt.tiktok.com/ZSCG2QUvS/" placeholder="https://vt.tiktok.com/...">
    
    <label for="action">نوع الخدمة:</label>
    <select id="action">
        <option value="Views">Views (مشاهدات)</option>
        <option value="Likes">Likes (لايكات)</option>
        <option value="Followers">Followers (متابعين)</option>
        <option value="Shares">Shares (مشاركات)</option>
    </select>
    
    <label for="quantity">الكمية:</label>
    <select id="quantity">
        <option value="100">100</option>
        <option value="500">500</option>
        <option value="1000" selected>1000</option>
        <option value="5000">5000</option>
    </select>
    
    <button id="submitBtn" onclick="sendRequests()">ابدأ التعزيز</button>
    
    <label>سجل العمليات:</label>
    <div id="logBox" class="log-box">جاهز للعمل...</div>
</div>

<script>
    async function sendRequests() {
        const url = document.getElementById('url').value.trim();
        const action = document.getElementById('action').value;
        const quantity = document.getElementById('quantity').value;
        const logBox = document.getElementById('logBox');
        const btn = document.getElementById('submitBtn');
        
        if (!url.startsWith('http')) {
            logBox.innerHTML = "❌ أدخل رابط صحيح";
            return;
        }
        
        btn.disabled = true;
        logBox.innerHTML = "جاري الإرسال...\n";
        
        try {
            const response = await fetch('/run-boost', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url, action, quantity: parseInt(quantity) })
            });
            
            const data = await response.json();
            logBox.innerHTML = data.logs.join('<br>');
        } catch (error) {
            logBox.innerHTML = "❌ خطأ في الاتصال: " + error.message;
        } finally {
            btn.disabled = false;
        }
    }
</script>
</body>
</html>
"""

def get_random_headers():
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"
    ]
    return {"User-Agent": random.choice(ua_list)}

def simulate_zefoy_boost(target_url, action_type, quantity):
    logs = [f"[{time.strftime('%H:%M:%S')}] 🚀 بدء تعزيز {action_type}..."]
    logs.append(f"الرابط → {target_url}")
    
    count = min(int(quantity), 300)
    success = 0
    
    for i in range(count):
        logs.append(f"[{i+1}/{count}] جاري الإرسال...")
        try:
            resp = requests.get(target_url, headers=get_random_headers(), timeout=10)
            if resp.status_code == 200:
                success += 1
                logs.append(f"  ✅ نجح (Status {resp.status_code})")
            else:
                logs.append(f"  ⚠️ Status: {resp.status_code}")
        except Exception as e:
            logs.append(f"  ❌ {str(e)[:60]}")
        
        time.sleep(random.uniform(1.5, 3.8))
    
    logs.append(f"✅ انتهى! تم إرسال {success}/{count} بنجاح (مخفي)")
    return logs

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/run-boost', methods=['POST'])
def run_boost():
    data = request.get_json()
    target_url = data.get('url')
    action_type = data.get('action')
    quantity = data.get('quantity', 100)
    
    if not target_url or not target_url.startswith("http"):
        return jsonify({"logs": ["❌ رابط غير صالح"]})
    
    logs = simulate_zefoy_boost(target_url, action_type, quantity)
    return jsonify({"logs": logs})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"✅ الخادم يعمل على http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
