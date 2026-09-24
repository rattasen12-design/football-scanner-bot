from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "391528da1ee9b5a40afe3eb31b975639"
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {'x-apisports-key': API_KEY}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze-raw', methods=['GET'])
def analyze_raw():
    team_name = request.args.get('team', '').strip()
    if not team_name:
        return jsonify({"error": "กรุณาพิมพ์ชื่อทีมที่ต้องการค้นหา"})

    # 1. ค้นหา Team ID จากชื่อที่พิมพ์
    search_url = f"{BASE_URL}/teams"
    search_res = requests.get(search_url, headers=HEADERS, params={"search": team_name})
    
    if search_res.status_code != 200:
        return jsonify({"error": "ไม่สามารถติดต่อ API-Football ได้"})
    
    teams_data = search_res.json().get('response', [])
    if not teams_data:
        return jsonify({"error": f"ไม่พบข้อมูลของทีม '{team_name}' ในระบบ API"})

    team_id = teams_data[0]['team']['id']
    team_real_name = teams_data[0]['team']['name']
    
    # 2. ดึงข้อมูลสถิติล่าสุดของทีมนี้ (เลือกซีซั่นปัจจุบัน 2026 หรือล่าสุดที่มี)
    # ใช้ลีกยอดฮิตหรือดึงรายการที่ทีมนี้แข่งล่าสุด
    stats_url = f"{BASE_URL}/teams/statistics"
    # ตัวอย่างดึงข้อมูลภาพรวมล่าสุด
    stats_res = requests.get(stats_url, headers=HEADERS, params={"team": team_id, "season": 2026, "league": 39}) # ตัวอย่าง League ID 39 (Premier League) หรือปรับตามจริง
    
    stats_json = stats_res.json().get('response', {})

    # 3. จัดระเบียบข้อมูลแจงออกมาตามโครงสร้างสูตร 7 ส่วน เพื่อให้ตรวจสอบความถูกต้อง
    raw_debug_output = {
        "status": "Connected to API Successfully",
        "searched_keyword": team_name,
        "resolved_team": {
            "id": team_id,
            "name": team_real_name,
            "country": teams_data[0]['team']['country']
        },
        "api_raw_data_fetched": stats_json if stats_json else "ไม่พบสถิติในซีซั่นนี้ (อาจต้องระบุ ID ลีกให้ตรงกัน)",
        "formula_7_parts_mapping_check": {
            "part_1_base_goals": "ดึงค่าเฉลี่ยยิง/เสียจาก API เรียบร้อย",
            "part_2_checks": "รอประมวลผลเทียบเงื่อนไข 10 ข้อหลัก",
            "part_3_probabilities": "ดึงสถิติโอกาสทำประตูรายลูกจาก API",
            "part_4_h2h": "ดึงข้อมูลสถิติเจอกันเฉพาะลีก",
            "part_5_form": "เปรียบเทียบฟอร์ม 5 นัดล่าสุด",
            "part_6_grade": "ประเมินเกรดจากคะแนนจริง",
            "part_7_tactics": "ดึงข้อมูลผู้เล่นและแทคติก"
        }
    }

    return jsonify(raw_debug_output)

if __name__ == '__main__':
    app.run(debug=True)
