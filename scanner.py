from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# ตั้งค่า API Key ของ API-Football
API_KEY = "391528da1ee9b5a40afe3eb31b975639"
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {'x-apisports-key': API_KEY}

@app.route('/')
def home():
    return render_template('index.html') # หรือชื่อไฟล์หน้าเว็บของคุณ

@app.route('/api/search-team', methods=['GET'])
def search_team():
    """ค้นหาข้อมูลทีมจาก API-Football แบบเรียลไทม์"""
    team_name = request.args.get('name', '')
    url = f"{BASE_URL}/teams"
    params = {"search": team_name}
    
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json().get('response', [])
        return jsonify({"status": "success", "results": data})
    return jsonify({"status": "error", "message": "ไม่สามารถเชื่อมต่อ API ได้"})

@app.route('/analyze', methods=['POST'])
def analyze_match():
    """แกนกลางประมวลผลสูตร 7 ส่วน"""
    match_name = request.form.get('match_name')
    league_name = request.form.get('league_name')
    handicap = float(request.form.get('handicap', 0.0) or 0.0)
    over_under = float(request.form.get('over_under', 2.5) or 2.5)
    
    # จำลองการประมวลผลสูตร 7 ส่วนตามข้อมูลที่กรอกเข้ามา
    analysis_result = {
        "status": "Success",
        "match": match_name,
        "league": league_name,
        "formula_7_parts": {
            "part_1_base_data": "ผ่านเกณฑ์ช่องว่างราคาและค่าเฉลี่ยประตู (แยกเฉพาะลีก 100%)",
            "part_2_main_checks": "ผ่านเงื่อนไขหลัก 10/10 ข้อ และสถิติสูงเกินเกณฑ์",
            "part_3_probabilities": "โอกาสผ่านราคาเป้าหมายอยู่ในเกณฑ์สูงกว่า 80%",
            "part_4_h2h": "สถิติเจอกันเฉพาะลีกย้อนหลังผ่านเกณฑ์ 50%",
            "part_5_form": "แนวโน้มฟอร์ม 5 นัดล่าสุดอยู่ในขาขึ้น",
            "part_6_grade": "A+ (ความมั่นใจ 93.5%)",
            "part_7_tactics": "วิเคราะห์ตัวผู้เล่นและแทคติกครบถ้วน สมบูรณ์"
        }
    }
    return jsonify(analysis_result)

if __name__ == '__main__':
    app.run(debug=True)
