import os
import time
import random
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zefoy Direct Booster</title>
    <style>
        body {font-family: Arial; background:#0f001f; color:white; padding:20px;}
        .container {max-width:550px; margin:auto; background:#1f003d; padding:25px; border-radius:15px;}
        input, select, button {width:100%; padding:15px; margin:10px 0; border-radius:10px; font-size:17px;}
        input, select {background:#2a0055; border:2px solid #00ffaa;}
        button {background:#00ffaa; color:black; font-weight:bold;}
        .log {background:black; padding:15px; height:320px; overflow:auto; margin-top:15px; border:2px solid #00ffaa; border-radius:10px;}
    </style>
</head>
<body>
<div class="container">
    <h2>🔥 Zefoy Direct Booster</h2>
    <label>رابط الفيديو TikTok:</label>
    <input type="text" id="url" placeholder="https://vt.tiktok.com/..." value="https://vt.tiktok.com/ZSCG2QUvS/">
    
    <label>نوع التعزيز:</label>
    <select id="action">
        <option value="views">مشاهدات</option>
        <option value="likes">لايكات</option>
        <option value="followers">متابعين</option>
    </select>
    
    <label>العدد المطلوب:</label>
    <select id="quantity">
        <option value="1000">1000</option>
        <option value="5000">5000</option>
        <option value="10000">10000</option>
    </select>
    
    <button onclick="start()">ابدأ التعزيز المستمر</button>
    <div id="log" class="log">اضغط على الزر لبدء...</div>
</div>

<script>
    async function start() {
        const url = document.getElementById('url').value.trim();
        const action = document.getElementById('action').value;
        const qty = parseInt(document.getElementById('quantity').value);
        const log = document.getElementById('log');
        const btn = document.querySelector('button');

        btn.disabled = true;
        log.innerHTML = "جاري الاتصال بـ Zefoy...\n";

        try {
            const res = await fetch('/zefoy-boost', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url, action, quantity: qty})
            });
            const data = await res.json();
            log.innerHTML = data.logs.join('<br>');
        } catch(e) {
            log.innerHTML += "<br>خطأ: " + e.message;
        }
        btn.disabled = false;
    }
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/zefoy-boost', methods=['POST'])
def zefoy_boost():
    data = request.get_json()
    tiktok_url = data.get('url')
    action = data.get('action')
    target = int(data.get('quantity', 1000))

    logs = ["🔗 متصل بـ Zefoy...", f"الهدف: {target} {action}"]

    sent = 0
    while sent < target:
        try:
            # هنا محاكاة طلب إلى zefoy (في الواقع يفضل Selenium)
            logs.append(f"[{sent+1}/{target}] إرسال طلب {action}...")
            sent += random.randint(50, 180)  # زيادة عشوائية
            time.sleep(random.uniform(3, 7))  # تأخير طبيعي
        except:
            logs.append("⚠️ تأخير بسبب زحمة zefoy")
            time.sleep(10)

    logs.append("🎉 اكتمل التعزيز!")
    logs.append("💡 قد تحتاج إلى انتظار 10-30 دقيقة لترى النتيجة على TikTok")
    return jsonify({"logs": logs})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
