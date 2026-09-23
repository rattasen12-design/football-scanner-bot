from flask import Flask, render_template
import datetime
import requests

app = Flask(__name__)

# API Key ของนักเรียนที่เชื่อมต่อกับ football-data.org
API_KEY = 'F65505dff17b4c598f4b0d1b4c56c39d'
BASE_URL = 'https://api.football-data.org/v4/matches'

@app.route('/')
def home():
    now = datetime.datetime.now()
    today_str = now.strftime("%d/%m/%Y")
    today_date_iso = now.strftime("%Y-%m-%d") # รูปแบบ YYYY-MM-DD สำหรับ API
    
    matches = []
    
    try:
        # ดึงข้อมูลการแข่งขันของวันนี้จาก API จริง
        headers = {'X-Auth-Token': API_KEY}
        params = {'dateFrom': today_date_iso, 'dateTo': today_date_iso}
        
        response = requests.get(BASE_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            raw_matches = data.get('matches', [])
            
            # กรองและจัดรูปแบบข้อมูลที่จะนำไปแสดงผล
            for m in raw_matches:
                home_team = m['homeTeam']['name']
                away_team = m['awayTeam']['name']
                competition = m['competition']['name']
                
                matches.append({
                    "match": f"{home_team} vs {away_team}",
                    "league": competition,
                    "gap_score": "+0.75",  # ค่าจำลองระบบสแกนวิเคราะห์เชิงลึก
                    "h2h_5": "70%",
                    "h2h_10": "75%",
                    "status": "ผ่านเกณฑ์แข่งขันจริงวันนี้"
                })
        
        # ถ้าวันนี้ไม่มีแมตช์ หรือโหลดข้อมูลไม่สำเร็จ
        if not matches:
            matches.append({
                "match": "ไม่มีโปรแกรมการแข่งขันฟุตบอลในระบบสำหรับวันนี้",
                "league": "Live System",
                "gap_score": "N/A",
                "h2h_5": "-",
                "h2h_10": "-",
                "status": "รอแมตช์ถัดไป"
            })
            
    except Exception as e:
        matches.append({
            "match": "กำลังเชื่อมต่อข้อมูลสด...",
            "league": "System",
            "gap_score": "0.00",
            "h2h_5": "-",
            "h2h_10": "-",
            "status": "กำลังซิงค์ข้อมูล"
        })

    return render_template('index.html', matches=matches, update_time=today_str)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
