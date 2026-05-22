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

def get_content(day):
    LESSONS = {
        1: {
            "title": "Day 1｜起床晨间",
            "words": "alarm, snooze, wake up, get up, brush teeth, shower, get dressed, breakfast",
            "sentences": [
                "My alarm went off at 6:30.",
                "I hit snooze once and got up at 6:40.",
                "I had a quick breakfast before work."
            ],
            "review": "开口：用3句描述你的早晨流程。"
        },
        2: {
            "title": "Day 2｜通勤",
            "words": "commute, traffic, crowded, delay, transfer, on time, subway, headphones",
            "sentences": [
                "I usually commute by subway.",
                "The train was delayed for ten minutes.",
                "I got to work just on time."
            ],
            "review": "复习Day1：用 alarm / breakfast 各造一句。"
        },
        3: {
            "title": "Day 3｜办公室寒暄",
            "words": "colleague, meeting, deadline, task, schedule, update, busy, break",
            "sentences": [
                "Good morning, how’s your day going?",
                "I have a meeting at ten.",
                "I’m a bit busy, but everything is on schedule."
            ],
            "review": "复习Day2：说出你的通勤方式+是否堵车。"
        },
        4: {
            "title": "Day 4｜午餐点餐",
            "words": "menu, order, spicy, mild, dish, bill, separate, recommend",
            "sentences": [
                "Could I see the menu, please?",
                "I’d like this dish, not too spicy.",
                "Could we get the bill, please?"
            ],
            "review": "复习Day3：用 meeting / deadline 说2句。"
        },
        5: {
            "title": "Day 5｜咖啡店",
            "words": "latte, medium, iced, hot, less sugar, takeaway, receipt, size",
            "sentences": [
                "Could I get a medium latte?",
                "I’d like it iced, less sugar.",
                "That’s all, thank you."
            ],
            "review": "复习Day4：完整说一次点餐。"
        },
        6: {
            "title": "Day 6｜超市购物",
            "words": "basket, aisle, discount, fresh, checkout, cashier, total, change",
            "sentences": [
                "Where can I find fresh milk?",
                "Is this item on discount?",
                "Can I pay by card?"
            ],
            "review": "复习Day5：用3句完成咖啡点单。"
        },
        7: {
            "title": "Day 7｜周复习1",
            "words": "review, repeat, remember, practice, improve, fluency, mistake, correct",
            "sentences": [
                "Practice makes your speaking more natural.",
                "It’s okay to make mistakes.",
                "I’m improving little by little."
            ],
            "review": "复习Day1-6：每个场景说1句。"
        },
        8: {
            "title": "Day 8｜打电话",
            "words": "call back, available, voicemail, hold, connection, signal, confirm, schedule",
            "sentences": [
                "Hi, is this a good time to talk?",
                "Could you call me back later?",
                "I’m calling to confirm tomorrow’s meeting."
            ],
            "review": "复习Day7：说你这一周进步。"
        },
        9: {
            "title": "Day 9｜开会表达",
            "words": "agenda, point, suggest, agree, disagree, clarify, summary, action item",
            "sentences": [
                "Let’s start with the first agenda item.",
                "I agree with your point.",
                "Could you clarify that part?"
            ],
            "review": "复习Day8：模拟一通工作电话。"
        },
        10: {
            "title": "Day 10｜请假沟通",
            "words": "day off, sick leave, request, approve, urgent, recover, handover, notice",
            "sentences": [
                "I’d like to request a day off tomorrow.",
                "I’m not feeling well today.",
                "I’ll hand over my tasks before I leave."
            ],
            "review": "复习Day9：用 agree/disagree 各说一句。"
        },
        11: {
            "title": "Day 11｜问路",
            "words": "direction, straight, turn left, turn right, corner, block, across from, near",
            "sentences": [
                "Excuse me, how can I get to the station?",
                "Go straight and turn left at the corner.",
                "It’s across from the bank."
            ],
            "review": "复习Day10：请假3句模板复述。"
        },
        12: {
            "title": "Day 12｜打车",
            "words": "driver, destination, route, traffic jam, fare, drop off, pickup, payment",
            "sentences": [
                "Please take me to this address.",
                "Could you avoid the highway?",
                "Please drop me off here."
            ],
            "review": "复习Day11：模拟问路对话。"
        },
        13: {
            "title": "Day 13｜餐厅问题反馈",
            "words": "overcooked, cold, salty, replace, refund, service, apologize, manager",
            "sentences": [
                "Excuse me, this dish is a bit cold.",
                "Could you replace it, please?",
                "Thank you for your help."
            ],
            "review": "复习Day12：说一次打车需求。"
        },
        14: {
            "title": "Day 14｜周复习2",
            "words": "confidence, expression, natural, pause, intonation, response, habit, progress",
            "sentences": [
                "I’m becoming more confident when speaking.",
                "Short daily practice really helps.",
                "I can express myself more clearly now."
            ],
            "review": "复习Day8-13：每个主题说1句。"
        },
        15: {
            "title": "Day 15｜酒店入住",
            "words": "reservation, check in, passport, room key, floor, breakfast included, checkout, receipt",
            "sentences": [
                "I have a reservation under Li.",
                "Could I check in now?",
                "What time is checkout tomorrow?"
            ],
            "review": "复习Day14：描述你的口语变化。"
        },
        16: {
            "title": "Day 16｜机场值机",
            "words": "boarding pass, luggage, gate, security check, delayed, window seat, aisle seat, passport",
            "sentences": [
                "I’d like a window seat, please.",
                "Where is the boarding gate?",
                "Is the flight on time?"
            ],
            "review": "复习Day15：酒店入住3句复述。"
        },
        17: {
            "title": "Day 17｜同事协作",
            "words": "collaborate, assign, priority, support, feedback, revise, deadline, status",
            "sentences": [
                "Can we split these tasks?",
                "This task is the top priority today.",
                "Could you give me feedback on this draft?"
            ],
            "review": "复习Day16：值机流程口述。"
        },
        18: {
            "title": "Day 18｜汇报进度",
            "words": "progress, complete, pending, issue, solution, estimate, deliver, update",
            "sentences": [
                "I’ve completed about 70 percent.",
                "We have one issue to solve.",
                "I’ll send an update by 5 p.m."
            ],
            "review": "复习Day17：协作常用句说2句。"
        },
        19: {
            "title": "Day 19｜社交寒暄",
            "words": "hobby, weekend, lately, interesting, recommend, relax, favorite, plan",
            "sentences": [
                "What do you usually do on weekends?",
                "I’ve been reading a lot lately.",
                "Do you have any recommendations?"
            ],
            "review": "复习Day18：做一个30秒进度汇报。"
        },
        20: {
            "title": "Day 20｜看病",
            "words": "symptom, fever, cough, sore throat, medicine, prescription, appointment, rest",
            "sentences": [
                "I’ve had a cough for three days.",
                "Do I need any medicine?",
                "I’ll get some rest and drink more water."
            ],
            "review": "复习Day19：聊一次周末计划。"
        },
        21: {
            "title": "Day 21｜周复习3",
            "words": "review, organize, recall, retell, shadowing, fluency, accuracy, consistency",
            "sentences": [
                "Consistency is more important than intensity.",
                "Retelling helps build fluency.",
                "I can speak more smoothly now."
            ],
            "review": "复习Day15-20：每个场景口述20秒。"
        },
        22: {
            "title": "Day 22｜网购与快递",
            "words": "order, shipment, tracking, delivered, return, exchange, package, address",
            "sentences": [
                "My package hasn’t arrived yet.",
                "Could you check the tracking number?",
                "I’d like to return this item."
            ],
            "review": "复习Day21：说你如何坚持练习。"
        },
        23: {
            "title": "Day 23｜租房沟通",
            "words": "rent, deposit, contract, utility, maintenance, landlord, lease, repair",
            "sentences": [
                "How much is the monthly rent?",
                "Is the utility fee included?",
                "The sink is leaking. Could you repair it?"
            ],
            "review": "复习Day22：描述一次退货流程。"
        },
        24: {
            "title": "Day 24｜银行业务",
            "words": "account, transfer, balance, statement, fee, password, card, branch",
            "sentences": [
                "I’d like to open a bank account.",
                "Could you help me transfer money?",
                "What is my current balance?"
            ],
            "review": "复习Day23：询问租房3句。"
        },
        25: {
            "title": "Day 25｜健身房",
            "words": "workout, warm up, trainer, treadmill, strength, stretch, routine, membership",
            "sentences": [
                "I work out three times a week.",
                "I usually start with a warm-up.",
                "Could you show me the correct form?"
            ],
            "review": "复习Day24：模拟银行对话。"
        },
        26: {
            "title": "Day 26｜天气与出行",
            "words": "forecast, humid, temperature, storm, umbrella, cancel, reschedule, slippery",
            "sentences": [
                "The forecast says it will rain tonight.",
                "It’s too humid today.",
                "Let’s reschedule if the weather gets worse."
            ],
            "review": "复习Day25：说你的健身习惯。"
        },
        27: {
            "title": "Day 27｜邀请与拒绝",
            "words": "invite, available, unfortunately, maybe next time, appreciate, join, schedule, conflict",
            "sentences": [
                "Would you like to join us for dinner?",
                "I’d love to, but I have a schedule conflict.",
                "Thanks for the invitation."
            ],
            "review": "复习Day26：天气影响计划怎么说。"
        },
        28: {
            "title": "Day 28｜周复习4",
            "words": "summarize, scenario, expression, confidence, timing, respond, connect, polish",
            "sentences": [
                "I can respond faster in daily conversations.",
                "My vocabulary is becoming more practical.",
                "I just need to keep polishing my speaking."
            ],
            "review": "复习Day22-27：每个场景说2句。"
        },
        29: {
            "title": "Day 29｜综合口语1",
            "words": "situation, explain, compare, choose, reason, experience, challenge, solution",
            "sentences": [
                "Let me explain the situation briefly.",
                "I chose this option because it’s more practical.",
                "The main challenge was time."
            ],
            "review": "复习Day28：总结你本月进步。"
        },
        30: {
            "title": "Day 30｜综合口语2（收官）",
            "words": "goal, achievement, weakness, strategy, routine, confidence, continue, milestone",
            "sentences": [
                "My goal is to speak English more naturally.",
                "I’ve made steady progress this month.",
                "I will continue this routine next month."
            ],
            "review": "最终任务：做1分钟自我总结（学习内容+进步+下月目标）。"
        }
    }

    d = LESSONS.get(day, LESSONS[1])

    msg = f"""{d['title']}

【词汇】
{d['words']}

【句子】
1) {d['sentences'][0]}
2) {d['sentences'][1]}
3) {d['sentences'][2]}

【复习任务】
{d['review']}
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
