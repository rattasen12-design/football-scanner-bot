def search_fixture_by_name(team_query):
    """
    ระบบค้นหาอัจฉริยะ: ตัดคำและค้นหาบางส่วนจากชื่อทีมใน API จริง
    ป้องกันปัญหาพิมพ์ติดรหัสราคาหรือตัวหนังสือพิเศษ
    """
    url = f"https://{API_HOST}/fixtures"
    today_date = datetime.utcnow().strftime('%Y-%m-%d')
    querystring = {"date": today_date}

    try:
        response = requests.get(url, headers=HEADERS, params=querystring, timeout=10)
        if response.status_code == 200:
            matches = response.json().get('response', [])
            
            # ทำความสะอาดคำค้นหา ตัดเอาเฉพาะตัวอักษรที่เกี่ยวข้อง
            clean_query = team_query.lower()
            
            for match in matches:
                home_team = match['teams']['home']['name'].lower()
                away_team = match['teams']['away']['name'].lower()
                home_original = match['teams']['home']['name']
                away_original = match['teams']['away']['name']
                
                # เช็กว่าคำที่พิมพ์ค้นหามีอยู่ในชื่อทีมเหย้าหรือทีมเยือนหรือไม่
                if home_team in clean_query or away_team in clean_query or any(word in clean_query for word in home_team.split()) or any(word in clean_query for word in away_team.split()):
                    raw_date_str = match['fixture']['date']
                    match_time = parse_utc_to_thai_time(raw_date_str)
                    return {
                        "found": True,
                        "id": match['fixture']['id'],
                        "name": f"{home_original} vs {away_original}",
                        "home_team": home_original,
                        "away_team": away_original,
                        "league": match['league']['name'],
                        "time": f"เวลา {match_time} น."
                    }
    except Exception as e:
        print(f"Search API Error: {e}")

    return {"found": False}
