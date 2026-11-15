# -*- coding: utf-8 -*-
"""
塔罗占卜工作台 MVP v1.0
功能：
1. 开始新占卜：录入客户/问题/牌面，自动生成"可粘贴给 AI"的解读提示词
   （老客户自动整合过往所有案例，无需翻聊天记录）
2. 补录客户反馈：回头客反馈随时补录，自动关联到对应案例
3. 查看历史：按客户名查看全部占卜档案
数据存于脚本同目录 tarot_workbench.db，提示词自动存档到 prompts_log.txt
运行方式：PyCharm 直接运行，或终端执行 python tarot_workbench.py
"""

import sqlite3
import os
import re
import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tarot_workbench.db")
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts_log.txt")

# ==================== 牌义关键词库 ====================

# 大阿卡纳（正/逆）
MAJOR = {
    "愚人":   {"正": "新开始、冒险、冲动、自由", "逆": "鲁莽、拖延、逃避责任"},
    "魔术师": {"正": "创造力、行动力、资源整合", "逆": "欺骗、能力不足、滥用才华"},
    "女祭司": {"正": "直觉、潜意识、静观其变", "逆": "忽视直觉、隐藏秘密、情绪化"},
    "皇后":   {"正": "丰盛、滋养、创造力落地", "逆": "过度依赖、停滞、挥霍"},
    "皇帝":   {"正": "权威、稳定、掌控局面", "逆": "专制、固执、失控"},
    "教皇":   {"正": "传统、指导、贵人相助", "逆": "教条、叛逆、打破常规"},
    "恋人":   {"正": "爱情、结合、重大选择", "逆": "分离、冲突、价值观不合"},
    "战车":   {"正": "意志力、胜利、坚定前进", "逆": "失控、受阻、方向迷失"},
    "力量":   {"正": "勇气、耐心、内在力量", "逆": "软弱、自我怀疑、冲动"},
    "隐士":   {"正": "独处、内省、寻求智慧", "逆": "孤立、逃避、过度保守"},
    "命运之轮": {"正": "转折、机遇、命运推动", "逆": "厄运、停滞、抗拒变化"},
    "正义":   {"正": "公正、平衡、理性决策", "逆": "不公、偏见、失衡"},
    "倒吊人": {"正": "换位思考、牺牲、静待时机", "逆": "无谓牺牲、拖延、固执"},
    "死神":   {"正": "结束、蜕变、放下旧局", "逆": "抗拒改变、停滞、拖延"},
    "节制":   {"正": "调和、耐心、适度", "逆": "失衡、过度、无节制"},
    "恶魔":   {"正": "欲望、束缚、沉迷", "逆": "挣脱、觉醒、戒断"},
    "高塔":   {"正": "剧变、崩塌、真相大白", "逆": "灾后重建、侥幸避免灾难"},
    "星星":   {"正": "希望、疗愈、灵感", "逆": "失望、失去信心、迷茫"},
    "月亮":   {"正": "不安、梦境、潜意识涌动", "逆": "拨云见日、直面恐惧"},
    "太阳":   {"正": "成功、喜悦、生命力", "逆": "过度乐观、短暂快乐"},
    "审判":   {"正": "觉醒、重生、召唤", "逆": "自我怀疑、错失机会"},
    "世界":   {"正": "圆满、完成、达成目标", "逆": "未完成、停滞、差一步"},
}

# 小阿卡纳：数字牌（1-10）关键词
MINOR = {
    "权杖": {  # 火 · 行动与热情
        "element": "火 · 行动与热情",
        "1": "新起点、灵感迸发、行动的火种",
        "2": "规划、权衡抉择、明确方向",
        "3": "扩张、协作、初见成果",
        "4": "稳定、庆祝、小有成就",
        "5": "竞争、冲突、内耗",
        "6": "胜利、被认可、声望",
        "7": "坚守立场、防守、勇气",
        "8": "迅速行动、进展、消息传来",
        "9": "坚守到底、警觉、独撑大局",
        "10": "负重前行、完成、过度负荷",
    },
    "圣杯": {  # 水 · 情感与关系
        "element": "水 · 情感与关系",
        "1": "新感情、情感萌芽、直觉涌现",
        "2": "结合、默契、互相吸引",
        "3": "友谊、庆祝、社交",
        "4": "倦怠、反思、意兴阑珊",
        "5": "失落、遗憾、回头看",
        "6": "怀旧、回忆、旧人旧事",
        "7": "幻想、选择过多、不切实际",
        "8": "离开旧境、追寻意义",
        "9": "愿望成真、满足、感恩",
        "10": "圆满、家庭幸福、情感丰盛",
    },
    "宝剑": {  # 风 · 思维与冲突
        "element": "风 · 思维与冲突",
        "1": "新想法、思路清晰、突破",
        "2": "纠结、僵局、两难",
        "3": "心碎、伤痛、真相刺痛",
        "4": "休整、暂停、给自己空间",
        "5": "冲突、胜负、伤人伤己",
        "6": "过渡、疗愈、离开困境",
        "7": "欺骗、偷偷行动、策略",
        "8": "束缚、困住、自我设限",
        "9": "焦虑、噩梦、过度担忧",
        "10": "结束、解脱、最坏已过",
    },
    "金币": {  # 土 · 金钱与现实
        "element": "土 · 金钱与现实",
        "1": "新机会、物质种子、财运起点",
        "2": "权衡、理财、时间管理",
        "3": "合作、技能、团队成果",
        "4": "守成、稳定、抓得太紧",
        "5": "困境、匮乏、患难见真情",
        "6": "给予、分享、接受帮助",
        "7": "等待、评估、投资回报",
        "8": "精进、劳作、打磨技艺",
        "9": "独立、丰盛、自给自足",
        "10": "传承、长期富足、家业",
    },
}

# 宫廷牌
COURT = {
    "权杖": {"侍从": "热情探索、新消息、跃跃欲试",
             "骑士": "冲劲十足、冒险行动、停不下来",
             "皇后": "自信魅力、热情大方、有感染力",
             "国王": "成熟领袖、远见、执行力强"},
    "圣杯": {"侍从": "敏感细腻、新感情讯号、想象力",
             "骑士": "浪漫追求、理想化、为爱奔走",
             "皇后": "温柔共情、疗愈者、情感丰沛",
             "国王": "情感成熟、沉稳包容、值得托付"},
    "宝剑": {"侍从": "机敏好奇、爱观察、口舌快",
             "骑士": "犀利直接、争辩、行动果断",
             "皇后": "独立理性、清醒冷静、界限分明",
             "国王": "权威冷静、逻辑主导、公正"},
    "金币": {"侍从": "踏实学习、新技能、务实",
             "骑士": "务实努力、稳步推进、可靠",
             "皇后": "丰盛滋养、会经营、接地气",
             "国王": "富足可靠、理财有成、大方"},
}

INVERSE_SUFFIX = "（逆位：受阻/过度/内在化，需转内求）"


def get_keywords(card_name, pos):
    """根据牌名与正逆位返回关键词，未收录时给出提示"""
    name = card_name.strip()
    if name in MAJOR:
        return MAJOR[name].get(pos, MAJOR[name]["正"])
    for suit, table in MINOR.items():
        if name.startswith(suit):
            rest = name[len(suit):]
            # 支持 "权杖一"、"权杖1"、数字牌与宫廷牌
            num = None
            for k in ["10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]:
                if rest in (k, "十" if k == "10" else {"1": "一", "2": "二", "3": "三", "4": "四", "5": "五",
                                                       "6": "六", "7": "七", "8": "八", "9": "九"}[k]):
                    num = k
                    break
            if num:
                kw = table[num]
                return kw + (INVERSE_SUFFIX if pos == "逆" else "")
            if rest in COURT[suit]:
                kw = COURT[suit][rest]
                return kw + (INVERSE_SUFFIX if pos == "逆" else "")
    return "（未收录此牌，可自行补充）"


def parse_cards(text):
    """解析牌面输入：'恋人 正, 宝剑三 逆' → [(牌名, 正/逆, 关键词), ...]"""
    text = text.replace("，", ",")
    parts = [p.strip() for p in text.split(",") if p.strip()]
    result = []
    for p in parts:
        m = re.match(r"^(.+?)[\s]*([正逆])(?:位)?$", p)
        if m:
            name, pos = m.group(1).strip(), m.group(2)
        else:
            name, pos = p, "正"
        kw = get_keywords(name, pos)
        result.append((name, pos, kw))
    return result


# ==================== 数据库 ====================

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        created_at TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        date TEXT,
        q_type TEXT,
        question TEXT,
        spread TEXT,
        cards TEXT,
        reading TEXT,
        feedback TEXT)""")
    conn.commit()
    conn.close()


def get_client_id(conn, name):
    c = conn.cursor()
    c.execute("SELECT id FROM clients WHERE name = ?", (name,))
    row = c.fetchone()
    if row:
        return row[0]
    c.execute("INSERT INTO clients (name, created_at) VALUES (?, ?)",
              (name, datetime.date.today().isoformat()))
    conn.commit()
    return c.lastrowid


def get_history(conn, name):
    c = conn.cursor()
    c.execute("""SELECT c.date, c.q_type, c.question, c.cards, c.reading, c.feedback
                 FROM cases c JOIN clients cl ON c.client_id = cl.id
                 WHERE cl.name = ? ORDER BY c.date, c.id""", (name,))
    return [dict(zip(["date", "q_type", "question", "cards", "reading", "feedback"], row))
            for row in c.fetchall()]


def save_case(conn, name, q_type, question, spread, cards_text, reading):
    c = conn.cursor()
    client_id = None
    if name:
        client_id = get_client_id(conn, name)
    c.execute("""INSERT INTO cases (client_id, date, q_type, question, spread, cards, reading)
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
              (client_id, datetime.date.today().isoformat(), q_type, question, spread, cards_text, reading))
    conn.commit()


def add_feedback(conn, name, case_idx, feedback):
    c = conn.cursor()
    c.execute("""SELECT c.id FROM cases c JOIN clients cl ON c.client_id = cl.id
                 WHERE cl.name = ? ORDER BY c.date, c.id""", (name,))
    rows = c.fetchall()
    if case_idx < 1 or case_idx > len(rows):
        return False
    c.execute("UPDATE cases SET feedback = ? WHERE id = ?", (feedback, rows[case_idx - 1][0]))
    conn.commit()
    return True


def list_cases(conn, name):
    c = conn.cursor()
    c.execute("""SELECT c.date, c.q_type, c.question, c.cards, c.reading, c.feedback
                 FROM cases c JOIN clients cl ON c.client_id = cl.id
                 WHERE cl.name = ? ORDER BY c.date, c.id""", (name,))
    return c.fetchall()


# ==================== 提示词生成 ====================

def build_prompt(name, history, q_type, question, spread, cards):
    lines = []
    lines.append("【客户档案】")
    if name:
        lines.append(f"称呼：{name}（第{len(history) + 1}次占卜）")
    else:
        lines.append("称呼：匿名客户（首次占卜）")
    if history:
        lines.append(f"历史案例 {len(history)} 条：")
        for i, h in enumerate(history, 1):
            lines.append(f"--- 案例 {i}（{h['date']}）---")
            lines.append(f"问题类型：{h['q_type']} | 提问：{h['question']}")
            lines.append(f"牌面：{h['cards']}")
            if h["reading"]:
                lines.append(f"解读：{h['reading']}")
            if h["feedback"]:
                lines.append(f"客户反馈：{h['feedback']}")
    else:
        lines.append("历史案例：无（首次占卜）")
    lines.append("")
    lines.append("【本次占卜】")
    lines.append(f"日期：{datetime.date.today().isoformat()}")
    lines.append(f"问题类型：{q_type}")
    lines.append(f"提问：{question}")
    if spread:
        lines.append(f"牌阵：{spread}")
    lines.append("牌面及牌义：")
    for i, (cname, pos, kw) in enumerate(cards, 1):
        lines.append(f"{i}. {cname}（{pos}位）：{kw}")
    lines.append("")
    lines.append("【任务要求】")
    lines.append("你是一位经验丰富的职业塔罗师。请基于以上客户背景与本次牌面：")
    lines.append("1. 先逐张解读，再做多张牌的串联解读，找出牌面之间的叙事线（时间线/角色/主题均可）；")
    lines.append("2. 若客户有历史案例，提炼反复出现的主题与趋势，结合本次牌面给出延续性判断；")
    lines.append("3. 结论直率、具体、可落地，避免空泛鸡汤；")
    lines.append("4. 最后输出一段适合公众号推文或视频口播的总结文案（200字以内）。")
    return "\n".join(lines)


def save_prompt_log(name, prompt):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"\n{'=' * 60}\n")
        f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}] 客户：{name or '匿名'}\n")
        f.write(f"{'=' * 60}\n")
        f.write(prompt + "\n")


# ==================== 交互流程 ====================

def new_reading(conn):
    print("\n---------- 开始新占卜 ----------")
    name = input("客户称呼（回车=匿名）：").strip()
    history = []
    if name:
        history = get_history(conn, name)
        if history:
            print(f">>> 老客户 {name}，历史 {len(history)} 条案例，最近问题：{history[-1]['question']}")
            fb_count = sum(1 for h in history if h["feedback"])
            print(f">>> 其中已有反馈 {fb_count} 条")
        else:
            print(f">>> 新客户 {name}，首次占卜")
    q_type = input("问题类型（事业/情感/学业/财运，回车默认综合）：").strip() or "综合"
    question = input("客户提问：").strip()
    spread = input("牌阵（如 圣三角，回车跳过）：").strip()
    cards_text = input("牌面（格式：恋人 正, 宝剑三 逆）：").strip()
    if not cards_text:
        print("未输入牌面，已取消。")
        return
    cards = parse_cards(cards_text)
    print("\n识别到的牌面：")
    for i, (cname, pos, kw) in enumerate(cards, 1):
        print(f"  {i}. {cname}（{pos}位）：{kw}")

    prompt = build_prompt(name, history, q_type, question, spread, cards)
    print("\n" + "=" * 60)
    print("以下内容可直接复制粘贴给 AI：")
    print("=" * 60)
    print(prompt)
    print("=" * 60)
    save_prompt_log(name, prompt)
    print(f"（提示词已自动存档到：{LOG_PATH}）")

    if input("\n保存为案例？(y/n)：").strip().lower() == "y":
        reading = input("你的解读/备注（回车跳过）：").strip()
        save_case(conn, name, q_type, question, spread, cards_text, reading)
        print("已保存。")


def add_feedback_flow(conn):
    print("\n---------- 补录客户反馈 ----------")
    name = input("客户称呼：").strip()
    if not name:
        return
    rows = list_cases(conn, name)
    if not rows:
        print("该客户暂无案例。")
        return
    print(f"{name} 的历史案例：")
    for i, r in enumerate(rows, 1):
        print(f"  {i}. [{r[0]}] {r[1]} | {r[2]}")
        print(f"     牌面：{r[3]}")
        if r[4]:
            print(f"     解读：{r[4][:40]}")
        if r[5]:
            print(f"     反馈：{r[5]}")
    try:
        idx = int(input(f"选择要补录反馈的案例编号（1-{len(rows)}）：").strip())
    except ValueError:
        print("输入无效。")
        return
    feedback = input("客户反馈内容：").strip()
    if feedback and add_feedback(conn, name, idx, feedback):
        print("反馈已补录。")


def view_history(conn):
    print("\n---------- 查看历史 ----------")
    name = input("客户称呼（输入 * 查看全部客户）：").strip()
    if name == "*":
        c = conn.cursor()
        c.execute("""SELECT cl.name, COUNT(c.id) FROM clients cl
                     LEFT JOIN cases c ON c.client_id = cl.id
                     GROUP BY cl.id ORDER BY cl.name""")
        rows = c.fetchall()
        if not rows:
            print("暂无客户记录。")
            return
        print("客户列表：")
        for n, cnt in rows:
            print(f"  {n}（{cnt} 条案例）")
        return
    rows = list_cases(conn, name)
    if not rows:
        print("未找到该客户记录。")
        return
    print(f"\n{name} 的全部案例：")
    for i, r in enumerate(rows, 1):
        print(f"\n--- 案例 {i} [{r[0]}] ---")
        print(f"问题类型：{r[1]} | 提问：{r[2]}")
        print(f"牌面：{r[3]}")
        if r[4]:
            print(f"解读：{r[4]}")
        if r[5]:
            print(f"反馈：{r[5]}")


def main():
    init_db()
    print("===== 塔罗占卜工作台 v1.0 =====")
    conn = sqlite3.connect(DB_PATH)
    try:
        while True:
            print("\n1. 开始新占卜（老客户自动整合历史）")
            print("2. 补录客户反馈")
            print("3. 查看历史")
            print("4. 退出")
            choice = input("请选择：").strip()
            if choice == "1":
                new_reading(conn)
            elif choice == "2":
                add_feedback_flow(conn)
            elif choice == "3":
                view_history(conn)
            elif choice == "4":
                print("再见，老板。")
                break
            else:
                print("无效输入，请重新选择。")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
