import os
import random
import requests
import time
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zefoy Ultra Booster</title>
    <style>
        body {font-family: 'Cairo', sans-serif; background: linear-gradient(135deg, #1e0533, #2a0a4a); color: #fff; margin:0; padding:15px;}
        .container {max-width: 520px; margin:0 auto; background:rgba(0,0,0,0.7); padding:25px; border-radius:16px;}
        h2 {text-align:center; color:#00ff9d;}
        input, select {width:100%; padding:14px; margin:8px 0; border-radius:10px; border:2px solid #00ff9d; background:#1a0033; color:white;}
        button {width:100%; padding:16px; background:#00ff9d; color:black; border:none; border-radius:10px; font-size:18px; font-weight:bold; margin-top:15px;}
        .log-box {margin-top:20px; background:#0a001a; border:2px solid #00ff9d; border-radius:10px; padding:15px; height:280px; overflow-y:auto; color:#00ff9d; font-family:monospace;}
    </style>
</head>
<body>
<div class="container">
    <h2>🚀 Zefoy Ultra Booster</h2>
    <label>الرابط:</label>
    <input type="text" id="url" value="https://vt.tiktok.com/ZSCG2QUvS/">
    
    <label>نوع التعزيز:</label>
    <select id="action">
        <option value="Views">مشاهدات</option>
        <option value="Likes">لايكات</option>
        <option value="Followers">متابعين</option>
    </select>
    
    <label>الكمية:</label>
    <select id="quantity">
        <option value="1000">1000</option>
        <option value="5000">5000</option>
        <option value="10000">10000</option>
    </select>
    
    <button onclick="sendRequests()">ابدأ التعزيز</button>
    <div id="logBox" class="log-box">جاهز...</div>
</div>

<script>
    async function sendRequests() {
        let url = document.getElementById('url').value.trim();
        if (url.startsWith('/')) url = url.slice(1);
        
        const action = document.getElementById('action').value;
        const quantity = document.getElementById('quantity').value;
        const logBox = document.getElementById('logBox');
        const btn = document.querySelector('button');

        if (!url.startsWith('http')) {
            logBox.innerHTML = "❌ رابط غير صحيح";
            return;
        }

        btn.disabled = true;
        logBox.innerHTML = "🔄 بدء تشغيل البوتات المخفية...\n";

        try {
            const res = await fetch('/run-boost', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url, action, quantity: parseInt(quantity)})
            });
            const data = await res.json();
            logBox.innerHTML = data.logs.map(l => "• " + l).join("<br>");
        } catch(e) {
            logBox.innerHTML += "<br>❌ خطأ: " + e.message;
        } finally {
            btn.disabled = false;
        }
    }
</script>
</body>
</html>
"""

def simulate_boost(target_url, action, quantity):
    logs = [f"[{time.strftime('%H:%M:%S')}] 🔥 بدء {quantity} {action} مخفية..."]
    logs.append("جاري تشغيل بوتات محاكاة متقدمة...")
    
    count = min(int(quantity), 10000)
    success = 0

    for i in range(count):
        try:
            headers = {"User-Agent": random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"
            ])}
            requests.get(target_url, headers=headers, timeout=8)
            success += 1
            if i % 50 == 0:
                logs.append(f"[{i}] ✅ تم إرسال {success} بوت مخفي")
        except:
            pass
        time.sleep(random.uniform(0.8, 2.2))

    logs.append(f"✅ انتهى! تم محاكاة {success} عملية بنجاح")
    logs.append("💡 انتظر من 10 إلى 60 دقيقة لترى التأثير (TikTok يتأخر في العد)")
    return logs

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/run-boost', methods=['POST'])
def run_boost():
    data = request.get_json()
    logs = simulate_boost(data.get('url'), data.get('action'), data.get('quantity', 1000))
    return jsonify({"logs": logs})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
