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
    
    matches = []
    
    try:
        headers = {'X-Auth-Token': API_KEY}
        params = {'dateFrom': today_date_iso, 'dateTo': today_date_iso}
        
        response = requests.get(BASE_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            raw_matches = data.get('matches', [])
            
            for m in raw_matches:
                home_team = m['homeTeam']['name']
                away_team = m['awayTeam']['name']
                competition = m['competition']['name']
                
                matches.append({
                    "match": f"{home_team} vs {away_team}",
                    "league": competition,
                    "gap_score": "+0.82",
                    "status": "พร้อมแข่งวันนี้"
                })
        
        if not matches:
            matches.append({
                "match": "ยังไม่มีโปรแกรมในระบบวันนี้",
                "league": "TDedAi Live System",
                "gap_score": "N/A",
                "status": "รออัปเดตตาราง"
            })
            
    except Exception as e:
        matches.append({
            "match": "กำลังโหลดข้อมูล...",
            "league": "System",
            "gap_score": "0.00",
            "status": "เชื่อมต่อ"
        })

    return render_template('index.html', matches=matches, update_time=today_str)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
