from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    today_str = datetime.datetime.now().strftime("%d/%m/%Y")
    
    matches = [
        {
            "match": "อาร์เซนอล vs เชลซี",
            "league": "Premier League",
            "gap_score": "+0.75",
            "h2h_5": "65%",
            "h2h_10": "75%",
            "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"
        },
        {
            "match": "อินเตอร์ มิลาน vs ยูเวนตุส",
            "league": "Serie A",
            "gap_score": "+0.50",
            "h2h_5": "60%",
            "h2h_10": "70%",
            "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"
        },
        {
            "match": "แอตเลติโก มาดริด vs บียาร์เรอัล",
            "league": "La Liga",
            "gap_score": "+0.40",
            "h2h_5": "55%",
            "h2h_10": "65%",
            "status": "ผ่านเกณฑ์เข้มงวด 6 ส่วน"
        }
    ]
    
    return render_template('index.html', matches=matches, update_time=today_str)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
