from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    # ดึงวันที่ปัจจุบันแบบอัตโนมัติ
    now = datetime.datetime.now()
    today_str = now.strftime("%d/%m/%Y")
    
    # จำลองรายการแข่งขันสดประจำวัน (สามารถเปลี่ยนเป็นดึงจาก API หรือระบบสแกนได้ในอนาคต)
    matches = [
        {
            "match": "เรอัล มาดริด vs บาร์เซโลน่า",
            "league": "La Liga",
            "gap_score": "+0.85",
            "h2h_5": "80%",
            "h2h_10": "75%",
            "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"
        },
        {
            "match": "บาเยิร์น มิวนิค vs ดอร์ทมุนด์",
            "league": "Bundesliga",
            "gap_score": "+0.65",
            "h2h_5": "70%",
            "h2h_10": "80%",
            "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"
        },
        {
            "match": "ลิเวอร์พูล vs แมนเชสเตอร์ ซิตี้",
            "league": "Premier League",
            "gap_score": "+0.55",
            "h2h_5": "65%",
            "h2h_10": "70%",
            "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"
        }
    ]
    
    return render_template('index.html', matches=matches, update_time=today_str)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
