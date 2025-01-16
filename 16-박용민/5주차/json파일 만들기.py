import json

data = {
    "person": "John",
    "email": "John@bikecorporation.me",
    "subject": "“ZENESIS” bike distribution cooperation and meeting schedule proposal",
    "summary": "John, Senior Executive Director at Bike Corporation, requests a detailed brochure for the ZENESIS model, including technical specifications, battery performance, and design aspects. He proposes a meeting to discuss collaboration possibilities on Tuesday, January 15th, at 10:00 AM at Kim's office.",
    "date": "Tuesday, January 15th, at 10:00 AM"
}

# JSON 파일로 저장
with open("meeting_schedule.json", "w") as file:
    json.dump(data, file, indent=4)