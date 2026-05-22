import os
import requests
from datetime import datetime, timedelta, timezone

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
OPENID = os.getenv("OPENID")

def get_access_token():
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": APP_ID,
        "secret": APP_SECRET
    }
    r = requests.get(url, params=params, timeout=15).json()
    return r.get("access_token")

def get_day_index():
    beijing_tz = timezone(timedelta(hours=8))
    today = datetime.now(beijing_tz).date()
    start_day = datetime(2026, 1, 1, tzinfo=beijing_tz).date()
    return (today - start_day).days % 30 + 1  # 1~30循环

def get_plan():
    # 30天场景标题（可继续扩展）
    titles = {
        1: "起床与晨间准备", 2: "通勤（地铁/公交）", 3: "办公室日常", 4: "午餐点餐",
        5: "咖啡店", 6: "超市购物", 7: "做饭", 8: "健身房",
        9: "医院就诊", 10: "银行办理业务", 11: "打电话", 12: "酒店入住",
        13: "机场值机", 14: "问路", 15: "天气交流", 16: "周末计划",
        17: "看电影", 18: "网购与快递", 19: "家庭清洁", 20: "宠物照顾",
        21: "社交寒暄", 22: "会议表达", 23: "做演示", 24: "请假与调休",
        25: "餐厅投诉与反馈", 26: "维修报修", 27: "租房沟通", 28: "节日与邀请",
        29: "复盘总结", 30: "综合复习日"
    }
    return titles

def build_content(day):
    titles = get_plan()
    title = titles.get(day, "生活英语")

    # 通用模板（每天不同场景名）
    words = [
        "schedule 日程", "habit 习惯", "prepare 准备", "comfortable 舒服的", "improve 提升",
        "repeat 重复", "review 复习", "remember 记住", "practice 练习", "progress 进步"
    ]
    sentences = [
        f"Today’s topic is {title}.",
        "I will learn new words and review yesterday’s notes.",
        "Small daily practice leads to big progress."
    ]

    # 简单复习机制：复习前1天/3天/7天
    d1 = day - 1 if day - 1 >= 1 else 30
    d3 = day - 3 if day - 3 >= 1 else 30 + (day - 3)
    d7 = day - 7 if day - 7 >= 1 else 30 + (day - 7)

    review = f"复习任务：回顾 Day {d1}、Day {d3}、Day {d7} 的3个单词，并各造1句。"

    msg = f"""Day {day}｜{title}

【词汇10个】
- {words[0]}
- {words[1]}
- {words[2]}
- {words[3]}
- {words[4]}
- {words[5]}
- {words[6]}
- {words[7]}
- {words[8]}
- {words[9]}

【句子3句】
1) {sentences[0]}
2) {sentences[1]}
3) {sentences[2]}

【复习】
{review}

【打卡】
今天我已完成：单词✅ 句子✅ 复习✅
"""
    return msg

def send_text_message(access_token, content):
    url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={access_token}"
    payload = {
        "touser": OPENID,
        "msgtype": "text",
        "text": {"content": content}
    }
    r = requests.post(url, json=payload, timeout=15).json()
    return r

def main():
    token = get_access_token()
    if not token:
        print("获取access_token失败")
        return
    day = get_day_index()
    content = build_content(day)
    result = send_text_message(token, content)
    print("发送结果：", result)

if __name__ == "__main__":
    main()
