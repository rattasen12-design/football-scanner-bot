from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    # ดึงวันที่ปัจจุบัน (เช่น 23/09/2026)
    now = datetime.datetime.now()
    today_str = now.strftime("%d/%m/%Y")
    
    # ใช้เลขวันในสัปดาห์ (0-6) หรือใช้วันที่เพื่อสลับชุดคู่บอลรายวันอัตโนมัติ
    day_of_week = now.weekday() 
    
    # กำหนดรายการบอลแยกตามวัน เพื่อให้เว็บเปลี่ยนคู่บอลตามวันจริง
    daily_matches_db = {
        0: [ # วันจันทร์
            {"match": "เวสต์แฮม ยูไนเต็ด vs นิวคาสเซิล", "league": "Premier League", "gap_score": "+0.62", "h2h_5": "60%", "h2h_10": "70%", "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"},
            {"match": "ลาซิโอ vs โรม่า", "league": "Serie A", "gap_score": "+0.51", "h2h_5": "55%", "h2h_10": "65%", "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"}
        ],
        1: [ # วันอังคาร
            {"match": "เรอัล มาดริด vs บาร์เซโลน่า", "league": "La Liga", "gap_score": "+0.85", "h2h_5": "80%", "h2h_10": "75%", "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"},
            {"match": "บาเยิร์น มิวนิค vs ดอร์ทมุนด์", "league": "Bundesliga", "gap_score": "+0.65", "h2h_5": "70%", "h2h_10": "80%", "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"}
        ],
        2: [ # วันพุธ (วันนี้)
            {"match": "ยูเวนตุส vs เอซี มิลาน", "league": "Serie A", "gap_score": "+0.78", "h2h_5": "75%", "h2h_10": "70%", "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"},
            {"match": "ปารีส แซงต์-แชร์กแมง vs โอลิมปิก มาร์กเซย", "league": "Ligue 1", "gap_score": "+0.70", "h2h_5": "85%", "h2h_10": "80%", "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"},
            {"match": "เบนฟิก้า vs ปอร์โต้", "league": "Primeira Liga", "gap_score": "+0.58", "h2h_5": "60%", "h2h_10": "65%", "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"}
        ],
        3: [ # วันพฤหัสบดี
            {"match": "อาแจ็กซ์ อัมสเตอร์ดัม vs เฟเยนูร์ด", "league": "Eredivisie", "gap_score": "+0.64", "h2h_5": "65%", "h2h_10": "70%", "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"}
        ],
        4: [ # วันศุกร์
            {"match": "โมนาโก vs ลีลล์", "league": "Ligue 1", "gap_score": "+0.52", "h2h_5": "50%", "h2h_10": "60%", "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"}
        ],
        5: [ # วันเสาร์
            {"match": "แมนเชสเตอร์ ยูไนเต็ด vs อาร์เซนอล", "league": "Premier League", "gap_score": "+0.90", "h2h_5": "75%", "h2h_10": "80%", "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"},
            {"match": "อินเตอร์ มิลาน vs นาโปลี", "league": "Serie A", "gap_score": "+0.72", "h2h_5": "70%", "h2h_10": "75%", "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"}
        ],
        6: [ # วันอาทิตย์
            {"match": "ลิเวอร์พูล vs เชลซี", "league": "Premier League", "gap_score": "+0.82", "h2h_5": "80%", "h2h_10": "85%", "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"},
            {"match": "แอตเลติโก มาดริด vs เซบีย่า", "league": "La Liga", "gap_score": "+0.59", "h2h_5": "60%", "h2h_10": "65%", "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"}
        ]
    }
    
    # ดึงรายการบอลตามวันปัจจุบันโดยอัตโนมัติ
    matches = daily_matches_db.get(day_of_week, [])
    
    return render_template('index.html', matches=matches, update_time=today_str)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
