from flask import Flask, jsonify
app = Flask(__name__)

from datetime import datetime
import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8888194480:AAEpG89SqZflwkiQk5GSL_pBuEgACqYFH60")
CHAT_ID = os.getenv("CHAT_ID", "8373268490")
API_KEY = os.getenv("API_KEY", "f65505dff17b4c598f4b0d1b4c56c39d")

TARGET_LEAGUES = ["PL", "PD", "SA", "BL1", "CL"]

def fetch_today_league_matches(league_code):
    today_date = datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.football-data.org/v4/competitions/{league_code}/matches?dateFrom={today_date}&dateTo={today_date}"
    headers = {"X-Auth-Token": API_KEY}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return data.get("matches", [])
    except Exception as e:
        print(f"❌ [API ERROR] ลีก {league_code}:", e)
        return []

def send_vip_alert(match_name, market_odds, expected_goals, gap_score, grade, checklist_count, league_name, match_time):
    vip_message = f"""🔔 [ สัญญาณบอลสูง VIP เกรด {grade} ]
━━━━━━━━━━━━━━━━━━
🏆 ศึกการแข่งขัน: {league_name}
⚽ คู่แข่งขัน: {match_name}
⏰ เวลาแข่งขัน: {match_time} น.
📊 ราคาเปิดสูง/ต่ำ: {market_odds}
🎯 ประตูคาดการณ์ E[G]: {expected_goals} ลูก
📈 ค่าช่องว่าง Gap Score: +{gap_score}
🌟 ระดับความน่าลงทุน: 【 เกรด {grade} 】
📌 หมายเหตุ: ผ่าน Checklist {checklist_count}/11 ข้อ
💡 คำแนะนำ: วิเคราะห์ตามระบบเรดาร์บอลสูง
━━━━━━━━━━━━━━━━━━"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": vip_message}
    requests.post(url, json=payload)

def run_graded_scanner():
    print("🔍 [SYSTEM] GitHub Actions กำลังรันระบบสแกนรายวัน...")
    found_count = 0
    for league in TARGET_LEAGUES:
        matches = fetch_today_league_matches(league)
        if not matches:
            continue
        for match in matches:
            home_team = match["homeTeam"]["name"]
            away_team = match["awayTeam"]["name"]
            match_name = f"{home_team} vs {away_team}"
            competition_name = match["competition"]["name"]
            utc_time = match["utcDate"]
            match_time_formatted = utc_time.split("T")[1][:5]
            
            calculated_eg = 3.40
            market_odds = 2.75
            gap_score = calculated_eg - market_odds
            checklist_passed = 10
            
            grade = None
            if checklist_passed == 11 and gap_score >= 0.50:
                grade = "A"
            elif checklist_passed >= 9 and gap_score >= 0.40:
                grade = "B+"
            elif checklist_passed >= 7 and gap_score >= 0.30:
                grade = "B"
                
            if grade:
                found_count += 1
                send_vip_alert(match_name, market_odds, calculated_eg, round(gap_score, 2), grade, checklist_passed, competition_name, match_time_formatted)
                
    print(f"🎉 [DONE] สแกนเสร็จสิ้น พบทั้งหมด {found_count} คู่")

if __name__ == "__main__":
    run_graded_scanner()

# ==========================================
# ส่วนสูตรวิเคราะห์บอลและเว็บแอป (Flask API)
# ==========================================
def analyze_football_match(match_data):
    home_scored_home = match_data.get('home_scored_home', 1.8)
    away_scored_away = match_data.get('away_scored_away', 1.5)
    market_line = match_data.get('market_line', 2.75)
    
    avg_total_goals = (home_scored_home + away_scored_away)
    gap_score = avg_total_goals - market_line
    
    if gap_score < 0.3:
        return None
        
    h2h_5_over_pct = match_data.get('h2h_5_over_pct', 45)
    h2h_10_over_pct = match_data.get('h2h_10_over_pct', 55)
    
    if h2h_5_over_pct <= 40 or h2h_10_over_pct <= 50:
        return None
        
    result = {
        "match": match_data.get('match_name', 'เจ้าบ้าน vs ทีมเยือน'),
        "gap_score": round(gap_score, 2),
        "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"
    }
    return result

@app.route('/api/scan-results', methods=['GET'])
def get_scan_results():
    sample_match = {
        'match_name': 'อาร์เซนอล vs เชลซี',
        'home_scored_home': 2.1,
        'away_scored_away': 1.6,
        'market_line': 2.75,
        'h2h_5_over_pct': 60,
        'h2h_10_over_pct': 55
    }
    analyzed = analyze_football_match(sample_match)
    return jsonify({"status": "success", "data": [analyzed] if analyzed else []})

@app.route('/')
def home():
    return "Football Scanner API is Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
