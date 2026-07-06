import os
import random
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# كود واجهة المستخدم HTML + CSS + JS مدمج بالكامل
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Developer Request Simulator</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; display: flex; justify-content: center; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%; max-width: 500px; }
        h2 { text-align: center; color: #333; margin-top: 0; }
        label { font-weight: bold; display: block; margin-top: 15px; margin-bottom: 5px; color: #555; }
        input, select { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-size: 14px; }
        button { width: 100%; padding: 12px; background-color: #28a745; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: bold; margin-top: 20px; cursor: pointer; }
        button:disabled { background-color: #6c757d; }
        .log-box { background: #222; color: #00ff00; padding: 15px; border-radius: 4px; height: 180px; overflow-y: auto; font-family: monospace; font-size: 13px; margin-top: 20px; white-space: pre-line; }
    </style>
</head>
<body>

<div class="container">
    <h2>Request Simulator Panel</h2>
    
    <label for="url">Target URL / Link:</label>
    <input type="text" id="url" placeholder="https://example.com">
    
    <label for="action">Select Action Type:</label>
    <select id="action">
        <option value="Followers">Followers</option>
        <option value="Likes">Likes</option>
        <option value="Comments">Comments</option>
        <option value="Shares">Shares</option>
        <option value="Views">Views</option>
        <option value="Saves">Saves</option>
    </select>
    
    <label for="quantity">Select Quantity:</label>
    <select id="quantity">
        <option value="1">1</option>
        <option value="10">10</option>
        <option value="100">100</option>
        <option value="1000">1000</option>
    </select>
    
    <button id="submitBtn" onclick="sendRequests()">Execute Requests</button>
    
    <label>Execution Logs:</label>
    <div id="logBox" class="log-box">System ready. Waiting for inputs...</div>
</div>

<script>
    async function sendRequests() {
        const url = document.getElementById('url').value;
        const action = document.getElementById('action').value;
        const quantity = document.getElementById('quantity').value;
        const logBox = document.getElementById('logBox');
        const btn = document.getElementById('submitBtn');
        
        if (!url.startsWith('http')) {
            logBox.innerText = "Error: Please enter a valid URL (starting with http:// or https://)";
            return;
        }
        
        btn.disabled = true;
        logBox.innerText = "Sending request to server... Please wait...\\n";
        
        try {
            const response = await fetch('/run-simulation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url, action, quantity })
            });
            
            const data = await response.json();
            logBox.innerText = data.logs.join('\\n');
        } catch (error) {
            logBox.innerText = "Failed to communicate with server: " + error;
        } finally {
            btn.disabled = false;
        }
    }
</script>
</body>
</html>
"""

# دالة محاكاة معالجة الروابط وإرسال الطلبات باختلاف الـ Sessions
def simulate_requests(target_url, action_type, quantity):
    logs = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    
    logs.append(f"Starting developer network check for: {action_type}")
    logs.append(f"Target Link: {target_url}")
    
    # حد أقصى للحماية من تجميد السيرفر أثناء المعالجة الآنية
    loop_count = min(int(quantity), 100) 
    
    for i in range(loop_count):
        # توليد معرف عشوائي لكل عملية لمحاكاة طلب منفصل
        mock_id = f"sess_{random.randint(100000, 999999)}"
        logs.append(f"[{i+1}/{loop_count}] Executing via Session: {mock_id}")
        
        try:
            # إرسال طلب فحص قياسي لرابط المستهدف لقراءة استجابة الخادم
            response = requests.get(target_url, headers=headers, timeout=5)
            logs.append(f" -> Server Status Output: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logs.append(f" -> Interrupted: {str(e)}")
            break
            
    logs.append("Simulation execution finished.")
    return logs

@app.route('/', methods=['GET'])
def index():
    # استدعاء الواجهة المدمجة مباشرة من النص دون الحاجة لملف خارجي
    return render_template_string(HTML_TEMPLATE)

@app.route('/run-simulation', methods=['POST'])
def run_simulation():
    data = request.json
    target_url = data.get('url')
    action_type = data.get('action')
    quantity = data.get('quantity')
    
    if not target_url or not target_url.startswith("http"):
        return jsonify({"success": False, "logs": ["Error: Invalid or missing URL."]}), 400
        
    execution_logs = simulate_requests(target_url, action_type, quantity)
    return jsonify({"success": True, "logs": execution_logs})

if __name__ == '__main__':
    # تهيئة المنفذ ليتوافق تلقائياً مع سيرفرات الاستضافة السحابية مثل Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
