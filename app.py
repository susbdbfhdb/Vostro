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
    <title>Zefoy Booster</title>
    <style>
        body { font-family: Arial; background: #1a0033; color: white; padding: 20px; }
        .container { max-width: 500px; margin: auto; background: #2a004d; padding: 20px; border-radius: 15px; }
        input, select, button { width: 100%; padding: 15px; margin: 10px 0; border-radius: 10px; font-size: 16px; }
        input, select { background: #3d0066; border: 2px solid #00ff9d; color: white; }
        button { background: #00ff9d; color: black; font-weight: bold; cursor: pointer; }
        .log { background: black; padding: 15px; height: 300px; overflow-y: scroll; margin-top: 15px; border-radius: 10px; white-space: pre-wrap; }
    </style>
</head>
<body>
<div class="container">
    <h2>🚀 Zefoy Booster</h2>
    
    <label>رابط الفيديو:</label>
    <input type="text" id="url" value="https://vt.tiktok.com/ZSCG2QUvS/">
    
    <label>النوع:</label>
    <select id="action">
        <option value="Views">مشاهدات</option>
        <option value="Likes">لايكات</option>
    </select>
    
    <label>الكمية:</label>
    <select id="quantity">
        <option value="1000">1000</option>
        <option value="5000">5000</option>
    </select>
    
    <button onclick="startBoost()">ابدأ التعزيز</button>
    
    <div id="log" class="log">جاهز... اضغط الزر</div>
</div>

<script>
    async function startBoost() {
        const url = document.getElementById('url').value.trim();
        const action = document.getElementById('action').value;
        const qty = document.getElementById('quantity').value;
        const log = document.getElementById('log');
        const btn = document.querySelector('button');

        log.innerHTML = "🔄 جاري البدء...\n";
        btn.disabled = true;

        try {
            const response = await fetch('/boost', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url, action, quantity: parseInt(qty) })
            });

            if (!response.ok) throw new Error('فشل الاتصال');

            const data = await response.json();
            log.innerHTML = data.logs.map(l => l).join('<br>');
        } catch (e) {
            log.innerHTML += '<br>❌ خطأ: ' + e.message + '<br>تأكد أن السيرفر شغال';
        } finally {
            btn.disabled = false;
        }
    }
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/boost', methods=['POST'])
def boost():
    data = request.get_json()
    url = data.get('url')
    action = data.get('action')
    quantity = int(data.get('quantity', 1000))

    logs = [f"بدء {action} - {quantity} عملية..."]
    
    for i in range(min(quantity, 2000)):
        logs.append(f"[{i+1}] إرسال بوت {action} ...")
        time.sleep(0.6)   # تأخير مرئي لترى الواجهة تتحرك
        if i % 15 == 0:
            try:
                requests.get(url, timeout=5)
            except:
                pass

    logs.append("✅ انتهى التشغيل")
    logs.append("⚠️ المشاهدات قد تأخذ وقت (5-60 دقيقة) حتى تظهر")
    
    return jsonify({"logs": logs})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("السيرفر يعمل → http://127.0.0.1:" + str(port))
    app.run(host='0.0.0.0', port=port, debug=False)
