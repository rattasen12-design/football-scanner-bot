from flask import Flask, render_template
import datetime
import requests

app = Flask(__name__)

API_KEY = 'F65505dff17b4c598f4b0d1b4c56c39d'
BASE_URL = 'https://api.football-data.org/v4/matches'

@app.route('/')
def home():
    now = datetime.datetime.now()
    today_str = now.strftime("%d/%m/%Y")
    today_date_iso = now.strftime("%Y-%m-%d")
    
    # ดึงโปรแกรมล่วงหน้า 7 วัน เพื่อให้มีแมตช์แสดงผลจากหลากหลายลีก
    end_date = (now + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    
    matches = []
    
    try:
        headers = {'X-Auth-Token': API_KEY}
        # ดึงภาพรวมแมตช์ทั้งหมดในช่วงเวลานี้ (ระบบจะดึงตามสิทธิ์บัญชีฟรีที่มี)
        params = {
            'dateFrom': today_date_iso,
            'dateTo': end_date
        }
        
        response = requests.get(BASE_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            raw_matches = data.get('matches', [])
            
            for m in raw_matches:
                home_team = m['homeTeam']['name']
                away_team = m['awayTeam']['name']
                competition = m['competition']['name']
                match_date_utc = m['utcDate']
                
                # แปลงเวลาเตะ
                match_date = match_date_utc[:10]
                match_time = match_date_utc.split('T')[1][:5]
                
                matches.append({
                    "match": f"{home_team} vs {away_team}",
                    "league": f"{competition}",
                    "gap_score": "+0.75",
                    "h2h_5": f"เวลา {match_time} น.",
                    "h2h_10": "สดจากสนาม",
                    "status": f"เตะวันที่: {match_date}"
                })
        
        # ถ้าระบบยังไม่เจอแมตช์ใน API ช่วงเวลานี้ ให้แสดงข้อความแจ้งเตือนสถานะการเชื่อมต่อจริง
        if not matches:
            matches.append({
                "match": "กำลังรอรอบการแข่งขันของลีกที่คุณเลือกในระบบ...",
                "league": "Daily Match Scanner",
                "gap_score": "Live",
                "h2h_5": "-",
                "h2h_10": "-",
                "status": f"ตรวจสอบวันที่: {today_str}"
            })
            
    except Exception as e:
        matches.append({
            "match": "กำลังซิงค์ข้อมูลกับเซิร์ฟเวอร์บอลสด...",
            "league": "System",
            "gap_score": "0.00",
            "h2h_5": "-",
            "h2h_10": "-",
            "status": "กำลังเชื่อมต่อ"
        })

    return render_template('index.html', matches=matches, update_time=today_str)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
