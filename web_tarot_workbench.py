# -*- coding: utf-8 -*-
"""
塔罗占卜工作台 · 网页版 v1.0
启动后自动打开浏览器，本地使用，数据存于脚本同目录 tarot_workbench.db
（与命令行版共用数据库，数据互通）

运行方式：PyCharm 直接运行，或终端执行 python web_tarot_workbench.py
"""

import base64
import secrets
import time
import io
import json
import math
import os
import re
import random
import sqlite3
import threading
import webbrowser
import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import quote, unquote, urlparse

from PIL import Image, ImageDraw, ImageFont

try:
    import astro_engine
except Exception as _e:
    astro_engine = None
    print('[astro] 引擎未加载:', _e)

try:
    import fortune_engine
except Exception as _e2:
    fortune_engine = None
    print('[fortune] 日运引擎未加载:', _e2)

PORT = 8765
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tarot_workbench.db")
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts_log.txt")

# ==================== 牌义关键词库 ====================

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

MINOR = {
    "权杖": {
        "element": "火 · 行动与热情",
        "1": "新起点、灵感迸发、行动的火种", "2": "规划、权衡抉择、明确方向",
        "3": "扩张、协作、初见成果", "4": "稳定、庆祝、小有成就",
        "5": "竞争、冲突、内耗", "6": "胜利、被认可、声望",
        "7": "坚守立场、防守、勇气", "8": "迅速行动、进展、消息传来",
        "9": "坚守到底、警觉、独撑大局", "10": "负重前行、完成、过度负荷",
    },
    "圣杯": {
        "element": "水 · 情感与关系",
        "1": "新感情、情感萌芽、直觉涌现", "2": "结合、默契、互相吸引",
        "3": "友谊、庆祝、社交", "4": "倦怠、反思、意兴阑珊",
        "5": "失落、遗憾、回头看", "6": "怀旧、回忆、旧人旧事",
        "7": "幻想、选择过多、不切实际", "8": "离开旧境、追寻意义",
        "9": "愿望成真、满足、感恩", "10": "圆满、家庭幸福、情感丰盛",
    },
    "宝剑": {
        "element": "风 · 思维与冲突",
        "1": "新想法、思路清晰、突破", "2": "纠结、僵局、两难",
        "3": "心碎、伤痛、真相刺痛", "4": "休整、暂停、给自己空间",
        "5": "冲突、胜负、伤人伤己", "6": "过渡、疗愈、离开困境",
        "7": "欺骗、偷偷行动、策略", "8": "束缚、困住、自我设限",
        "9": "焦虑、噩梦、过度担忧", "10": "结束、解脱、最坏已过",
    },
    "金币": {
        "element": "土 · 金钱与现实",
        "1": "新机会、物质种子、财运起点", "2": "权衡、理财、时间管理",
        "3": "合作、技能、团队成果", "4": "守成、稳定、抓得太紧",
        "5": "困境、匮乏、患难见真情", "6": "给予、分享、接受帮助",
        "7": "等待、评估、投资回报", "8": "精进、劳作、打磨技艺",
        "9": "独立、丰盛、自给自足", "10": "传承、长期富足、家业",
    },
}

COURT = {
    "权杖": {"侍从": "热情探索、新消息、跃跃欲试", "骑士": "冲劲十足、冒险行动、停不下来",
             "皇后": "自信魅力、热情大方、有感染力", "国王": "成熟领袖、远见、执行力强"},
    "圣杯": {"侍从": "敏感细腻、新感情讯号、想象力", "骑士": "浪漫追求、理想化、为爱奔走",
             "皇后": "温柔共情、疗愈者、情感丰沛", "国王": "情感成熟、沉稳包容、值得托付"},
    "宝剑": {"侍从": "机敏好奇、爱观察、口舌快", "骑士": "犀利直接、争辩、行动果断",
             "皇后": "独立理性、清醒冷静、界限分明", "国王": "权威冷静、逻辑主导、公正"},
    "金币": {"侍从": "踏实学习、新技能、务实", "骑士": "务实努力、稳步推进、可靠",
             "皇后": "丰盛滋养、会经营、接地气", "国王": "富足可靠、理财有成、大方"},
}

INVERSE_SUFFIX = "（逆位：受阻/过度/内在化，需转内求）"


def get_keywords(card_name, pos):
    name = card_name.strip()
    if name in MAJOR:
        return MAJOR[name].get(pos, MAJOR[name]["正"])
    for suit, table in MINOR.items():
        if name.startswith(suit):
            rest = name[len(suit):]
            chn = {"1": "一", "2": "二", "3": "三", "4": "四", "5": "五",
                   "6": "六", "7": "七", "8": "八", "9": "九", "10": "十"}
            for k in ["10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]:
                if rest in (k, chn[k]):
                    kw = table[k]
                    return kw + (INVERSE_SUFFIX if pos == "逆" else "")
            if rest in COURT[suit]:
                kw = COURT[suit][rest]
                return kw + (INVERSE_SUFFIX if pos == "逆" else "")
    return "（未收录此牌，可自行补充）"


def parse_cards(text):
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
        result.append({"name": name, "pos": pos, "kw": kw})
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
    c.execute("""CREATE TABLE IF NOT EXISTS site (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        banner_img TEXT,
        banner_link TEXT,
        site_title TEXT)""")
    c.execute("INSERT OR IGNORE INTO site (id, banner_img, banner_link, site_title) VALUES (1, ?, ?, ?)", ("", "", "PPTAROT"))
    # 星盘数据档案：前台客户填的出生信息 + 算出的星盘参数
    c.execute("""CREATE TABLE IF NOT EXISTS charts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT,
        name TEXT,
        birth TEXT,
        time_known INTEGER,
        region TEXT,
        lat REAL,
        lon REAL,
        sun TEXT,
        moon TEXT,
        asc TEXT,
        chart_json TEXT,
        relation TEXT,
        created_at TEXT)""")
    # charts 老库补 relation 列（关系标签：自己/伴侣/家人/朋友/同事/其他）
    try:
        cols = [r[1] for r in c.execute("PRAGMA table_info(charts)").fetchall()]
        if "relation" not in cols:
            c.execute("ALTER TABLE charts ADD COLUMN relation TEXT")
    except Exception:
        pass
    # ===== 用户行为记录（BI 统计 + 后期账号系统铺底）=====
    # visitors：一人一条，vid 是前台生成的匿名访客标识，account 预留给后期登录账号
    c.execute("""CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vid TEXT UNIQUE,
        ip TEXT,
        ua TEXT,
        account TEXT,
        first_at TEXT,
        last_at TEXT,
        visits INTEGER DEFAULT 0,
        n_daily INTEGER DEFAULT 0,
        n_draw INTEGER DEFAULT 0,
        n_answer INTEGER DEFAULT 0,
        n_dice INTEGER DEFAULT 0,
        note TEXT)""")
    # events：每一次行为一条，result 存结果摘要，q 存用户自己写的问题，detail 存 JSON 补充
    c.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vid TEXT,
        ip TEXT,
        ua TEXT,
        etype TEXT,
        cat TEXT,
        q TEXT,
        result TEXT,
        detail TEXT,
        day TEXT,
        created_at TEXT)""")
    c.execute("CREATE INDEX IF NOT EXISTS idx_events_day ON events(day)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON events(etype)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_events_vid ON events(vid)")
    conn.commit()
    conn.close()


# ==================== 用户行为记录 ====================

EVENT_TYPES = ("daily", "draw", "answer", "dice")
TRACK_RATE = {}          # ip -> [窗口起始秒, 次数]
TRACK_LIMIT = 120        # 每个 IP 每分钟最多写多少条，防刷
_now = datetime.datetime.now


def _rate_ok(ip, limit=TRACK_LIMIT):
    """极简内存限流：每 IP 每分钟 limit 条。"""
    now = time.time()
    it = TRACK_RATE.get(ip)
    if not it or now - it[0] > 60:
        TRACK_RATE[ip] = [now, 1]
        return True
    if it[1] >= limit:
        return False
    it[1] += 1
    return True


def track_visit(vid, ip, ua):
    """记录/更新一个访客（用户表雏形）。"""
    ts = _now().strftime("%Y-%m-%d %H:%M:%S")
    conn = db_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT id FROM visitors WHERE vid=?", (vid,))
        row = c.fetchone()
        if row:
            c.execute("UPDATE visitors SET last_at=?, visits=visits+1, ip=?, ua=? WHERE id=?",
                      (ts, ip, ua, row[0]))
        else:
            c.execute("""INSERT INTO visitors (vid,ip,ua,account,first_at,last_at,visits,note)
                         VALUES (?,?,?,'',?,?,1,'')""", (vid, ip, ua, ts, ts))
        conn.commit()
    finally:
        conn.close()


def track_event(vid, ip, ua, etype, cat, result, detail, q=""):
    """记录一条行为明细，同时累加访客表上对应的计数。"""
    now = _now()
    ts = now.strftime("%Y-%m-%d %H:%M:%S")
    day = now.strftime("%Y-%m-%d")
    col = {"daily": "n_daily", "draw": "n_draw", "answer": "n_answer", "dice": "n_dice"}.get(etype)
    conn = db_conn()
    try:
        c = conn.cursor()
        c.execute("""INSERT INTO events (vid,ip,ua,etype,cat,q,result,detail,day,created_at)
                     VALUES (?,?,?,?,?,?,?,?,?,?)""",
                  (vid, ip, ua, etype, (cat or "")[:40], (q or "")[:300],
                   (result or "")[:600], (detail or "")[:2000], day, ts))
        # 访客不存在就顺手建一条，避免只有事件没有用户记录
        c.execute("SELECT id FROM visitors WHERE vid=?", (vid,))
        row = c.fetchone()
        if not row:
            c.execute("""INSERT INTO visitors (vid,ip,ua,account,first_at,last_at,visits,note)
                         VALUES (?,?,?,'',?,?,0,'')""", (vid, ip, ua, ts, ts))
            vid_row = c.lastrowid
        else:
            vid_row = row[0]
        if col:
            c.execute("UPDATE visitors SET last_at=?, ip=?, ua=?, visits=visits+1, %s=%s+1 WHERE id=?" % (col, col),
                      (ts, ip, ua, vid_row))
        conn.commit()
    finally:
        conn.close()


def admin_stats(days=14):
    """后台概览：总量、今日、按类型、近 N 天曲线、分类分布。"""
    today = _now().strftime("%Y-%m-%d")
    days = max(1, min(int(days or 14), 90))
    start = (_now() - datetime.timedelta(days=days - 1)).strftime("%Y-%m-%d")
    conn = db_conn()
    try:
        c = conn.cursor()
        out = {"today": today, "by_type": {}, "series": [], "cat_dist": [], "recent": []}
        c.execute("SELECT COUNT(*) FROM events")
        out["total_events"] = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM visitors")
        out["total_visitors"] = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM events WHERE day=?", (today,))
        out["today_events"] = c.fetchone()[0]
        c.execute("SELECT COUNT(DISTINCT vid) FROM events WHERE day=?", (today,))
        out["today_visitors"] = c.fetchone()[0]
        for t in EVENT_TYPES:
            c.execute("SELECT COUNT(*) FROM events WHERE etype=?", (t,))
            total = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM events WHERE etype=? AND day=?", (t, today))
            out["by_type"][t] = {"total": total, "today": c.fetchone()[0]}
        c.execute("""SELECT day, etype, COUNT(*) FROM events WHERE day>=?
                     GROUP BY day, etype ORDER BY day""", (start,))
        bucket = {}
        for d, t, n in c.fetchall():
            bucket.setdefault(d, {})[t] = n
        cur = _now() - datetime.timedelta(days=days - 1)
        for i in range(days):
            d = (cur + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            row = {"day": d, "total": 0}
            for t in EVENT_TYPES:
                row[t] = (bucket.get(d) or {}).get(t, 0)
                row["total"] += row[t]
            out["series"].append(row)
        c.execute("""SELECT cat, COUNT(*) FROM events WHERE etype='draw' AND cat<>''
                     GROUP BY cat ORDER BY COUNT(*) DESC""")
        out["cat_dist"] = [{"cat": r[0], "n": r[1]} for r in c.fetchall()]
        c.execute("""SELECT id,vid,ip,etype,cat,q,result,created_at FROM events
                     ORDER BY id DESC LIMIT 12""")
        out["recent"] = [{"id": r[0], "vid": r[1], "ip": r[2], "etype": r[3], "cat": r[4],
                          "q": r[5], "result": r[6], "created_at": r[7]} for r in c.fetchall()]
        return out
    finally:
        conn.close()


def admin_events(etype="", kw="", days=0, limit=100, offset=0):
    """行为明细：可按类型 / 关键词（问题或结果）/ 天数筛选。"""
    where, args = [], []
    if etype and etype != "all":
        where.append("etype=?")
        args.append(etype)
    if kw:
        where.append("(q LIKE ? OR result LIKE ? OR cat LIKE ? OR ip LIKE ?)")
        like = "%" + kw + "%"
        args += [like, like, like, like]
    if days:
        start = (_now() - datetime.timedelta(days=int(days) - 1)).strftime("%Y-%m-%d")
        where.append("day>=?")
        args.append(start)
    sql_where = (" WHERE " + " AND ".join(where)) if where else ""
    conn = db_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM events" + sql_where, tuple(args))
        total = c.fetchone()[0]
        c.execute("""SELECT id,vid,ip,ua,etype,cat,q,result,detail,created_at FROM events
                     """ + sql_where + " ORDER BY id DESC LIMIT ? OFFSET ?",
                  tuple(args) + (max(1, min(int(limit or 100), 500)), max(0, int(offset or 0))))
        items = [{"id": r[0], "vid": r[1], "ip": r[2], "ua": r[3], "etype": r[4], "cat": r[5],
                  "q": r[6], "result": r[7], "detail": r[8], "created_at": r[9]} for r in c.fetchall()]
        return {"ok": True, "total": total, "items": items}
    finally:
        conn.close()


def admin_visitors(limit=300, kw=""):
    """访客列表：一人一行，带四类功能计数。"""
    conn = db_conn()
    try:
        c = conn.cursor()
        if kw:
            like = "%" + kw + "%"
            c.execute("""SELECT id,vid,ip,ua,account,first_at,last_at,visits,
                                n_daily,n_draw,n_answer,n_dice,note
                         FROM visitors WHERE ip LIKE ? OR vid LIKE ? OR ua LIKE ?
                         ORDER BY last_at DESC LIMIT ?""", (like, like, like, limit))
        else:
            c.execute("""SELECT id,vid,ip,ua,account,first_at,last_at,visits,
                                n_daily,n_draw,n_answer,n_dice,note
                         FROM visitors ORDER BY last_at DESC LIMIT ?""", (limit,))
        return [{"id": r[0], "vid": r[1], "ip": r[2], "ua": r[3], "account": r[4],
                 "first_at": r[5], "last_at": r[6], "visits": r[7], "n_daily": r[8],
                 "n_draw": r[9], "n_answer": r[10], "n_dice": r[11], "note": r[12]} for r in c.fetchall()]
    finally:
        conn.close()


def admin_visitor_del(vid):
    """删掉一个访客和他全部行为记录（BI 清脏数据用）。"""
    conn = db_conn()
    try:
        c = conn.cursor()
        c.execute("DELETE FROM events WHERE vid=?", (vid,))
        n1 = c.rowcount
        c.execute("DELETE FROM visitors WHERE vid=?", (vid,))
        conn.commit()
        return n1
    finally:
        conn.close()


def admin_visitor_note(vid, note):
    """给访客写备注（标老客户、渠道来源之类）。"""
    conn = db_conn()
    try:
        c = conn.cursor()
        c.execute("UPDATE visitors SET note=? WHERE vid=?", (note, vid))
        conn.commit()
        return c.rowcount
    finally:
        conn.close()


def chart_save(uid, name, birth, time_known, region, lat, lon, sun, moon, asc, chart_json, relation=""):
    """写入一条星盘档案，返回新 id。"""
    conn = db_conn()
    try:
        c = conn.cursor()
        c.execute("""INSERT INTO charts (uid,name,birth,time_known,region,lat,lon,sun,moon,asc,chart_json,relation,created_at)
                     VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (uid or "", name or "", birth or "", 1 if time_known else 0, region or "",
                   lat, lon, sun or "", moon or "", asc or "", chart_json or "",
                   (relation or "").strip(),
                   datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
        return c.lastrowid
    finally:
        conn.close()


def chart_list(uid, limit=50):
    """取某个前台访客的星盘档案（不含大字段），新建的在前。"""
    conn = db_conn()
    try:
        c = conn.cursor()
        c.execute("""SELECT id,name,birth,time_known,region,sun,moon,asc,relation,created_at
                     FROM charts WHERE uid=? ORDER BY id DESC LIMIT ?""", (uid or "", limit))
        rows = c.fetchall()
        return [{"id": r[0], "name": r[1], "birth": r[2], "time_known": r[3],
                 "region": r[4], "sun": r[5], "moon": r[6], "asc": r[7],
                 "relation": r[8] or "", "created_at": r[9]} for r in rows]
    finally:
        conn.close()


def chart_del(uid, cid):
    """删掉某访客自己的一条档案。"""
    conn = db_conn()
    try:
        c = conn.cursor()
        c.execute("DELETE FROM charts WHERE id=? AND uid=?", (cid, uid or ""))
        conn.commit()
        return c.rowcount
    finally:
        conn.close()


def chart_get(uid, cid):
    """取某访客的一条星盘档案（含坐标，前台可据此重算）。"""
    conn = db_conn()
    try:
        c = conn.cursor()
        c.execute("""SELECT id,name,birth,time_known,region,lat,lon,sun,moon,asc,relation,created_at
                     FROM charts WHERE id=? AND uid=?""", (cid, uid or ""))
        r = c.fetchone()
        if not r:
            return None
        return {"id": r[0], "name": r[1], "birth": r[2], "time_known": r[3],
                "region": r[4], "lat": r[5], "lon": r[6], "sun": r[7],
                "moon": r[8], "asc": r[9], "relation": r[10] or "", "created_at": r[11]}
    finally:
        conn.close()


def admin_charts(limit=500):
    """后台：全部星盘档案。"""
    conn = db_conn()
    try:
        c = conn.cursor()
        c.execute("""SELECT id,uid,name,birth,time_known,region,sun,moon,asc,chart_json,created_at
                     FROM charts ORDER BY id DESC LIMIT ?""", (limit,))
        rows = c.fetchall()
        return [{"id": r[0], "uid": r[1], "name": r[2], "birth": r[3], "time_known": r[4],
                 "region": r[5], "sun": r[6], "moon": r[7], "asc": r[8],
                 "chart_json": r[9], "created_at": r[10]} for r in rows]
    finally:
        conn.close()


def admin_chart_del(cid):
    conn = db_conn()
    try:
        c = conn.cursor()
        c.execute("DELETE FROM charts WHERE id=?", (cid,))
        conn.commit()
        return c.rowcount
    finally:
        conn.close()


def get_site(conn):
    c = conn.cursor()
    c.execute("SELECT banner_img, banner_link, site_title FROM site WHERE id = 1")
    row = c.fetchone()
    if not row:
        return {"banner_img": "", "banner_link": "", "site_title": "PPTAROT"}
    return {"banner_img": row[0] or "", "banner_link": row[1] or "", "site_title": row[2] or ""}


def set_site(conn, data):
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO site (id, banner_img, banner_link, site_title) VALUES (1, ?, ?, ?)",
              ("", "", "PPTAROT"))
    fields = {}
    for k in ("banner_img", "banner_link", "site_title"):
        if k in data:
            fields[k] = (data.get(k) or "").strip()
    if fields:
        sets = ", ".join("%s = ?" % k for k in fields)
        c.execute("UPDATE site SET " + sets + " WHERE id = 1", tuple(fields.values()))
        conn.commit()
    return {"ok": True, "site": get_site(conn)}


def save_site_banner(data_url):
    if not data_url or "," not in data_url:
        return {"error": "没有收到图片数据"}
    head, b64 = data_url.split(",", 1)
    ext = "png"
    if "jpeg" in head or "jpg" in head:
        ext = "jpg"
    elif "webp" in head:
        ext = "webp"
    try:
        raw = base64.b64decode(b64)
    except Exception:
        return {"error": "图片解析失败"}
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    fn = "site_banner_%d.%s" % (int(time.time()), ext)
    with open(os.path.join(UPLOAD_DIR, fn), "wb") as f:
        f.write(raw)
    return {"ok": True, "url": "/assets/uploads/" + fn}


def db_conn():
    return sqlite3.connect(DB_PATH)


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
    keys = ["date", "q_type", "question", "cards", "reading", "feedback"]
    return [dict(zip(keys, row)) for row in c.fetchall()]


def get_case_ids(conn, name):
    c = conn.cursor()
    c.execute("""SELECT c.id FROM cases c JOIN clients cl ON c.client_id = cl.id
                 WHERE cl.name = ? ORDER BY c.date, c.id""", (name,))
    return [row[0] for row in c.fetchall()]


def all_clients(conn):
    c = conn.cursor()
    c.execute("""SELECT cl.name, COUNT(c.id) FROM clients cl
                 LEFT JOIN cases c ON c.client_id = cl.id
                 GROUP BY cl.id ORDER BY cl.name""")
    return [{"name": n, "count": cnt} for n, cnt in c.fetchall()]


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
    for i, c in enumerate(cards, 1):
        lines.append(f"{i}. {c['name']}（{c['pos']}位）：{c['kw']}")
    lines.append("")
    lines.append("【任务要求】")
    lines.append("你是一位经验丰富的职业塔罗师。请基于以上客户背景与本次牌面：")
    lines.append("1. 先逐张解读，再做多张牌的串联解读，找出牌面之间的叙事线（时间线/角色/主题均可）；")
    lines.append("2. 若客户有历史案例，提炼反复出现的主题与趋势，结合本次牌面给出延续性判断；")
    lines.append("3. 结论直率、具体、可落地，避免空泛鸡汤；")
    lines.append("4. 最后输出一段适合公众号推文或视频口播的总结文案（200字以内）。")
    return "\n".join(lines)


def save_prompt_log(name, prompt):
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n{'=' * 60}\n")
            f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}] 客户：{name or '匿名'}\n")
            f.write(f"{'=' * 60}\n")
            f.write(prompt + "\n")
    except Exception:
        pass


# ==================== 图文生成器 · 牌库 ====================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARD_DIR = os.path.join(BASE_DIR, "cards")
ASSET_DIR = os.path.join(BASE_DIR, "assets")
UPLOAD_DIR = os.path.join(ASSET_DIR, "uploads")
LONG_DIR = os.path.join(BASE_DIR, "longimage")
SINGLE_DIR = os.path.join(BASE_DIR, "groupimage")
TMP_DIR = os.path.join(BASE_DIR, "_tmp")

MAJOR_CN = ["愚者", "魔术师", "女祭司", "皇后", "皇帝", "教皇", "恋人", "战车",
            "力量", "隐士", "命运之轮", "正义", "倒吊人", "死神", "节制", "恶魔",
            "高塔", "星星", "月亮", "太阳", "审判", "世界"]
SUIT_CN = ["权杖", "圣杯", "宝剑", "金币"]
RANK_CN = ["王牌", "二", "三", "四", "五", "六", "七", "八", "九", "十",
           "侍从", "骑士", "皇后", "国王"]

CARD_NAMES = list(MAJOR_CN)
for _s in SUIT_CN:
    for _r in RANK_CN:
        CARD_NAMES.append(_s + _r)

CN_NUM = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
MAX_GROUPS = 10
GROUP_BG = [(232, 201, 122), (168, 216, 232), (196, 178, 232), (150, 216, 178),
            (232, 178, 160), (170, 200, 168), (214, 186, 226), (232, 214, 160),
            (160, 206, 214), (208, 168, 200)]


def group_label(i):
    try:
        i = int(i)
    except Exception:
        i = 0
    return "第" + CN_NUM[i % 10] + "组"


def card_file(name):
    name = (name or "").strip()
    if name in CARD_NAMES:
        return "%02d_%s.png" % (CARD_NAMES.index(name), name)
    return None


def card_path(name):
    f = card_file(name)
    return os.path.join(CARD_DIR, f) if f else None


def random_draw(group_count=3):
    """78 张牌池内纯随机不放回抽取，正逆位各 50% 由程序决定，用户不可干预。"""
    try:
        n = int(group_count)
    except Exception:
        n = 3
    n = max(1, min(MAX_GROUPS, n))

    pool = list(CARD_NAMES)
    random.shuffle(pool)
    groups = []
    idx = 0
    for gi in range(n):
        cards = []
        for _ in range(3):
            if idx >= len(pool):
                break
            nm = pool[idx]
            idx += 1
            cards.append({"name": nm, "file": card_file(nm),
                          "pos": "逆" if random.random() < 0.5 else "正"})
        groups.append({"label": group_label(gi), "text": "", "subcover": "", "cards": cards})
    return {"groups": groups,
            "all": [{"name": nm, "file": card_file(nm)} for nm in CARD_NAMES]}


# ==================== 图文生成器 · 长图合成 ====================

BG_COLOR = (13, 26, 38)
TEXT_MAIN = (233, 242, 247)
TEXT_DIM = (146, 176, 194)
ACCENT_CYAN = (168, 216, 232)
ACCENT_GOLD = (232, 201, 122)
POS_REV_COLOR = (226, 158, 132)

def _pick_font(cands, linux_glob=""):
    """按候选顺序找第一个存在的字体文件，兼容 Windows / macOS / Linux。"""
    for p in cands:
        if p and os.path.isfile(p):
            return p
    if linux_glob:
        try:
            import glob
            hit = sorted(glob.glob(linux_glob))
            if hit:
                return hit[0]
        except Exception:
            pass
    return ""


_WIN_FONTS = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
FONT_REG = _pick_font([
    os.path.join(_WIN_FONTS, "msyh.ttc"),
    os.path.join(_WIN_FONTS, "simhei.ttf"),
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
], "/usr/share/fonts/**/NotoSansCJK*.ttc")
FONT_BOLD = _pick_font([
    os.path.join(_WIN_FONTS, "msyhbd.ttc"),
    os.path.join(_WIN_FONTS, "msyh.ttc"),
    "/System/Library/Fonts/PingFang.ttc",
], "/usr/share/fonts/**/NotoSansCJK*Bold*.ttc")
_FONT_CACHE = {}


def _font(size, bold=False):
    key = (size, bold)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    path = FONT_BOLD if bold else FONT_REG
    try:
        f = ImageFont.truetype(path, size)
    except Exception:
        try:
            f = ImageFont.truetype(FONT_REG, size)
        except Exception:
            f = ImageFont.load_default()
    _FONT_CACHE[key] = f
    return f


def _tw(draw, text, font):
    try:
        return draw.textlength(text, font=font)
    except Exception:
        try:
            return font.getsize(text)[0]
        except Exception:
            return len(text) * font.size


def _wrap(draw, text, font, max_w):
    lines = []
    for para in str(text or "").replace("\r", "").split("\n"):
        if not para.strip():
            lines.append("")
            continue
        cur = ""
        for ch in para:
            if not cur or _tw(draw, cur + ch, font) <= max_w:
                cur += ch
            else:
                lines.append(cur)
                cur = ch
        if cur:
            lines.append(cur)
    return lines


def _draw_spaced_center(draw, cx, y, text, font, fill, spacing=5):
    widths = [_tw(draw, ch, font) for ch in text]
    total = sum(widths) + spacing * max(0, len(text) - 1)
    x = cx - total / 2.0
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + spacing


def _open_rgb(path):
    try:
        im = Image.open(path)
        im.load()
        return im.convert("RGB")
    except Exception:
        return None


def _upload_path(name):
    """把前端传来的文件名解析成 uploads 目录内的真实路径，非法/不存在返回空串。"""
    name = os.path.basename(str(name or "").replace("\\", "/").strip())
    if not name or ".." in name:
        return ""
    base = os.path.normpath(UPLOAD_DIR)
    fp = os.path.normpath(os.path.join(base, name))
    if fp != base and not fp.startswith(base + os.sep):
        return ""
    return fp if os.path.isfile(fp) else ""


def save_upload_image(data_url, kind="cover"):
    """接收前端 FileReader 的 dataURL，落盘到 output/assets/uploads/ 并返回可访问 URL。"""
    s = str(data_url or "").strip()
    if not s:
        return {"error": "没有收到图片数据"}
    if s.lower().startswith("data:") and "," in s:
        s = s.split(",", 1)[1]
    try:
        raw = base64.b64decode(s)
    except Exception as e:
        return {"error": "图片解码失败：%s" % e}
    if not raw:
        return {"error": "图片内容为空"}
    try:
        im = Image.open(io.BytesIO(raw))
        im.load()
        im = im.convert("RGB")
    except Exception as e:
        return {"error": "无法识别该图片格式（请用 PNG/JPG）：%s" % e}

    if im.width > 1600:
        nh = max(1, int(round(im.height * 1600.0 / im.width)))
        im = im.resize((1600, nh), Image.LANCZOS)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_kind = "sub" if str(kind).lower().startswith("sub") else "cover"
    fn = "up_%s_%s_%04d.png" % (safe_kind, ts, random.randint(0, 9999))
    fp = os.path.join(UPLOAD_DIR, fn)
    guard = 0
    while os.path.exists(fp) and guard < 200:
        fn = "up_%s_%s_%04d_%d.png" % (safe_kind, ts, random.randint(0, 9999), guard)
        fp = os.path.join(UPLOAD_DIR, fn)
        guard += 1
    try:
        im.save(fp, "PNG", optimize=True)
    except Exception as e:
        return {"error": "图片保存失败：%s" % e}
    return {"ok": True, "file": fn, "path": fp,
            "url": "/assets/uploads/" + quote(fn),
            "width": im.width, "height": im.height}


# ---------- 背景纹理：宇宙星体 + 蝴蝶线描 ----------

def _qbez(p0, p1, p2, n=26):
    pts = []
    for i in range(n + 1):
        t = i / float(n)
        x = (1 - t) * (1 - t) * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) * (1 - t) * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts


def _paste_rgba(base, sprite, x, y):
    x = int(round(x))
    y = int(round(y))
    sx = -x if x < 0 else 0
    sy = -y if y < 0 else 0
    dx = x if x > 0 else 0
    dy = y if y > 0 else 0
    w = sprite.width - sx
    h = sprite.height - sy
    if w <= 0 or h <= 0 or dx >= base.width or dy >= base.height:
        return
    w = min(w, base.width - dx)
    h = min(h, base.height - dy)
    if w <= 0 or h <= 0:
        return
    base.alpha_composite(sprite.crop((sx, sy, sx + w, sy + h)), (dx, dy))


def _butterfly_sprite(size=240, color=(158, 210, 236), alpha=58, angle=0):
    """程序化线描蝴蝶（4 倍超采样后缩小，线条平滑），返回 RGBA 贴图。"""
    size = max(60, int(size))
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = S / 2.0, S / 2.0
    line_w = max(2, int(S * 0.007))
    line_col = tuple(color) + (int(max(6, alpha)),)
    fill_col = tuple(color) + (int(max(4, alpha * 0.32)),)

    def wing(sign):
        up = [(cx + sign * 0.03 * S, cy - 0.09 * S)]
        up += _qbez((cx + sign * 0.03 * S, cy - 0.09 * S),
                    (cx + sign * 0.30 * S, cy - 0.42 * S),
                    (cx + sign * 0.45 * S, cy - 0.26 * S), 22)
        up += _qbez((cx + sign * 0.45 * S, cy - 0.26 * S),
                    (cx + sign * 0.46 * S, cy - 0.05 * S),
                    (cx + sign * 0.05 * S, cy - 0.01 * S), 22)
        lo = [(cx + sign * 0.05 * S, cy + 0.02 * S)]
        lo += _qbez((cx + sign * 0.05 * S, cy + 0.02 * S),
                    (cx + sign * 0.40 * S, cy + 0.05 * S),
                    (cx + sign * 0.33 * S, cy + 0.27 * S), 22)
        lo += _qbez((cx + sign * 0.33 * S, cy + 0.27 * S),
                    (cx + sign * 0.20 * S, cy + 0.40 * S),
                    (cx + sign * 0.04 * S, cy + 0.19 * S), 22)
        for poly in (up, lo):
            d.polygon(poly, fill=fill_col)
            d.line(poly + [poly[0]], fill=line_col, width=line_w, joint="curve")

    wing(-1)
    wing(1)
    d.line([(cx, cy - 0.12 * S), (cx, cy + 0.22 * S)], fill=line_col, width=line_w)
    r = max(2, int(S * 0.008))
    d.ellipse([cx - r, cy - 0.14 * S - r, cx + r, cy - 0.14 * S + r], fill=line_col)
    thin = max(1, line_w - 1)
    d.line(_qbez((cx, cy - 0.13 * S), (cx - 0.10 * S, cy - 0.26 * S),
                 (cx - 0.18 * S, cy - 0.35 * S), 12), fill=line_col, width=thin, joint="curve")
    d.line(_qbez((cx, cy - 0.13 * S), (cx + 0.10 * S, cy - 0.26 * S),
                 (cx + 0.18 * S, cy - 0.35 * S), 12), fill=line_col, width=thin, joint="curve")

    im = im.resize((size, size), Image.LANCZOS)
    if angle:
        im = im.rotate(angle, resample=Image.BICUBIC, expand=False)
    return im


def _gradient_bg(W, H, top=(10, 20, 33), bottom=(20, 38, 56)):
    H = max(2, int(H))
    strip = Image.new("RGB", (1, H))
    px = strip.load()
    for y in range(H):
        t = y / float(H - 1)
        px[0, y] = (int(round(top[0] + (bottom[0] - top[0]) * t)),
                    int(round(top[1] + (bottom[1] - top[1]) * t)),
                    int(round(top[2] + (bottom[2] - top[2]) * t)))
    return strip.resize((W, H), Image.BILINEAR).convert("RGBA")


def _star_layer(W, H, seed, density=1.0, alpha_max=120):
    rnd = random.Random(seed)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    n_star = int(max(140, H / 6.0) * density)
    for _ in range(n_star):
        x = rnd.uniform(0, W)
        y = rnd.uniform(0, H)
        r = rnd.choice([0.7, 1.0, 1.2, 1.6, 2.1, 2.8])
        a = rnd.randint(28, max(30, int(alpha_max)))
        col = rnd.choice([(214, 238, 250), (176, 214, 238), (232, 222, 196)])
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (a,))
    for _ in range(int(max(10, H / 220))):
        x = rnd.uniform(30, W - 30)
        y = rnd.uniform(30, H - 30)
        R = rnd.uniform(2.6, 5.6)
        a = rnd.randint(60, min(170, int(alpha_max) + 50))
        # 柔光星点：由外向内多层圆晕 + 亮核，替代原来的直十字，避免出现生硬的“+”
        for k, fa in ((3.4, 0.14), (2.2, 0.24), (1.5, 0.38)):
            rr = R * k
            d.ellipse([x - rr, y - rr, x + rr, y + rr],
                      fill=(206, 234, 250, int(a * fa)))
        d.ellipse([x - R, y - R, x + R, y + R], fill=(226, 242, 252, int(a * 0.60)))
        d.ellipse([x - R * 0.42, y - R * 0.42, x + R * 0.42, y + R * 0.42],
                  fill=(255, 255, 255, min(255, int(a * 1.05))))
    for _ in range(int(max(6, H / 420))):
        cx = rnd.uniform(-W * 0.35, W * 1.15)
        cy = rnd.uniform(0, H)
        rr = rnd.uniform(150, 430)
        st = rnd.uniform(0, 360)
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], st, st + rnd.uniform(35, 150),
              fill=(150, 202, 228, rnd.randint(24, 60)), width=1)
    return lay


def _planet_layer(W, H, seed):
    rnd = random.Random(seed + 7)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for _ in range(int(max(2, H / 1500))):
        if rnd.random() < 0.5:
            cx = rnd.uniform(-60, W * 0.20)
        else:
            cx = rnd.uniform(W * 0.80, W + 60)
        cy = rnd.uniform(0, H)
        r = rnd.uniform(44, 116)
        a = rnd.randint(18, 34)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(176, 208, 232, a))
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  outline=(208, 232, 248, a + 24), width=2)
        d.ellipse([cx - r * 1.75, cy - r * 0.34, cx + r * 1.75, cy + r * 0.34],
                  outline=(196, 222, 242, a + 10), width=1)
    return lay


def _butterfly_layer(W, H, seed, alpha=52, step=520, size_range=(170, 300)):
    rnd = random.Random(seed + 13)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    y = rnd.uniform(90, 220)
    i = 0
    while y < H - 40:
        size = rnd.uniform(size_range[0], size_range[1])
        left = (i % 2 == 0)
        if left:
            x = rnd.uniform(-size * 0.32, size * 0.12)
        else:
            x = rnd.uniform(W - size * 0.78, W - size * 0.36)
        ang = rnd.uniform(-26, 26) * (1 if left else -1)
        a = int(max(10, alpha + rnd.randint(-12, 14)))
        sp = _butterfly_sprite(size=int(size), color=(156, 208, 236), alpha=a, angle=ang)
        _paste_rgba(lay, sp, x, y - size / 2.0)
        y += step + rnd.uniform(-110, 150)
        i += 1
    return lay


def make_background(W, H, seed=20261110):
    """与长图等高的整幅背景：深空渐变 + 星点/星芒/星轨 + 星体 + 蝴蝶线描 + 半透明遮罩。"""
    bg = _gradient_bg(W, H)
    bg.alpha_composite(_planet_layer(W, H, seed))
    bg.alpha_composite(_star_layer(W, H, seed))
    bg.alpha_composite(_butterfly_layer(W, H, seed))
    bg.alpha_composite(Image.new("RGBA", (W, H), BG_COLOR + (94,)))
    return bg


def make_foreground(W, H, seed=20261110):
    """覆盖在正文之上的极淡纹理：保证封面与每组区域都连续有元素，但阻尼到不影响阅读。"""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lay.alpha_composite(_star_layer(W, H, seed + 101, density=0.30, alpha_max=38))
    lay.alpha_composite(_butterfly_layer(W, H, seed + 55, alpha=24, step=760,
                                        size_range=(190, 320)))
    return lay


def _compose_subcover_grid(groups, W=750, H=900, top_h=470):
    """未上传总封面时：把各组子封面拼成一张图，每个子封面下方标注组别名称。"""
    items = []
    for gi, g in enumerate(groups or []):
        g = g if isinstance(g, dict) else {}
        fp = _upload_path(g.get("subcover"))
        im = _open_rgb(fp) if fp else None
        if im is None:
            continue
        label = (g.get("label") or "").strip() or group_label(gi)
        items.append((im, label))
    if not items:
        return None

    canvas = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    n = len(items)
    cols = 3 if n > 2 else n
    rows = int(math.ceil(n / float(cols)))
    pad = 22
    gap = 16
    label_h = 34
    cell_w = (W - pad * 2 - gap * (cols - 1)) / float(cols)
    avail_h = top_h - pad - gap * (rows - 1) - label_h * rows
    cell_h = max(60.0, min(300.0, avail_h / float(rows)))

    total_h = rows * cell_h + (rows - 1) * gap + rows * label_h
    y = pad + max(0.0, (top_h - pad - total_h) / 2.0)

    f_lb = _font(22, True)
    for idx, (im, label) in enumerate(items):
        c = idx % cols
        x = pad + c * (cell_w + gap)
        sc = min(cell_w / float(im.width), cell_h / float(im.height))
        nw = max(1, int(round(im.width * sc)))
        nh = max(1, int(round(im.height * sc)))
        sim = im.resize((nw, nh), Image.LANCZOS)
        px = int(x + (cell_w - nw) / 2.0)
        py = int(y + (cell_h - nh) / 2.0)
        draw.rectangle([px - 3, py - 3, px + nw + 3, py + nh + 3],
                       fill=(9, 18, 27), outline=(96, 132, 154))
        canvas.paste(sim, (px, py))
        ly = int(y + cell_h + 7)
        tw = _tw(draw, label, f_lb)
        draw.text((x + (cell_w - tw) / 2.0, ly), label, font=f_lb, fill=ACCENT_GOLD)
        if c == cols - 1 or idx == n - 1:
            y += cell_h + label_h + gap
    return canvas


def _render_cover(canvas, draw, W, PAD, CW, cover_path, title, subtitle, guide):
    COVER_H = 900
    cim = _open_rgb(cover_path) if cover_path else None
    if cim is not None:
        sc = max(W / float(cim.width), COVER_H / float(cim.height))
        nw = max(1, int(round(cim.width * sc)))
        nh = max(1, int(round(cim.height * sc)))
        cim = cim.resize((nw, nh), Image.LANCZOS)
        left = (nw - W) // 2
        top = (nh - COVER_H) // 2
        canvas.paste(cim.crop((left, top, left + W, top + COVER_H)), (0, 0))
    else:
        draw.rectangle([0, 0, W, COVER_H], fill=(16, 32, 46))

    mask = Image.new("L", (1, COVER_H), 0)
    for yy in range(COVER_H):
        if yy < 500:
            a = 0
        else:
            a = int(212 * min(1.0, (yy - 500) / 250.0))
        mask.putpixel((0, yy), a)
    mask = mask.resize((W, COVER_H))
    dark = Image.new("RGBA", (W, COVER_H), BG_COLOR + (255,))
    canvas.paste(Image.composite(dark, canvas.crop((0, 0, W, COVER_H)), mask), (0, 0))

    f_title = _font(54, True)
    tlines = _wrap(draw, title, f_title, CW)[:3]
    if len(tlines) > 1:
        f_title = _font(44, True)
        tlines = _wrap(draw, title, f_title, CW)[:3]
    cy = 520 if len(tlines) == 1 else 500
    fh = 74 if getattr(f_title, "size", 44) >= 50 else 60
    for ln in tlines:
        _draw_spaced_center(draw, W / 2.0, cy, ln, f_title, ACCENT_GOLD, 4)
        cy += fh

    draw.line([W / 2 - 45, cy + 4, W / 2 + 45, cy + 4], fill=ACCENT_CYAN, width=2)
    cy += 28

    if subtitle:
        f_sub = _font(26)
        for ln in _wrap(draw, subtitle, f_sub, CW)[:2]:
            draw.text(((W - _tw(draw, ln, f_sub)) / 2, cy), ln, font=f_sub, fill=TEXT_MAIN)
            cy += 40
        cy += 12
    if guide:
        f_g = _font(23)
        for ln in _wrap(draw, guide, f_g, CW)[:3]:
            draw.text(((W - _tw(draw, ln, f_g)) / 2, cy), ln, font=f_g, fill=ACCENT_CYAN)
            cy += 36
    return COVER_H


def _render_group(canvas, draw, W, PAD, CW, gi, g, y, tail_rule=True):
    y += 48
    label = (g.get("label") or "").strip() or group_label(gi)
    f_pill = _font(26, True)
    pill_w = _tw(draw, label, f_pill) + 44
    pbg = GROUP_BG[gi % len(GROUP_BG)]
    draw.rounded_rectangle([PAD, y, PAD + pill_w, y + 48], radius=24, fill=pbg)
    bb = f_pill.getbbox(label)
    draw.text((PAD + 22, y + (48 - (bb[3] - bb[1])) / 2.0 - bb[1]), label,
              font=f_pill, fill=(18, 32, 44))
    y += 48 + 26

    # 子封面（选填）：组标签下方、三张牌上方，居中，宽约内容区 70%，等比不裁切
    sub_fp = _upload_path(g.get("subcover"))
    if sub_fp:
        sim = _open_rgb(sub_fp)
        if sim is not None:
            tw_ = int(round(CW * 0.70))
            sc = tw_ / float(sim.width)
            nh_ = int(round(sim.height * sc))
            # 仅在极端超长图时才收窄，常规竖版/横版图都保持 70% 宽 + 原始比例不裁切
            max_h = 1100
            if nh_ > max_h:
                sc = max_h / float(sim.height)
                tw_ = max(1, int(round(sim.width * sc)))
                nh_ = max_h
            sim = sim.resize((max(1, tw_), max(1, nh_)), Image.LANCZOS)
            px = (W - sim.width) // 2
            draw.rectangle([px - 4, y - 4, px + sim.width + 4, y + sim.height + 4],
                           fill=(9, 18, 27), outline=(96, 132, 154))
            canvas.paste(sim, (px, y))
            y += sim.height + 30

    cards = g.get("cards") or []
    CARD_W = 186
    CARD_H = int(round(CARD_W * 1.72))
    GAP = 34
    total_w = 3 * CARD_W + 2 * GAP
    x0 = (W - total_w) // 2
    max_bottom = y

    for i in range(min(3, len(cards))):
        c = cards[i]
        name = (c.get("name") or "").strip()
        pos = "逆" if c.get("pos") == "逆" else "正"
        cx = x0 + i * (CARD_W + GAP)
        fp = card_path(name)
        ch = CARD_H
        if fp and os.path.isfile(fp):
            try:
                im = Image.open(fp).convert("RGB")
                if pos == "逆":
                    im = im.rotate(180)
                sc = min(CARD_W / float(im.width), CARD_H / float(im.height))
                nw = max(1, int(round(im.width * sc)))
                nh = max(1, int(round(im.height * sc)))
                im = im.resize((nw, nh), Image.LANCZOS)
                ox = cx + (CARD_W - nw) // 2
                oy = y + (CARD_H - nh) // 2
                draw.rectangle([cx + 4, y + 6, cx + CARD_W + 4, y + CARD_H + 6], fill=(6, 14, 20))
                canvas.paste(im, (ox, oy))
                draw.rectangle([cx, y, cx + CARD_W, y + CARD_H], outline=(120, 152, 172), width=1)
            except Exception:
                draw.rectangle([cx, y, cx + CARD_W, y + ch], fill=(28, 44, 58),
                               outline=(120, 152, 172))
        else:
            draw.rectangle([cx, y, cx + CARD_W, y + ch], fill=(28, 44, 58),
                           outline=(120, 152, 172))
            f_m = _font(18)
            draw.text((cx + (CARD_W - _tw(draw, "缺图", f_m)) / 2, y + ch / 2.0 - 12),
                      "缺图", font=f_m, fill=TEXT_DIM)

        f_nm = _font(21, True)
        nlines = _wrap(draw, name, f_nm, CARD_W)[:2]
        if nlines and max(_tw(draw, ln, f_nm) for ln in nlines) > CARD_W:
            f_nm = _font(17, True)
            nlines = _wrap(draw, name, f_nm, CARD_W)[:2]
        ny = y + ch + 12
        for ln in nlines:
            draw.text((cx + (CARD_W - _tw(draw, ln, f_nm)) / 2, ny), ln, font=f_nm, fill=TEXT_MAIN)
            ny += 27

        f_ps = _font(16)
        ptxt = "正位" if pos == "正" else "逆位"
        pcol = ACCENT_CYAN if pos == "正" else POS_REV_COLOR
        draw.text((cx + (CARD_W - _tw(draw, ptxt, f_ps)) / 2, ny + 2), ptxt, font=f_ps, fill=pcol)
        if ny + 30 > max_bottom:
            max_bottom = ny + 30

    y = max_bottom + 28

    txt = (g.get("text") or "").strip()
    if txt:
        f_b = _font(25)
        lh = 42
        for ln in _wrap(draw, txt, f_b, CW):
            if ln == "":
                y += int(lh * 0.55)
                continue
            draw.text((PAD, y), ln, font=f_b, fill=TEXT_MAIN)
            y += lh

    y += 14
    if tail_rule:
        for x in range(PAD, W - PAD, 12):
            draw.line([x, y, x + 6, y], fill=(46, 70, 88), width=1)
    return y + 6


def _render_all(canvas, draw, W, PAD, CW, title, subtitle, guide, footer, groups, cover_path):
    y = _render_cover(canvas, draw, W, PAD, CW, cover_path, title, subtitle, guide)
    segs = [{"key": "cover", "title": "封面", "y0": 0, "y1": y}]
    for gi, g in enumerate(groups):
        y0 = y
        y = _render_group(canvas, draw, W, PAD, CW, gi, g, y,
                          tail_rule=(gi < len(groups) - 1))
        segs.append({"key": "g%d" % (gi + 1), "title": group_label(gi),
                     "y0": y0, "y1": y})

    y0 = y
    y += 56
    if footer:
        f_f = _font(22)
        draw.text(((W - _tw(draw, footer, f_f)) / 2, y), footer, font=f_f, fill=TEXT_DIM)
        y += 40
    y += 46
    segs.append({"key": "footer", "title": "页脚", "y0": y0, "y1": y + 60})
    return y + 60, segs


# ==================== 每组单图（每组独立一张） ====================
# 版式：顶部大标题 + 三张牌横排 + 组标签/头像/作者名 + 白色解读区（牌面解析 / 给你的建议 / 免责声明）

CARD_PAPER = (255, 255, 255)
CARD_INK = (44, 48, 56)
CARD_INK_SUB = (104, 112, 124)
CARD_INK_DIM = (152, 158, 168)
CARD_RED = (198, 74, 74)
CARD_RULE = (228, 232, 238)


def _draw_tri_cards(canvas, draw, W, CW, cards, y, card_w=186, gap=34):
    # 横排三张牌 + 牌名 + 正逆位，返回新的 y
    card_h = int(round(card_w * 1.72))
    total_w = 3 * card_w + 2 * gap
    x0 = (W - total_w) // 2
    max_bottom = y
    for i in range(min(3, len(cards))):
        c = cards[i] if isinstance(cards[i], dict) else {}
        name = (c.get("name") or "").strip()
        pos = "逆" if c.get("pos") == "逆" else "正"
        cx = x0 + i * (card_w + gap)
        fp = card_path(name)
        if fp and os.path.isfile(fp):
            try:
                im = Image.open(fp).convert("RGB")
                if pos == "逆":
                    im = im.rotate(180)
                sc = min(card_w / float(im.width), card_h / float(im.height))
                nw = max(1, int(round(im.width * sc)))
                nh = max(1, int(round(im.height * sc)))
                im = im.resize((nw, nh), Image.LANCZOS)
                draw.rectangle([cx + 4, y + 6, cx + card_w + 4, y + card_h + 6], fill=(6, 14, 20))
                canvas.paste(im, (cx + (card_w - nw) // 2, y + (card_h - nh) // 2))
                draw.rectangle([cx, y, cx + card_w, y + card_h], outline=(132, 164, 184), width=1)
            except Exception:
                draw.rectangle([cx, y, cx + card_w, y + card_h], fill=(28, 44, 58),
                               outline=(132, 164, 184))
        else:
            draw.rectangle([cx, y, cx + card_w, y + card_h], fill=(28, 44, 58),
                           outline=(132, 164, 184))
            f_m = _font(18)
            draw.text((cx + (card_w - _tw(draw, "缺图", f_m)) / 2, y + card_h / 2.0 - 12),
                      "缺图", font=f_m, fill=TEXT_DIM)

        f_nm = _font(22, True)
        nlines = _wrap(draw, name, f_nm, card_w)[:2]
        if nlines and max(_tw(draw, ln, f_nm) for ln in nlines) > card_w:
            f_nm = _font(18, True)
            nlines = _wrap(draw, name, f_nm, card_w)[:2]
        ny = y + card_h + 14
        for ln in nlines:
            draw.text((cx + (card_w - _tw(draw, ln, f_nm)) / 2, ny), ln, font=f_nm, fill=TEXT_MAIN)
            ny += 28
        f_ps = _font(17)
        ptxt = "正位" if pos == "正" else "逆位"
        pcol = ACCENT_CYAN if pos == "正" else POS_REV_COLOR
        draw.text((cx + (card_w - _tw(draw, ptxt, f_ps)) / 2, ny + 2), ptxt, font=f_ps, fill=pcol)
        if ny + 32 > max_bottom:
            max_bottom = ny + 32
    return max_bottom + 26


def _single_card_blocks(draw, CW, payload, g, gi):
    # 预排白色解读区：只测量不绘制，返回 (blocks, card_h)
    pad = 40
    inner = CW - pad * 2
    blocks = []
    label = (g.get("label") or "").strip() or group_label(gi)
    f_pill = _font(26, True)
    blocks.append({"t": "head", "y": pad, "label": label, "f": f_pill,
                   "pill_w": _tw(draw, label, f_pill) + 44})
    y = pad + 66 + 20
    blocks.append({"t": "rule", "y": y})
    y += 30

    lead = (payload.get("lead") or "").strip()
    if lead:
        f_lead = _font(25)
        lines = _wrap(draw, lead, f_lead, inner)
        blocks.append({"t": "lead", "y": y, "lines": lines, "f": f_lead, "lh": 42})
        y += len(lines) * 42 + 26

    for title, key in (("牌面解析", "analysis"), ("给你的建议", "advice")):
        body = (g.get(key) or "").strip()
        if not body:
            continue
        f_h = _font(27, True)
        f_b = _font(24)
        blocks.append({"t": "sec", "y": y, "title": title, "f": f_h})
        y += 46
        lines = _wrap(draw, body, f_b, inner)
        blocks.append({"t": "body", "y": y, "lines": lines, "f": f_b, "lh": 40})
        y += len(lines) * 40 + 30

    disc = (payload.get("disclaimer") or "").strip()
    if disc:
        f_d = _font(18)
        lines = _wrap(draw, disc, f_d, inner)
        y += 14
        blocks.append({"t": "rule2", "y": y})
        y += 24
        blocks.append({"t": "disc", "y": y, "lines": lines, "f": f_d, "lh": 28})
        y += len(lines) * 28
    return blocks, int(round(y + 34))


def _paint_single_card(canvas, draw, W, PAD, CW, payload, g, gi, y0, card_h):
    pad = 40
    inner_l = PAD + pad
    inner_r = PAD + CW - pad
    blocks, _ = _single_card_blocks(draw, CW, payload, g, gi)
    draw.rounded_rectangle([PAD, y0, PAD + CW, y0 + card_h], radius=30, fill=CARD_PAPER)

    av_fp = _upload_path(payload.get("avatar_file"))
    author = (payload.get("author") or "").strip()

    for b in blocks:
        by = y0 + b["y"]
        t = b["t"]
        if t == "head":
            pbg = GROUP_BG[gi % len(GROUP_BG)]
            draw.rounded_rectangle([inner_l, by, inner_l + b["pill_w"], by + 46],
                                   radius=23, fill=pbg)
            f_p = b["f"]
            bb = f_p.getbbox(b["label"])
            draw.text((inner_l + 22, by + (46 - (bb[3] - bb[1])) / 2.0 - bb[1]), b["label"],
                      font=f_p, fill=(18, 32, 44))
            ax = inner_r
            if av_fp:
                av = _open_rgb(av_fp)
                if av is not None:
                    d_ = 58
                    sc = d_ / float(max(1, min(av.width, av.height)))
                    nw = max(1, int(round(av.width * sc)))
                    nh = max(1, int(round(av.height * sc)))
                    av = av.resize((nw, nh), Image.LANCZOS)
                    lf = (nw - d_) // 2
                    tp = (nh - d_) // 2
                    av = av.crop((lf, tp, lf + d_, tp + d_)).convert("RGBA")
                    mask = Image.new("L", (d_, d_), 0)
                    ImageDraw.Draw(mask).ellipse([0, 0, d_ - 1, d_ - 1], fill=255)
                    canvas.paste(av, (ax - d_, by - 6), mask)
                    ax -= d_ + 12
            if author:
                f_a = _font(24)
                draw.text((ax - _tw(draw, author, f_a), by + 8), author, font=f_a, fill=CARD_INK_SUB)
        elif t == "rule":
            draw.line([inner_l, by, inner_r, by], fill=CARD_RULE, width=2)
        elif t == "rule2":
            draw.line([inner_l, by, inner_r, by], fill=CARD_RULE, width=1)
        elif t == "lead":
            for ln in b["lines"]:
                draw.text((inner_l, by), ln, font=b["f"], fill=CARD_INK_SUB)
                by += b["lh"]
        elif t == "sec":
            draw.rectangle([inner_l, by + 5, inner_l + 5, by + 35], fill=CARD_RED)
            draw.text((inner_l + 18, by), b["title"], font=b["f"], fill=(30, 34, 42))
        elif t == "body":
            for ln in b["lines"]:
                draw.text((inner_l, by), ln, font=b["f"], fill=CARD_INK)
                by += b["lh"]
        elif t == "disc":
            for ln in b["lines"]:
                draw.text(((W - _tw(draw, ln, b["f"])) / 2, by), ln, font=b["f"], fill=CARD_INK_DIM)
                by += b["lh"]


def _render_single_group(canvas, draw, W, PAD, CW, payload, gi, g):
    title = (payload.get("title") or "").strip() or "选牌"
    subtitle = (payload.get("subtitle") or "").strip()
    y = 64

    f_t = _font(48, True)
    tlines = _wrap(draw, title, f_t, CW)[:3]
    if len(tlines) > 1:
        f_t = _font(42, True)
        tlines = _wrap(draw, title, f_t, CW)[:3]
    for ln in tlines:
        _draw_spaced_center(draw, W / 2.0, y, ln, f_t, ACCENT_GOLD, 4)
        y += 62
    draw.line([W / 2.0 - 42, y + 8, W / 2.0 + 42, y + 8], fill=ACCENT_GOLD, width=2)
    y += 38

    # 单牌图按需求不展示副标题，只保留大标题 + 金线
    y += 8

    sub_fp = _upload_path(g.get("subcover"))
    if sub_fp:
        sim = _open_rgb(sub_fp)
        if sim is not None:
            tw_ = int(round(CW * 0.62))
            sc = tw_ / float(sim.width)
            nh_ = int(round(sim.height * sc))
            if nh_ > 900:
                nh_ = 900
                tw_ = max(1, int(round(sim.width * nh_ / float(sim.height))))
            sim = sim.resize((max(1, tw_), max(1, nh_)), Image.LANCZOS)
            px = (W - sim.width) // 2
            draw.rectangle([px - 4, y - 4, px + sim.width + 4, y + sim.height + 4],
                           fill=(9, 18, 27), outline=(96, 132, 154))
            canvas.paste(sim, (px, y))
            y += sim.height + 34
    else:
        y += 10

    y = _draw_tri_cards(canvas, draw, W, CW, g.get("cards") or [], y)
    y += 22

    blocks, card_h = _single_card_blocks(draw, CW, payload, g, gi)
    _paint_single_card(canvas, draw, W, PAD, CW, payload, g, gi, y, card_h)
    return y + card_h + 64


def _norm_single_groups(groups):
    out = []
    for g in groups:
        gg = dict(g) if isinstance(g, dict) else {}
        a = str(gg.get("analysis") or "").strip()
        adv = str(gg.get("advice") or "").strip()
        if not a and not adv:
            t = str(gg.get("text") or "").strip()
            if t:
                parts = [p.strip() for p in re.split(r"\n\s*\n", t) if p.strip()]
                if parts:
                    a = parts[0]
                    if len(parts) > 1:
                        adv = "\n\n".join(parts[1:])
        gg["analysis"] = a
        gg["advice"] = adv
        out.append(gg)
    return out


def compose_group_images(payload):
    W = 750
    PAD = 56
    CW = W - PAD * 2

    groups = payload.get("groups")
    if not isinstance(groups, list) or not groups:
        groups = random_draw(3)["groups"]
    groups = _norm_single_groups(groups[:MAX_GROUPS])

    os.makedirs(SINGLE_DIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    images = []

    for gi, g in enumerate(groups):
        H = 3600
        layer = None
        yend = 0
        for _ in range(8):
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            draw = ImageDraw.Draw(layer)
            yend = _render_single_group(layer, draw, W, PAD, CW, payload, gi, g)
            if yend + 20 <= H:
                break
            H = int(yend) + 400
        H2 = int(min(yend + 20, H))
        layer = layer.crop((0, 0, W, H2))

        seed = 20261110 + gi * 37
        bg = make_background(W, H2, seed)
        img = Image.alpha_composite(bg, layer)
        img = Image.alpha_composite(img, make_foreground(W, H2, seed))
        img = img.convert("RGB")

        label = (g.get("label") or "").strip() or group_label(gi)
        safe = re.sub(r"[\\/:*?\"<>|]+", "", label) or group_label(gi)
        fn = "单组图_%s_%s.png" % (safe, ts)
        fp = os.path.join(SINGLE_DIR, fn)
        k = 1
        while os.path.exists(fp):
            fn = "单组图_%s_%s_%d.png" % (safe, ts, k)
            fp = os.path.join(SINGLE_DIR, fn)
            k += 1
        try:
            img.save(fp, "PNG", optimize=True)
        except Exception as e:
            return {"error": "单图保存失败：%s" % e}
        images.append({"index": gi + 1, "title": label, "filename": fn, "path": fp,
                       "url": "/groupimage/" + quote(fn), "width": W, "height": H2})
    return {"ok": True, "count": len(images), "images": images}


def _unique_long_path(ts, suffix=""):
    fn = "选牌长图_%s%s.png" % (ts, suffix)
    fp = os.path.join(LONG_DIR, fn)
    n = 1
    while os.path.exists(fp):
        fn = "选牌长图_%s%s_%d.png" % (ts, suffix, n)
        fp = os.path.join(LONG_DIR, fn)
        n += 1
    return fn, fp


def compose_long_image(payload):
    W = 750
    PAD = 56
    CW = W - PAD * 2

    title = (payload.get("title") or "").strip() or "选牌"
    subtitle = (payload.get("subtitle") or "").strip()
    guide = (payload.get("guide") or "").strip()
    footer = (payload.get("footer") or "").strip()
    groups = payload.get("groups")
    if not isinstance(groups, list):
        groups = []
    groups = groups[:MAX_GROUPS]
    if not groups:
        groups = random_draw(3)["groups"]

    _norm = []
    for _g in groups:
        _gg = dict(_g) if isinstance(_g, dict) else {}
        if not str(_gg.get("text") or "").strip():
            _parts = [x.strip() for x in (str(_gg.get("analysis") or ""),
                                          str(_gg.get("advice") or "")) if x.strip()]
            if _parts:
                _gg["text"] = "\n\n".join(_parts)
        _norm.append(_gg)
    groups = _norm

    # 封面优先级：① 上传的总封面 ② 未上传则用各组子封面拼一张并标注组名 ③ 都没有才用内置 cover_1~3
    cover_path = ""
    up_cover = _upload_path(payload.get("cover_file"))
    if up_cover:
        cover_path = up_cover
    else:
        grid = _compose_subcover_grid(groups, W)
        if grid is not None:
            try:
                os.makedirs(TMP_DIR, exist_ok=True)
                _gfn = os.path.join(TMP_DIR, "cover_grid_%s.png" %
                                    datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
                grid.save(_gfn, "PNG")
                cover_path = _gfn
            except Exception:
                cover_path = ""
        if not cover_path:
            try:
                cover_idx = int(payload.get("cover") or 1)
            except Exception:
                cover_idx = 1
            if cover_idx not in (1, 2, 3):
                cover_idx = 1
            cp = os.path.join(ASSET_DIR, "cover_%d.png" % cover_idx)
            if os.path.isfile(cp):
                cover_path = cp

    H = 5200
    layer = None
    yend = 0
    segs = []
    for _ in range(8):
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        yend, segs = _render_all(layer, draw, W, PAD, CW, title, subtitle,
                                 guide, footer, groups, cover_path)
        if yend + 20 <= H:
            break
        H = int(yend) + 400

    H2 = int(min(yend + 20, H))
    layer = layer.crop((0, 0, W, H2))

    bg = make_background(W, H2)
    out = Image.alpha_composite(bg, layer)
    out = Image.alpha_composite(out, make_foreground(W, H2))
    out = out.convert("RGB")

    os.makedirs(LONG_DIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fn, fp = _unique_long_path(ts)
    try:
        out.save(fp, "PNG", optimize=True)
    except Exception as e:
        return {"error": "长图保存失败：%s" % e}

    stem = os.path.splitext(fn)[0]
    fixed = []
    for s in segs:
        y0 = max(0, min(H2 - 1, int(s["y0"])))
        y1 = max(y0 + 1, min(H2, int(s["y1"])))
        fixed.append({"key": s["key"], "title": s["title"], "y0": y0, "y1": y1})

    if payload.get("export_segments"):
        for s in fixed:
            sfn = "%s_%s.png" % (stem, s["title"])
            sp = os.path.join(LONG_DIR, sfn)
            k = 1
            while os.path.exists(sp):
                sfn = "%s_%s_%d.png" % (stem, s["title"], k)
                sp = os.path.join(LONG_DIR, sfn)
                k += 1
            try:
                out.crop((0, s["y0"], W, s["y1"])).save(sp, "PNG", optimize=True)
                s["filename"] = sfn
                s["path"] = sp
                s["url"] = "/longimage/" + quote(sfn)
            except Exception as e:
                s["error"] = str(e)

    return {"ok": True, "filename": fn, "path": fp,
            "url": "/longimage/" + quote(fn),
            "width": W, "height": H2,
            "segments": fixed,
            "cover_used": os.path.basename(cover_path) if cover_path else ""}


def compose_single_long_image(payload):
    """单图版长图：先用单图版式逐组绘制，再按组竖向拼成一张长图。
    与 compose_long_image（长图版式）完全独立，互不影响。
    """
    res = compose_group_images(payload)
    if res.get("error"):
        return res
    items = res.get("images") or []
    if not items:
        return {"error": "暂无单图可拼接，请先确认组数据"}

    opened = []
    for it in items:
        fp = str(it.get("path") or "")
        try:
            opened.append(Image.open(fp).convert("RGB"))
        except Exception as e:
            return {"error": "读取单图失败：%s" % e}

    try:
        _g = payload.get("gap")
        gap = 0 if _g in (None, "") else int(_g)
    except Exception:
        gap = 0
    gap = max(0, min(120, gap))

    W = max([im.width for im in opened] + [750])
    H = sum(im.height for im in opened) + gap * (len(opened) - 1)
    canvas = Image.new("RGB", (W, H), (8, 9, 16))

    segs = []
    y = 0
    for idx, im in enumerate(opened):
        canvas.paste(im, ((W - im.width) // 2, y))
        title = str((items[idx] or {}).get("title") or ("第%d组" % (idx + 1))).strip()
        if not title:
            title = "第%d组" % (idx + 1)
        segs.append({"key": "group_%d" % (idx + 1), "title": title,
                     "y0": y, "y1": y + im.height})
        y += im.height + gap

    os.makedirs(LONG_DIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base = "单组拼接_%s" % ts
    fn = base + ".png"
    fp = os.path.join(LONG_DIR, fn)
    k = 1
    while os.path.exists(fp):
        fn = "%s_%d.png" % (base, k)
        fp = os.path.join(LONG_DIR, fn)
        k += 1
    try:
        canvas.save(fp, "PNG", optimize=True)
    except Exception as e:
        return {"error": "单图长图保存失败：%s" % e}

    stem = os.path.splitext(fn)[0]
    if payload.get("export_segments"):
        for s in segs:
            sfn = "%s_%s.png" % (stem, s["title"])
            sp = os.path.join(LONG_DIR, sfn)
            k2 = 1
            while os.path.exists(sp):
                sfn = "%s_%s_%d.png" % (stem, s["title"], k2)
                sp = os.path.join(LONG_DIR, sfn)
                k2 += 1
            try:
                canvas.crop((0, s["y0"], W, s["y1"])).save(sp, "PNG", optimize=True)
                s["filename"] = sfn
                s["path"] = sp
                s["url"] = "/longimage/" + quote(sfn)
            except Exception as e:
                s["error"] = str(e)

    return {"ok": True, "filename": fn, "path": fp,
            "url": "/longimage/" + quote(fn),
            "width": W, "height": H,
            "segments": segs, "mode": "single", "count": len(segs)}


def crop_long_image(payload):
    fn = os.path.basename(str(payload.get("filename") or "").replace("\\", "/").strip())
    if not fn or ".." in fn:
        return {"error": "缺少长图文件名"}
    base = os.path.normpath(LONG_DIR)
    src = os.path.normpath(os.path.join(base, fn))
    if src != base and not src.startswith(base + os.sep):
        return {"error": "非法路径"}
    if not os.path.isfile(src):
        return {"error": "长图不存在：%s" % fn}
    im = _open_rgb(src)
    if im is None:
        return {"error": "长图读取失败"}
    h = im.height
    try:
        y0 = int(float(payload.get("y0")))
    except Exception:
        y0 = 0
    try:
        y1 = int(float(payload.get("y1")))
    except Exception:
        y1 = h
    y0 = max(0, min(h - 1, y0))
    y1 = max(y0 + 20, min(h, y1))
    out = im.crop((0, y0, im.width, y1))

    stem = os.path.splitext(fn)[0]
    ts = datetime.datetime.now().strftime("%H%M%S")
    ofn = "%s_crop_%s_%d-%d.png" % (stem, ts, y0, y1)
    ofp = os.path.join(base, ofn)
    guard = 1
    while os.path.exists(ofp):
        ofn = "%s_crop_%s_%d-%d_%d.png" % (stem, ts, y0, y1, guard)
        ofp = os.path.join(base, ofn)
        guard += 1
    try:
        out.save(ofp, "PNG", optimize=True)
    except Exception as e:
        return {"error": "裁剪图保存失败：%s" % e}
    return {"ok": True, "filename": ofn, "path": ofp,
            "url": "/longimage/" + quote(ofn),
            "width": out.width, "height": out.height, "y0": y0, "y1": y1}


# ==================== 前端页面 ====================

PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PPTAROT · 管理后台</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:"Microsoft YaHei", sans-serif; background:linear-gradient(135deg,#1a1033 0%,#2d1b4e 60%,#4a2c6d 100%); min-height:100vh; color:#e8dcf5; }
.container { max-width:860px; margin:0 auto; padding:24px 16px 60px; }
h1 { text-align:center; font-size:28px; letter-spacing:6px; color:#f5d78e; margin:18px 0 6px; text-shadow:0 0 18px rgba(245,215,142,.35); }
.sub { text-align:center; color:#a992c7; font-size:13px; margin-bottom:22px; }
.tabs { display:flex; justify-content:center; gap:8px; margin-bottom:20px; }
.tab { padding:9px 26px; border-radius:20px; background:#3a2660; color:#cbb8e8; cursor:pointer; border:1px solid #5a3d8f; font-size:14px; transition:.2s; }
.tab.active { background:#f5d78e; color:#2d1b4e; font-weight:bold; border-color:#f5d78e; }
.card { background:rgba(255,255,255,.07); border:1px solid rgba(245,215,142,.25); border-radius:14px; padding:20px; margin-bottom:16px; box-shadow:0 4px 20px rgba(0,0,0,.3); }
.card h3 { color:#f5d78e; font-size:16px; margin-bottom:14px; }
label { display:block; font-size:13px; color:#cbb8e8; margin:12px 0 6px; }
input[type=text], select, textarea { width:100%; padding:10px 12px; border-radius:8px; border:1px solid #5a3d8f; background:#241639; color:#f0e6ff; font-size:14px; outline:none; }
input:focus, select:focus, textarea:focus { border-color:#f5d78e; }
textarea { min-height:72px; resize:vertical; }
.hint { font-size:12px; color:#8f7bb0; margin-top:5px; }
.btn { padding:10px 22px; border:none; border-radius:8px; cursor:pointer; font-size:14px; font-weight:bold; transition:.2s; }
.btn-gold { background:#f5d78e; color:#2d1b4e; margin-top:14px; }
.btn-gold:hover { background:#ffdf9e; }
.btn-purple { background:#5a3d8f; color:#f0e6ff; }
.btn-purple:hover { background:#6d4ca8; }
.btn-small { padding:6px 14px; font-size:12px; border-radius:6px; }
.hist-box { background:rgba(245,215,142,.08); border:1px solid rgba(245,215,142,.4); border-radius:10px; padding:12px; margin-top:10px; font-size:13px; color:#e8dcf5; max-height:220px; overflow:auto; }
.hist-box .item { padding:6px 0; border-bottom:1px dashed rgba(255,255,255,.12); }
.hist-box .item:last-child { border-bottom:none; }
.result { background:#101020; border:1px solid #5a3d8f; border-radius:10px; padding:14px; margin-top:14px; white-space:pre-wrap; font-size:13px; line-height:1.7; color:#e8dcf5; max-height:420px; overflow:auto; display:none; }
.toolbar { display:flex; gap:10px; margin-top:12px; align-items:center; }
.toolbar .btn { margin-top:0; }
.status { font-size:13px; margin-top:10px; color:#7ed8a8; display:none; }
.msg-err { color:#f0a0a0; }
.list-item { background:rgba(255,255,255,.05); border-radius:10px; padding:12px; margin-bottom:10px; border:1px solid rgba(255,255,255,.1); font-size:13px; line-height:1.8; }
.list-item b { color:#f5d78e; }
.field-row { margin:6px 0 0; line-height:1.9; }
.fb-tag { display:inline-block; padding:2px 10px; border-radius:10px; font-size:12px; margin-left:8px; }
.fb-yes { background:#2c5a3c; color:#a8e6c3; }
.fb-no { background:#5a2c3c; color:#f0a0a0; }
.cards-row { display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; }
.chip { background:#3a2660; border:1px solid #6d4ca8; padding:4px 12px; border-radius:14px; font-size:12px; color:#e8dcf5; }
.chip b { color:#f5d78e; }
.ig-row { display:flex; gap:14px; flex-wrap:wrap; }
.ig-row>div { flex:1; min-width:140px; }
.cover-pick { display:flex; gap:12px; margin-top:8px; flex-wrap:wrap; }
.cover-pick .thumb { width:110px; height:132px; border-radius:10px; overflow:hidden; border:2px solid #4b3468; cursor:pointer; position:relative; background:#241639; }
.cover-pick .thumb img { width:100%; height:100%; object-fit:cover; display:block; }
.cover-pick .thumb.on { border-color:#f5d78e; box-shadow:0 0 12px rgba(245,215,142,.55); }
.cover-pick .thumb span { position:absolute; left:0; bottom:0; width:100%; background:rgba(0,0,0,.55); color:#f5d78e; font-size:11px; text-align:center; padding:2px 0; }
.grp { background:rgba(255,255,255,.05); border:1px solid rgba(168,216,232,.28); border-radius:12px; padding:14px; margin-bottom:14px; }
.grp-head { display:flex; gap:10px; align-items:center; margin-bottom:10px; }
.slots { display:grid; grid-template-columns:repeat(auto-fill, minmax(170px, 1fr)); gap:8px; margin-bottom:6px; align-items:start; }
.slot { background:#1d2f3f; border:1px solid #3f5f78; border-radius:10px; padding:6px; min-width:0; }
.slot img { width:100%; margin:0 auto; display:block; border-radius:5px; background:#0d1a24; cursor:zoom-in; }
.slot select { margin-top:5px; font-size:11px; padding:3px 2px; width:100%; box-sizing:border-box; }
.ig-preview { margin-top:16px; display:none; }
.ig-preview img { width:100%; max-width:750px; border-radius:10px; border:1px solid #4b3468; display:block; }
.ig-preview a { display:inline-block; margin-top:12px; text-decoration:none; }
.sub-cover { display:flex; gap:12px; align-items:center; margin-bottom:12px; padding:10px; background:rgba(168,216,232,.07); border:1px dashed rgba(168,216,232,.35); border-radius:10px; }
.sub-cover .sc-thumb { width:120px; height:76px; border-radius:8px; overflow:hidden; background:#12212c; border:1px solid #3f5f78; display:flex; align-items:center; justify-content:center; }
.sub-cover .sc-thumb img { width:100%; height:100%; object-fit:cover; }
.sub-cover .sc-thumb i { font-size:11px; color:#7f9aab; font-style:normal; }
.sub-cover .sc-ops { display:flex; flex-direction:column; gap:6px; }
.seg-list { display:flex; flex-wrap:wrap; gap:10px; margin-top:8px; }
.seg-item { background:#1d2f3f; border:1px solid #3f5f78; border-radius:10px; padding:8px 10px; font-size:12px; }
.seg-item b { color:#f5d78e; display:block; margin-bottom:4px; }
.seg-item a { color:#a8d8e8; text-decoration:none; }
.seg-item .rg { color:#7f9aab; }
.nav{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 16px;}
.nav .tab{display:inline-block;border:1px solid rgba(245,215,142,.32);background:rgba(245,215,142,.06);
color:#cfc6ea;border-radius:12px;padding:10px 20px;font-size:14px;letter-spacing:1px;cursor:pointer;font-family:inherit;transition:.15s;}
.nav .tab.active{background:rgba(245,215,142,.22);color:#f5d78e;border-color:rgba(245,215,142,.7);font-weight:700;}
.hub{display:flex;gap:14px;flex-wrap:wrap;margin-top:4px;}
.hubcard{flex:1 1 230px;border:1px solid rgba(245,215,142,.26);background:rgba(255,255,255,.04);
border-radius:16px;padding:22px 18px;cursor:pointer;transition:.15s;}
.hubcard:hover{background:rgba(245,215,142,.10);border-color:rgba(245,215,142,.6);}
.hubcard .hi{font-size:26px;line-height:1.2;}
.hubcard .ht{font-size:16px;color:#f5d78e;font-weight:700;margin:8px 0 5px;letter-spacing:1px;}
.hubcard .hd{font-size:12.5px;color:#9c93bd;line-height:1.7;}
.back{border:1px solid rgba(168,160,220,.4);background:rgba(120,110,180,.18);color:#cfc6ea;border-radius:999px;
padding:6px 14px;font-size:12.5px;margin-bottom:12px;cursor:pointer;font-family:inherit;}
.back:active{background:rgba(120,110,180,.34);}
/* ===== 左侧栏布局 ===== */
body{overflow-x:hidden;}
.shell{display:flex;min-height:100vh;align-items:stretch;}
.side{width:236px;flex:0 0 236px;position:sticky;top:0;height:100vh;box-sizing:border-box;
display:flex;flex-direction:column;padding:22px 14px 16px;
background:linear-gradient(180deg,rgba(24,16,44,.97),rgba(15,11,28,.97));
border-right:1px solid rgba(245,215,142,.18);z-index:60;transition:left .22s;}
.side .logo{font-size:18px;letter-spacing:4px;color:#f5d78e;text-align:center;text-shadow:0 0 14px rgba(245,215,142,.4)}
.side .sidesub{text-align:center;font-size:11px;letter-spacing:4px;color:#8b82ab;margin:7px 0 18px}
.menu{flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;padding-bottom:8px}
.m1{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:11px 12px;border-radius:11px;
font-size:13.5px;color:#d6cdea;cursor:pointer;letter-spacing:1px;transition:.15s;user-select:none}
.m1:hover{background:rgba(245,215,142,.09);color:#f5d78e}
.m1.active{background:rgba(245,215,142,.18);color:#f5d78e;font-weight:700}
.m1 .ar{font-style:normal;font-size:13px;color:#8b82ab;transition:transform .18s;display:inline-block}
.mgroup.open>.m1 .ar{transform:rotate(90deg);color:#f5d78e}
.m2wrap{max-height:0;overflow:hidden;transition:max-height .22s ease}
.mgroup.open>.m2wrap{max-height:340px}
.m2{margin:3px 0 3px 14px;padding:9px 12px;border-radius:9px;font-size:12.5px;color:#a99fc4;
cursor:pointer;border-left:2px solid rgba(245,215,142,.16);transition:.15s;letter-spacing:.5px}
.m2:hover{color:#f0d79c;background:rgba(245,215,142,.07)}
.m2.active{color:#1a1428;background:linear-gradient(120deg,#f0d79c,#e0b978);font-weight:700;border-left-color:#f0d79c}
.sidefoot{border-top:1px solid rgba(245,215,142,.14);padding-top:12px;margin-top:10px;display:flex;flex-direction:column;gap:6px}
.sidefoot a{font-size:12px;text-decoration:none;color:#9c93bd;padding:6px 10px;border-radius:8px;transition:.15s}
.sidefoot a:hover{background:rgba(245,215,142,.1);color:#f0d79c}
.main{flex:1;min-width:0}
.main .container{max-width:none;margin:0;padding:26px 26px 90px}
.sbtn{display:none;position:fixed;left:12px;top:12px;z-index:70;width:40px;height:40px;border-radius:11px;
border:1px solid rgba(245,215,142,.4);background:rgba(20,14,36,.92);color:#f0d79c;font-size:17px;cursor:pointer;font-family:inherit}
.smask{display:none;position:fixed;left:0;top:0;right:0;bottom:0;background:rgba(4,6,14,.62);z-index:55}
.smask.on{display:block}
/* 图片悬浮操作层：预览 + 下载 */
.ig-thumb{position:relative;display:inline-block;border-radius:10px;overflow:hidden;margin:10px 0;line-height:0;background:#0e1620;vertical-align:top}
.ig-thumb>img{display:block;width:240px;max-width:100%;border-radius:10px}
.ig-thumb.wide,.ig-thumb.wide>img{width:100%}
.ig-acts{position:absolute;left:0;top:0;right:0;bottom:0;display:flex;align-items:center;justify-content:center;gap:16px;background:rgba(6,10,18,.42);opacity:0;transition:opacity .16s}
.ig-thumb:hover .ig-acts{opacity:1}
.ig-act{width:46px;height:46px;border-radius:50%;border:0;background:rgba(255,255,255,.94);color:#26313d;display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0;box-shadow:0 4px 14px rgba(0,0,0,.35);transition:transform .14s,background .14s}
.ig-act:hover{transform:scale(1.08);background:#fff}
.ig-act svg{width:22px;height:22px;display:block}
@media (hover:none){ .ig-acts{opacity:1;background:rgba(6,10,18,.28)} }
@media (max-width:860px){
  .side{position:fixed;left:-270px;top:0;width:250px;flex:none;height:100vh}
  .side.open{left:0;box-shadow:0 0 44px rgba(0,0,0,.65)}
  .sbtn{display:block}
  .main .container{padding:64px 14px 80px}
}
@media (max-width:600px){ .tab{padding:8px 14px;font-size:12px;} }
</style>
</head>
<body>
<button class="sbtn" id="sBtn" aria-label="菜单">☰</button>
<div class="smask" id="sMask"></div>
<div class="shell">
<aside class="side" id="side">
  <div class="logo">PPTAROT🔮</div>
  <div class="sidesub">管 理 后 台</div>
  <nav class="menu" id="menu">
    <div class="mgroup open" data-view="home">
      <div class="m1 active" onclick="menuGo('home')"><span>📊 概览</span></div>
    </div>
    <div class="mgroup">
      <div class="m1" onclick="menuToggle(this)"><span>📁 案例管理</span><i class="ar">›</i></div>
      <div class="m2wrap">
        <div class="m2" data-view="new" onclick="menuGo('new')">案例记录</div>
        <div class="m2" data-view="history" onclick="menuGo('history')">案例库</div>
        <div class="m2" data-view="charts" onclick="menuGo('charts')">星盘数据</div>
      </div>
    </div>
    <div class="mgroup">
      <div class="m1" onclick="menuToggle(this)"><span>📈 数据统计</span><i class="ar">›</i></div>
      <div class="m2wrap">
        <div class="m2" data-view="stats" onclick="menuGo('stats')">使用概览</div>
        <div class="m2" data-view="events" onclick="menuGo('events')">行为明细</div>
        <div class="m2" data-view="visitors" onclick="menuGo('visitors')">访客记录</div>
      </div>
    </div>
    <div class="mgroup">
      <div class="m1" onclick="menuToggle(this)"><span>🎨 图文生成器</span><i class="ar">›</i></div>
      <div class="m2wrap">
        <div class="m2" data-view="ig" onclick="menuGo('ig')">抽牌出图</div>
        <div class="m2" data-view="igs" onclick="menuGo('igs')">每组单图</div>
      </div>
    </div>
    <div class="mgroup">
      <div class="m1" onclick="menuToggle(this)"><span>⚙️ 网站设置</span><i class="ar">›</i></div>
      <div class="m2wrap">
        <div class="m2" onclick="openSitePanel()">首页设置</div>
      </div>
    </div>
  </nav>
  <div class="sidefoot">
    <a href="/" target="_blank">→ 打开前台抽牌页</a>
    <a href="javascript:logout()">退出登录</a>
  </div>
</aside>
<main class="main">
<div class="container">

<!-- 后台首页：按钮总览 -->
<div id="tab-home">
  <div class="hub">
    <div class="hubcard" onclick="switchTab('history')">
      <div class="hi">📁</div>
      <div class="ht">案例库</div>
      <div class="hd">按客户称呼搜历史案例，心得与反馈随手改</div>
    </div>
    <div class="hubcard" onclick="switchTab('charts')">
      <div class="hi">🪐</div>
      <div class="ht">星盘数据</div>
      <div class="hd">客户在前台填的出生时间与星盘参数，自动存档</div>
    </div>
    <div class="hubcard" onclick="switchTab('tools')">
      <div class="hi">🧰</div>
      <div class="ht">工具</div>
      <div class="hd">案例记录 · 图文生成器</div>
    </div>
  </div>
</div>

<!-- 工具：二级按钮 -->
<div id="tab-tools" style="display:none;">
  <div class="hub">
    <div class="hubcard" onclick="switchTab('new')">
      <div class="hi">📝</div>
      <div class="ht">案例记录</div>
      <div class="hd">录入牌面 · 生成AI提示词 · 保存为案例</div>
    </div>
    <div class="hubcard" onclick="switchTab('ig')">
      <div class="hi">🎨</div>
      <div class="ht">图文生成器</div>
      <div class="hd">抽牌出图 · 长图或单组图 · 公众号素材</div>
    </div>
  </div>
</div>

<!-- 新占卜 -->
<div id="tab-new" style="display:none;">
  <button class="back" onclick="menuGo('home')">← 返回概览</button>
  <div class="card">
    <h3>1 · 客户信息（首次与回头客通用）</h3>
    <label>客户称呼（必填，用于后续搜索；老客户输入后自动带出历史）</label>
    <input type="text" id="name" placeholder="客户称呼（必填），回车检测老客户" onblur="checkClient()" onkeydown="if(event.key==='Enter')checkClient()">
    <div class="hist-box" id="histBox" style="display:none;"></div>
  </div>

  <div class="card">
    <h3>2 · 本次占卜</h3>
    <label>问题类型</label>
    <select id="qtype">
      <option value="综合">综合</option><option value="事业">事业</option>
      <option value="情感">情感</option><option value="学业">学业</option><option value="财运">财运</option>
    </select>
    <label>客户提问</label>
    <textarea id="question" placeholder="例如：这次复合能成吗？"></textarea>
    <label>牌阵</label>
    <input type="text" id="spread" placeholder="例如：圣三角（可留空）">
    <label>牌面</label>
    <input type="text" id="cards" placeholder="格式：恋人 正, 宝剑三 逆（多张用逗号分隔）">
    <div class="hint">支持大阿卡纳与小阿卡纳，如：愚人 正、圣杯骑士 逆、权杖一、金币十</div>
    <div class="cards-row" id="chipBox"></div>
    <button class="btn btn-gold" onclick="genPrompt()">✨ 生成 AI 提示词</button>
    <div class="result" id="result"></div>
    <div class="toolbar" id="toolbar" style="display:none;">
      <button class="btn btn-purple btn-small" onclick="copyPrompt()">复制提示词</button>
      <button class="btn btn-purple btn-small" onclick="saveCase()">保存为案例</button>
      <input type="text" id="reading" placeholder="你的心得（保存时填，可留空，事后可在历史档案里修改）" style="flex:1;">
    </div>
    <div class="status" id="status"></div>
  </div>
</div>

<!-- 案例库 -->
<div id="tab-history" style="display:none;">
  <div class="card">
    <h3>案例库（每条案例的心得与反馈都可直接编辑）</h3>
    <label>客户称呼（输入 * 查看全部客户，回车搜索）</label>
    <input type="text" id="hisName" placeholder="输入客户称呼，回车搜索；* 查看全部客户" onkeydown="if(event.key==='Enter')loadHistory()">
    <div id="hisList" style="margin-top:12px;"></div>
  </div>
</div>

<!-- 星盘数据 -->
<div id="tab-charts" style="display:none;">
  <style>
  .cht{width:100%;border-collapse:collapse;font-size:12.5px}
  .cht th{text-align:left;padding:8px 8px;color:#9c93bd;font-weight:400;letter-spacing:1px;border-bottom:1px solid rgba(245,215,142,.22);white-space:nowrap}
  .cht td{padding:9px 8px;border-bottom:1px solid rgba(255,255,255,.07);color:#d6cdea;vertical-align:top}
  .cht tr:hover td{background:rgba(245,215,142,.05)}
  .chdet{padding:6px 2px 12px;font-size:12px;line-height:2;color:#b6adcd}
  .chdet b{color:#f0d79c;font-weight:600}
  .chchip{display:inline-block;margin:0 6px 6px 0;padding:2px 9px;border-radius:999px;font-size:11.5px;
    border:1px solid rgba(245,215,142,.3);color:#e8dcc0}
  </style>
  <div class="card">
    <h3>星盘数据（前台客户提交的出生信息与星盘参数）</h3>
    <div class="toolbar">
      <button class="btn btn-purple btn-small" onclick="loadCharts()">刷新</button>
      <span class="hint" id="chTip">读取中…</span>
    </div>
    <div class="hint" style="margin-top:8px;">客户在前台填的出生时间会自动存档到这里，一人可多条，用来复盘。</div>
    <div id="chList" style="margin-top:14px;overflow-x:auto;"></div>
  </div>
</div>

<!-- 数据统计 · 使用概览 -->
<div id="tab-stats" style="display:none;">
  <style>
  .kpi{display:grid;grid-template-columns:repeat(auto-fill,minmax(148px,1fr));gap:12px}
  .kpi .k{border:1px solid rgba(245,215,142,.26);background:rgba(255,255,255,.04);border-radius:14px;padding:14px 16px}
  .kpi .k .kt{font-size:12px;color:#9c93bd;letter-spacing:1px}
  .kpi .k .kv{font-size:26px;color:#f5d78e;font-weight:700;margin-top:6px;line-height:1.1}
  .kpi .k .kd{font-size:11.5px;color:#8b82ab;margin-top:5px}
  .bars{display:flex;align-items:flex-end;gap:5px;height:110px;margin:16px 0 26px}
  .bars .bcol{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;height:100%;position:relative}
  .bars .bar{width:100%;background:linear-gradient(180deg,#f0d79c,#b0783a);border-radius:4px 4px 0 0;min-height:2px}
  .bars .bday{font-size:10px;color:#8b82ab;margin-top:4px;white-space:nowrap}
  .bars .bnum{font-size:10px;color:#cbb8e8;margin-bottom:3px}
  .dstt{width:100%;border-collapse:collapse;font-size:12.5px}
  .dstt th{text-align:left;padding:8px;color:#9c93bd;font-weight:400;letter-spacing:1px;border-bottom:1px solid rgba(245,215,142,.22);white-space:nowrap}
  .dstt td{padding:9px 8px;border-bottom:1px solid rgba(255,255,255,.07);color:#d6cdea;vertical-align:top}
  .dstt tr:hover td{background:rgba(245,215,142,.05)}
  .etag{display:inline-block;padding:1px 9px;border-radius:999px;font-size:11.5px;white-space:nowrap;
    border:1px solid rgba(245,215,142,.3);color:#e8dcc0}
  .edet{padding:4px 2px 10px;font-size:12px;line-height:2;color:#b6adcd;word-break:break-all}
  .edet b{color:#f0d79c;font-weight:600}
  .fline{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:10px}
  .fline select,.fline input{margin:0;max-width:220px}
  .pager{display:flex;gap:10px;align-items:center;margin-top:12px;font-size:12.5px;color:#9c93bd}
  .empty{color:#8b82ab;font-size:13px;padding:16px 0}
  </style>
  <div class="card">
    <h3>使用概览（前台匿名行为，只有你自己能看到）</h3>
    <div class="fline">
      <button class="btn btn-purple btn-small" onclick="loadStats()">刷新</button>
      <span class="hint" id="stTip">读取中…</span>
    </div>
    <div class="kpi" id="stKpi" style="margin-top:14px;"></div>
    <h3 style="margin-top:22px;font-size:14px;">近 14 天使用曲线</h3>
    <div class="bars" id="stBars"></div>
    <h3 style="margin-top:8px;font-size:14px;">抽牌分类分布</h3>
    <div id="stCats" style="margin-top:10px;"></div>
    <h3 style="margin-top:22px;font-size:14px;">最近 12 条行为</h3>
    <div id="stRecent" style="margin-top:10px;overflow-x:auto;"></div>
  </div>
</div>

<!-- 数据统计 · 行为明细 -->
<div id="tab-events" style="display:none;">
  <div class="card">
    <h3>行为明细（谁在什么时候抽了什么）</h3>
    <div class="fline">
      <select id="evType" onchange="loadEvents(1)">
        <option value="all">全部类型</option>
        <option value="daily">每日塔罗</option>
        <option value="draw">塔罗抽牌</option>
        <option value="answer">答案之书</option>
        <option value="dice">星骰</option>
      </select>
      <select id="evDays" onchange="loadEvents(1)">
        <option value="0">全部时间</option>
        <option value="1">今天</option>
        <option value="7">近 7 天</option>
        <option value="30">近 30 天</option>
      </select>
      <input type="text" id="evKw" placeholder="搜问题 / 结果 / IP，回车搜" onkeydown="if(event.key==='Enter')loadEvents(1)">
      <button class="btn btn-purple btn-small" onclick="loadEvents(1)">查询</button>
      <span class="hint" id="evTip"></span>
    </div>
    <div id="evList" style="margin-top:14px;overflow-x:auto;"></div>
    <div class="pager">
      <button class="btn btn-small" onclick="evPage(-1)">上一页</button>
      <span id="evPageTxt">1 / 1</span>
      <button class="btn btn-small" onclick="evPage(1)">下一页</button>
    </div>
  </div>
</div>

<!-- 数据统计 · 访客记录 -->
<div id="tab-visitors" style="display:none;">
  <div class="card">
    <h3>访客记录（后台用户表的雏形，后期接登录账号）</h3>
    <div class="fline">
      <button class="btn btn-purple btn-small" onclick="loadVisitors()">刷新</button>
      <input type="text" id="vsKw" placeholder="搜 IP / 浏览器标识，回车搜" onkeydown="if(event.key==='Enter')loadVisitors()">
      <span class="hint" id="vsTip"></span>
    </div>
    <div id="vsList" style="margin-top:14px;overflow-x:auto;"></div>
  </div>
</div>

<!-- 图文生成器 -->
<div id="tab-ig" style="display:none;">
  <button class="back" onclick="menuGo('home')">← 返回概览</button>
  <div class="card">
    <h3>1 · 抽牌</h3>
    <div class="toolbar">
      <button class="btn btn-purple btn-small" onclick="igDrawAll()">重新随机抽牌</button>
      <button class="btn btn-purple btn-small" onclick="igAddGroup()">+ 添加一组</button>
      <span class="hint" id="igGroupCount"></span>
    </div>
    <div class="hint">78 张牌池内纯随机、不放回抽取（1~10 组，每组 3 张，组间不重复），正逆位由程序随机决定，无需设置。</div>
  </div>

  <div class="card">
    <h3>2 · 封面与标题</h3>
    <label>总封面底图（点选内置，或上传自己的图片）</label>
    <div class="cover-pick" id="igCovers"></div>
    <div class="toolbar" style="margin-top:12px;">
      <button class="btn btn-purple btn-small" onclick="igPickUploadCover()">上传总封面</button>
      <button class="btn btn-small" onclick="igResetCover()">恢复内置</button>
      <input type="file" id="igCoverFile" accept="image/*" style="display:none;" onchange="igDoUploadCover(this)">
      <span class="hint" id="igCoverTip">当前使用：内置底图 1</span>
    </div>
    <label>封面大标题</label>
    <input type="text" id="igTitle" value="选牌" placeholder="例如：三组选牌，你的答案藏在哪一张里">
    <label>副标题</label>
    <input type="text" id="igSub" value="凭直觉，选最有感觉的一组">
    <label>组别引导语</label>
    <input type="text" id="igGuide" value="静心深呼吸三次，从下面几组牌中选择最吸引你的一组">
    <label>页脚公众号名</label>
    <input type="text" id="igFooter" value="" placeholder="例如：@你的公众号名">

  </div>

  <div class="card">
    <h3>3 · 牌面与文案（可自由增删组 · 每组可加子封面）</h3>
    <div id="igGroupsBox"></div>
    <div class="toolbar">
      <button class="btn btn-purple btn-small" onclick="igAddGroup()">+ 添加一组</button>
      <button class="btn btn-purple btn-small" onclick="igCopyList()">复制抽牌结果清单</button>
    </div>
    <div class="status" id="igStatus"></div>
  </div>

  <div class="card">
    <h3>4 · 长图出图</h3>
    <div class="toolbar">
      <button class="btn btn-gold" onclick="igGenerate(false)">生成长图（全部拼一张）</button>
      <button class="btn btn-purple btn-small" onclick="igGenerate(true)">长图 + 分段导出</button>
    </div>
    <div class="hint">长图：750px 竖版，封面 + 所有组竖向拼成一张，存 output/longimage/。每组单图已独立成单独功能页，见左侧「图文生成器 → 每组单图」。</div>

    <div class="ig-preview" id="igPreview">
      <img id="igPreviewImg" src="" alt="长图预览">
      <div class="toolbar">
        <a class="btn btn-purple btn-small" id="igDownload" href="" download>下载整张长图</a>
      </div>
      <div class="hint" id="igPath"></div>

      <div id="igSegBox" style="display:none;margin-top:18px;">
        <label>分段导出（封面 / 各组 / 页脚，各自一张 PNG）</label>
        <div class="seg-list" id="igSegList"></div>
        <div class="toolbar" style="margin-top:10px;">
          <button class="btn btn-purple btn-small" onclick="igExportAll()">全部导出</button>
        </div>
      </div>

    </div>

  </div>
</div>

<div id="tab-igs" style="display:none;">
  <button class="back" onclick="menuGo('home')">← 返回概览</button>

  <div class="card">
    <h3>1 · 单图版参数</h3>
    <label>作者名（显示在每组标签右侧）</label>
    <input type="text" id="igAuthor" value="" placeholder="例如：Starmoon / PPTAROT">
    <label>头像（选填，圆形显示在作者名左侧）</label>
    <div class="toolbar">
      <button class="btn btn-purple btn-small" onclick="igPickAvatar()">上传头像</button>
      <button class="btn btn-small" onclick="igClearAvatar()">移除头像</button>
      <input type="file" id="igAvatarFile" accept="image/*" style="display:none;" onchange="igDoUploadAvatar(this)">
      <span class="hint" id="igAvatarTip">未上传</span>
    </div>
    <label>解读区导语</label>
    <input type="text" id="igLead" value="亲爱的，先深呼吸，看看牌想对你说什么">
    <label>免责声明</label>
    <input type="text" id="igDisclaimer" value="仅供参考，命运永远握在自己手里">
  </div>

  <div class="card">
    <h3>2 · 抽牌与牌面文案（本页独立）</h3>
    <div class="hint">本页自己抽牌、自己写文案，和「抽牌出图」页各存一份，互不覆盖。</div>
    <div class="toolbar">
      <span class="hint" style="margin:0;">组数</span>
      <input type="number" id="igsDrawCount" value="3" min="1" max="12" style="width:88px;">
      <button class="btn btn-gold btn-small" onclick="igsDraw()">抽牌</button>
      <button class="btn btn-purple btn-small" onclick="igsAddGroup()">添加一组</button>
      <button class="btn btn-small" onclick="igsResetGroups()">清空重抽</button>
    </div>
    <div class="hint" id="igsGroupCount"></div>
    <div id="igsEditBox"></div>
    <div class="status" id="igsStatus"></div>
  </div>

  <div class="card">
    <h3>3 · 生成每组单图</h3>
    <div class="toolbar">
      <button class="btn btn-gold" onclick="igGenerateGroup()">生成每组单图（每组一张）</button>
      <button class="btn btn-purple btn-small" onclick="igDownloadSingles()">全部下载单图</button>
    </div>
    <div class="hint">单图方式：每组独立一张 750px 竖图，存 output/groupimage/。想在同一个页面里出长图，见下面「4 · 长图方式」。</div>
    <div id="igSingleBox" style="display:none;margin-top:12px;">
      <div class="seg-list" id="igSingleList"></div>
      <div class="hint" id="igSinglePath"></div>
    </div>
  </div>

  <div class="card">
    <h3>4 · 长图方式（单图版式竖排拼接）</h3>
    <div class="toolbar">
      <button class="btn btn-gold" onclick="igsGenerateLong(false)">生成长图（全部拼一张）</button>
      <button class="btn btn-purple btn-small" onclick="igsGenerateLong(true)">长图 + 分段导出</button>
    </div>
    <div class="hint">与「抽牌出图」的长图页完全独立：这里按单图版式逐组绘制，再竖向拼成一张长图，存 output/longimage/。每一段就是一组的单图。</div>
    <div class="toolbar" style="margin-top:8px;">
      <span class="hint" style="margin:0;">组间留白（px）</span>
      <input type="number" id="igsGap" value="0" min="0" max="120" style="width:96px;">
      <span class="hint">默认 0（无缝拼接），想留白再改大</span>
    </div>
    <div id="igsPreview" style="display:none;margin-top:12px;">
      <div class="ig-thumb wide">
        <img id="igsPreviewImg" src="" alt="单图版长图">
        <div class="ig-acts">
          <button type="button" class="ig-act" title="预览" onclick="igZoomLong()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7z"></path><circle cx="12" cy="12" r="3"></circle></svg></button>
          <button type="button" class="ig-act" title="下载" onclick="igDownloadLong()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"></path><path d="M7 11l5 5 5-5"></path><path d="M4 20h16"></path></svg></button>
        </div>
      </div>
      <div class="toolbar">
        <a class="btn btn-purple btn-small" id="igsDownload" href="#" download>下载整张长图</a>
      </div>
      <div class="hint" id="igsLongPath"></div>
    </div>
    <div id="igsSegBox" style="display:none;margin-top:18px;">
      <div class="seg-list" id="igsSegList"></div>
      <div class="toolbar">
        <button class="btn btn-purple btn-small" onclick="igsExportAll(false)">全部导出</button>
        <button class="btn btn-small" onclick="igsDownloadAllSegs()">全部下载分段</button>
      </div>
    </div>
    <div class="status" id="igsLongStatus"></div>
  </div>
</div>
</div>

<script>
let currentPrompt = '';
let currentName = '';

function menuGo(tab){
  switchTab(tab);
  var s=document.getElementById('side'), m=document.getElementById('sMask');
  if(s){ s.classList.remove('open'); }
  if(m){ m.classList.remove('on'); }
}
function menuToggle(el){
  var g = el.parentNode;
  if(g){ g.classList.toggle('open'); }
}
function openSitePanel(){
  // 实际打开逻辑由页面底部「首页设置」浮窗脚本覆盖（window.openSitePanel = openSite）
  var s=document.getElementById('side'), m=document.getElementById('sMask');
  if(s){ s.classList.remove('open'); }
  if(m){ m.classList.remove('on'); }
}
function switchTab(tab, root){
  if(tab==='new' || tab==='ig' || tab==='igs'){ root = 'tools'; }
  if(!root){ root = tab; }
  document.querySelectorAll('.m2').forEach(function(t){ t.classList.toggle('active', t.getAttribute('data-view')===tab); });
  document.querySelectorAll('.mgroup').forEach(function(g){
    var hit = g.querySelector('.m2.active');
    if(hit){ g.classList.add('open'); }
    var h = g.querySelector('.m1');
    if(h){ h.classList.toggle('active', !!hit || g.getAttribute('data-view')===tab); }
  });
  ['home','history','tools','new','ig','igs','charts','stats','events','visitors'].forEach(function(k){
    var el = document.getElementById('tab-'+k);
    if(el){ el.style.display = (k===tab) ? '' : 'none'; }
  });
  if(tab==='ig'){ igInit(); }
  if(tab==='igs'){ igsInit(); }
  if(tab==='charts'){ loadCharts(); }
  if(tab==='stats'){ loadStats(); }
  if(tab==='events'){ loadEvents(1); }
  if(tab==='visitors'){ loadVisitors(); }
  window.scrollTo(0,0);
}

/* ============ 星盘数据（前台客户提交的出生信息与星盘参数） ============ */
window.__CH = [];
function loadCharts(){
  var box = document.getElementById('chList'), tip = document.getElementById('chTip');
  if(!box) return;
  box.innerHTML = '<div class="hint">读取中…</div>';
  api('/api/charts', {}).then(function(d){
    if(!d || !d.ok){ box.innerHTML = '<div class="hint">读取失败，刷新重试</div>'; if(tip) tip.textContent=''; return; }
    var it = d.items || [];
    window.__CH = it;
    if(tip) tip.textContent = '共 ' + it.length + ' 条';
    if(!it.length){
      box.innerHTML = '<div class="hint">还没有客户提交星盘数据。客户在前台点「星盘」填完出生时间，这里就会自动出现。</div>';
      return;
    }
    var h = '<table class="cht"><thead><tr><th>ID</th><th>称呼</th><th>出生时间</th><th>出生地</th><th>太阳</th><th>月亮</th><th>上升</th><th>提交时间</th><th>操作</th></tr></thead><tbody>';
    it.forEach(function(r){
      h += '<tr><td>' + r.id + '</td>'
        + '<td>' + (r.name || '—') + '</td>'
        + '<td>' + (r.birth || '—') + (r.time_known ? '' : ' <span style="color:#8b82ab">(时间未知)</span>') + '</td>'
        + '<td>' + (r.region || '—') + '</td>'
        + '<td>' + (r.sun || '—') + '</td>'
        + '<td>' + (r.moon || '—') + '</td>'
        + '<td>' + (r.asc || '—') + '</td>'
        + '<td>' + (r.created_at || '') + '</td>'
        + '<td style="white-space:nowrap"><button class="btn btn-small" onclick="chartDetail(' + r.id + ')">参数</button> '
        + '<button class="btn btn-small" onclick="chartRemove(' + r.id + ')">删</button></td></tr>';
      h += '<tr id="chd' + r.id + '" style="display:none"><td colspan="9"><div class="chdet" id="chdc' + r.id + '"></div></td></tr>';
    });
    box.innerHTML = h + '</tbody></table>';
  }).catch(function(){
    box.innerHTML = '<div class="hint">连不上服务</div>';
  });
}
function chartDetail(id){
  var row = document.getElementById('chd' + id), cell = document.getElementById('chdc' + id);
  if(!row) return;
  if(row.style.display !== 'none'){ row.style.display = 'none'; return; }
  var rec = (window.__CH || []).filter(function(x){ return x.id === id; })[0];
  if(!rec){ return; }
  var ch = {};
  try { ch = JSON.parse(rec.chart_json || '{}'); } catch(e){ ch = {}; }
  var h = '';
  if(ch.planets && ch.planets.length){
    h += '<div style="margin-bottom:8px"><b>行星落点</b><br>';
    ch.planets.forEach(function(p){
      h += '<span class="chchip">' + p.n + ' ' + fmtLon(p.lon)
        + (p.house ? ' · ' + p.house + '宫' : '') + (p.retro ? ' R' : '') + '</span>';
    });
    h += '</div>';
  }
  if(ch.cusps && ch.cusps.length === 12){
    h += '<div style="margin-bottom:8px"><b>十二宫头</b><br>';
    ch.cusps.forEach(function(c, i){ h += '<span class="chchip">' + (i + 1) + '宫 ' + fmtLon(c) + '</span>'; });
    h += '</div>';
  }
  if(ch.aspects && ch.aspects.length){
    h += '<div><b>主要相位</b><br>';
    ch.aspects.forEach(function(a){
      h += '<span class="chchip">' + a.a + ' ' + a.t + ' ' + a.b + ' · ' + (a.orb != null ? a.orb.toFixed(1) + '°' : '') + '</span>';
    });
    h += '</div>';
  }
  if(!h) h = '<div class="hint">这条没有星盘参数（可能当时星盘引擎没加载）</div>';
  cell.innerHTML = h;
  row.style.display = '';
}
function fmtLon(lon){
  if(typeof lon !== 'number') return '';
  var s = ['白羊','金牛','双子','巨蟹','狮子','处女','天秤','天蝎','射手','摩羯','水瓶','双鱼'];
  var i = Math.floor(((lon % 360) + 360) % 360 / 30);
  var x = ((lon % 30) + 30) % 30;
  var d = Math.floor(x), m = Math.floor((x - d) * 60);
  return s[i] + ' ' + (d < 10 ? '0' : '') + d + '°' + (m < 10 ? '0' : '') + m + "'";
}
function chartRemove(id){
  if(!window.confirm('确定删除这条星盘数据？删了找不回来。')){ return; }
  api('/api/chart_remove', { id: id }).then(function(d){
    if(d && d.ok){ loadCharts(); }
    else { alert('删除失败'); }
  }).catch(function(){ alert('连不上服务'); });
}

/* ============ 数据统计（前台匿名行为，只给自己看） ============ */
var ET_NAME = { daily:'每日塔罗', draw:'塔罗抽牌', answer:'答案之书', dice:'星骰' };
var CAT_NAME = { love:'情感', career:'事业', study:'学业', money:'财运' };
var EV_PAGE = 1, EV_PAGESIZE = 50, EV_TOTAL = 0;
window.__EV = [];

function dsEsc(s){
  return String(s == null ? '' : s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function fmtDetail(s){
  if(!s) return '<span style="color:#7d749b">—</span>';
  try{
    var o = JSON.parse(s);
    if(o && typeof o === 'object'){
      var out = [];
      for(var k in o){
        if(o[k] === '' || o[k] == null) continue;
        out.push('<b>' + dsEsc(k) + '</b>: ' + dsEsc(o[k]));
      }
      return out.length ? out.join(' ｜ ') : '<span style="color:#7d749b">—</span>';
    }
  }catch(e){}
  return dsEsc(s);
}

function loadStats(){
  var tip = document.getElementById('stTip');
  if(tip) tip.textContent = '读取中…';
  api('/api/stats', { days: 14 }).then(function(d){
    if(!d || !d.ok){ if(tip) tip.textContent = '读取失败，刷新重试'; return; }
    if(tip) tip.textContent = '统计截至 ' + d.today;
    var bt = d.by_type || {};
    var kp = [
      ['总行为次数', d.total_events || 0, '所有功能合计'],
      ['独立访客', d.total_visitors || 0, '按浏览器标识去重'],
      ['今日行为', d.today_events || 0, '今天'],
      ['今日访客', d.today_visitors || 0, '今天']
    ];
    ['daily','draw','answer','dice'].forEach(function(t){
      var o = bt[t] || {};
      kp.push([ET_NAME[t], o.total || 0, '今日 ' + (o.today || 0)]);
    });
    document.getElementById('stKpi').innerHTML = kp.map(function(x){
      return '<div class="k"><div class="kt">' + x[0] + '</div><div class="kv">' + x[1] + '</div><div class="kd">' + x[2] + '</div></div>';
    }).join('');

    var sr = d.series || [], mx = 1;
    sr.forEach(function(r){ if(r.total > mx) mx = r.total; });
    document.getElementById('stBars').innerHTML = sr.map(function(r){
      var h = Math.round(r.total / mx * 100);
      return '<div class="bcol" title="' + r.day + '：共 ' + r.total + ' 次">'
        + '<div class="bnum">' + (r.total || '') + '</div>'
        + '<div class="bar" style="height:' + Math.max(h, 2) + '%"></div>'
        + '<div class="bday">' + r.day.slice(5) + '</div></div>';
    }).join('');

    var cd = d.cat_dist || [];
    document.getElementById('stCats').innerHTML = cd.length ? cd.map(function(c){
      return '<span class="etag" style="margin:0 8px 8px 0;display:inline-block">'
        + (CAT_NAME[c.cat] || c.cat) + ' · ' + c.n + ' 次</span>';
    }).join('') : '<div class="empty">还没有抽牌记录</div>';

    var rc = d.recent || [];
    if(!rc.length){
      document.getElementById('stRecent').innerHTML = '<div class="empty">还没有任何前台行为。前台有人点开抽牌，这里就会出现记录。</div>';
    } else {
      var h = '<table class="dstt"><thead><tr><th>时间</th><th>IP</th><th>行为</th><th>分类</th><th>问题</th><th>结果</th></tr></thead><tbody>';
      rc.forEach(function(r){
        h += '<tr><td style="white-space:nowrap">' + (r.created_at || '') + '</td>'
          + '<td>' + dsEsc(r.ip) + '</td>'
          + '<td><span class="etag">' + (ET_NAME[r.etype] || r.etype) + '</span></td>'
          + '<td>' + (CAT_NAME[r.cat] || r.cat || '—') + '</td>'
          + '<td>' + (r.q ? dsEsc(r.q) : '<span style="color:#7d749b">—</span>') + '</td>'
          + '<td>' + dsEsc(r.result || '—') + '</td></tr>';
      });
      document.getElementById('stRecent').innerHTML = h + '</tbody></table>';
    }
  }).catch(function(){ if(tip) tip.textContent = '连不上服务'; });
}

function loadEvents(p){
  if(p) EV_PAGE = p;
  var tip = document.getElementById('evTip');
  var box = document.getElementById('evList');
  if(!box) return;
  box.innerHTML = '<div class="hint">读取中…</div>';
  var body = {
    etype: (document.getElementById('evType') || {}).value || 'all',
    days: (document.getElementById('evDays') || {}).value || 0,
    kw: ((document.getElementById('evKw') || {}).value || '').trim(),
    limit: EV_PAGESIZE,
    offset: (EV_PAGE - 1) * EV_PAGESIZE
  };
  api('/api/events', body).then(function(d){
    if(!d || !d.ok){ box.innerHTML = '<div class="hint">读取失败</div>'; return; }
    EV_TOTAL = d.total || 0;
    window.__EV = d.items || [];
    var pages = Math.max(1, Math.ceil(EV_TOTAL / EV_PAGESIZE));
    if(tip) tip.textContent = '共 ' + EV_TOTAL + ' 条';
    var pt = document.getElementById('evPageTxt');
    if(pt) pt.textContent = EV_PAGE + ' / ' + pages;
    if(!window.__EV.length){
      box.innerHTML = '<div class="empty">这段条件下没有记录。</div>';
      return;
    }
    var h = '<table class="dstt"><thead><tr><th>时间</th><th>IP</th><th>行为</th><th>分类</th><th>问题</th><th>结果</th><th>详情</th></tr></thead><tbody>';
    window.__EV.forEach(function(r, i){
      h += '<tr><td style="white-space:nowrap">' + (r.created_at || '') + '</td>'
        + '<td>' + dsEsc(r.ip) + '</td>'
        + '<td><span class="etag">' + (ET_NAME[r.etype] || r.etype) + '</span></td>'
        + '<td>' + (CAT_NAME[r.cat] || r.cat || '—') + '</td>'
        + '<td>' + (r.q ? dsEsc(r.q) : '<span style="color:#7d749b">—</span>') + '</td>'
        + '<td>' + dsEsc(r.result || '—') + '</td>'
        + '<td style="white-space:nowrap"><button class="btn btn-small" onclick="evToggle(' + i + ')">展开</button></td></tr>';
      h += '<tr id="evd' + i + '" style="display:none"><td colspan="7"><div class="edet">'
        + '<div><b>访客</b>: ' + dsEsc(r.vid) + '</div>'
        + '<div><b>浏览器</b>: ' + dsEsc(r.ua) + '</div>'
        + '<div><b>详情</b>: ' + fmtDetail(r.detail) + '</div>'
        + '</div></td></tr>';
    });
    box.innerHTML = h + '</tbody></table>';
  }).catch(function(){ box.innerHTML = '<div class="hint">连不上服务</div>'; });
}

function evToggle(i){
  var row = document.getElementById('evd' + i);
  if(row) row.style.display = (row.style.display === 'none' ? '' : 'none');
}
function evPage(step){
  var pages = Math.max(1, Math.ceil(EV_TOTAL / EV_PAGESIZE));
  var n = EV_PAGE + step;
  if(n < 1 || n > pages) return;
  loadEvents(n);
}

function loadVisitors(){
  var box = document.getElementById('vsList'), tip = document.getElementById('vsTip');
  if(!box) return;
  box.innerHTML = '<div class="hint">读取中…</div>';
  var kw = ((document.getElementById('vsKw') || {}).value || '').trim();
  api('/api/visitors', { limit: 300, kw: kw }).then(function(d){
    if(!d || !d.ok){ box.innerHTML = '<div class="hint">读取失败</div>'; return; }
    var it = d.items || [];
    if(tip) tip.textContent = '共 ' + it.length + ' 个访客';
    if(!it.length){
      box.innerHTML = '<div class="empty">还没有访客记录。前台第一次访问时就会自动建档。</div>';
      return;
    }
    var h = '<table class="dstt"><thead><tr><th>最近访问</th><th>IP</th><th>访客标识</th><th>设备</th><th>访问次数</th><th>每日塔罗</th><th>抽牌</th><th>答案之书</th><th>星骰</th><th>首次</th><th>备注</th><th>操作</th></tr></thead><tbody>';
    it.forEach(function(r){
      var ua = r.ua || '';
      h += '<tr><td style="white-space:nowrap">' + (r.last_at || '') + '</td>'
        + '<td>' + dsEsc(r.ip) + '</td>'
        + '<td style="font-size:11px;color:#8b82ab">' + dsEsc((r.vid || '').slice(0, 12)) + '…</td>'
        + '<td style="max-width:260px;font-size:11.5px;color:#9c93bd" title="' + dsEsc(ua) + '">' + dsEsc(ua.slice(0, 46)) + '</td>'
        + '<td>' + (r.visits || 0) + '</td>'
        + '<td>' + (r.n_daily || 0) + '</td>'
        + '<td>' + (r.n_draw || 0) + '</td>'
        + '<td>' + (r.n_answer || 0) + '</td>'
        + '<td>' + (r.n_dice || 0) + '</td>'
        + '<td style="white-space:nowrap">' + (r.first_at || '') + '</td>'
        + '<td style="white-space:nowrap;color:#c8b6ff;cursor:pointer" data-vid="' + dsEsc(r.vid) + '" data-note="' + dsEsc(r.note || '') + '" onclick="vsNote(this.dataset.vid, this.dataset.note)">' + (r.note ? dsEsc(r.note) : '＋ 备注') + '</td>'
        + '<td style="white-space:nowrap"><button class="btn btn-small" data-vid="' + dsEsc(r.vid) + '" onclick="vsDel(this.dataset.vid)">清掉</button></td></tr>';
    });
    box.innerHTML = h + '</tbody></table>';
  }).catch(function(){ box.innerHTML = '<div class="hint">连不上服务</div>'; });
}

function vsNote(vid, cur){
  var v = window.prompt('给这个访客加个备注（比如「老客户」「小红书上来的」），清空则删除备注：', cur || '');
  if(v === null){ return; }
  api('/api/visitor_note', { vid: vid, note: v }).then(function(d){
    if(d && d.ok){ loadVisitors(); } else { alert('保存失败'); }
  }).catch(function(){ alert('连不上服务'); });
}

function vsDel(vid){
  if(!window.confirm('清掉这个访客和他所有行为记录？只删统计数据，不影响前台。')){ return; }
  api('/api/visitor_del', { vid: vid }).then(function(d){
    if(d && d.ok){ loadVisitors(); } else { alert('删除失败'); }
  }).catch(function(){ alert('连不上服务'); });
}

(function(){
  var b=document.getElementById('sBtn'), s=document.getElementById('side'), m=document.getElementById('sMask');
  if(b){ b.addEventListener('click', function(){
    s.classList.toggle('open');
    m.classList.toggle('on', s.classList.contains('open'));
  }); }
  if(m){ m.addEventListener('click', function(){ s.classList.remove('open'); m.classList.remove('on'); }); }
})();

function logout(){
  fetch('/api/logout',{method:'POST'})
    .then(function(){ location.href='/login'; })
    .catch(function(){ location.href='/login'; });
}

function api(path, data){
  return fetch(path, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)})
    .then(r=>r.json());
}

function showStatus(msg, isErr){
  const s = document.getElementById('status');
  s.style.display = 'block';
  s.textContent = msg;
  s.className = isErr ? 'status msg-err' : 'status';
}

// 输入客户名后检测老客户
function checkClient(){
  const name = document.getElementById('name').value.trim();
  if(!name){ document.getElementById('histBox').style.display='none'; return; }
  api('/api/check', {name}).then(res=>{
    const box = document.getElementById('histBox');
    if(res.is_old){
      box.style.display = 'block';
      box.innerHTML = '<b style="color:#f5d78e;">老客户 ' + name + '，第' + (res.count+1) + ' 次占卜</b><br>' + res.summary_html;
    } else {
      box.style.display = 'block';
      box.innerHTML = '新客户，首次占卜';
    }
  });
}

// 实时解析牌面关键词
document.getElementById('cards').addEventListener('input', function(){
  const txt = this.value.trim();
  if(!txt){ document.getElementById('chipBox').innerHTML=''; return; }
  api('/api/parse', {cards:txt}).then(res=>{
    document.getElementById('chipBox').innerHTML = res.cards.map(c=>
      '<span class="chip"><b>'+c.name+'</b> '+c.pos+' · '+c.kw+'</span>').join('');
  });
});

function genPrompt(){
  const name = document.getElementById('name').value.trim();
  const qtype = document.getElementById('qtype').value;
  const question = document.getElementById('question').value.trim();
  const spread = document.getElementById('spread').value.trim();
  const cards = document.getElementById('cards').value.trim();
  if(!name){ showStatus('请先填写客户称呼（必填，用于后续搜索）', true); return; }
  if(!question || !cards){ showStatus('请至少填写提问和牌面', true); return; }
  api('/api/prompt', {name, qtype, question, spread, cards}).then(res=>{
    if(res.error){ showStatus(res.error, true); return; }
    currentPrompt = res.prompt;
    currentName = name;
    document.getElementById('result').style.display = 'block';
    document.getElementById('result').textContent = res.prompt;
    document.getElementById('toolbar').style.display = 'flex';
    showStatus('提示词已生成，可直接复制粘贴给 AI');
  });
}

function copyPrompt(){
  navigator.clipboard.writeText(currentPrompt).then(()=>{
    showStatus('已复制到剪贴板');
  }).catch(()=>{
    const ta = document.createElement('textarea');
    ta.value = currentPrompt;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    showStatus('已复制到剪贴板');
  });
}

function saveCase(){
  const name = document.getElementById('name').value.trim();
  if(!name){ showStatus('客户称呼必填，用于后续搜索该客户', true); return; }
  const qtype = document.getElementById('qtype').value;
  const question = document.getElementById('question').value.trim();
  const spread = document.getElementById('spread').value.trim();
  const cards = document.getElementById('cards').value.trim();
  const reading = document.getElementById('reading').value.trim();
  api('/api/save', {name, qtype, question, spread, cards, reading}).then(res=>{
    if(res.ok){ showStatus('案例已保存，下次自动整合'); } else { showStatus(res.error||'保存失败', true); }
  });
}


function loadHistory(){
  const name = document.getElementById('hisName').value.trim();
  if(!name){ return; }
  api('/api/history', {name}).then(res=>{
    const box = document.getElementById('hisList');
    if(res.error){ box.innerHTML = '<div class="msg-err">'+res.error+'</div>'; return; }
    if(res.clients){
      box.innerHTML = '<div class="list-item">'+res.clients.map(c=>'<b>'+c.name+'</b>（'+c.count+' 条案例）').join('<br>')+'</div>';
      return;
    }
    box.innerHTML = res.cases.map(c=>
      '<div class="list-item"><b>['+c.date+']</b> '+c.q_type+' | 提问：'+c.question+'<br>牌面：'+c.cards+
      '<div class="field-row"><b>心得：</b><span id="rtext_'+c.id+'">'+(c.reading||'（未填写）')+'</span>'+
      ' <button class="btn btn-purple btn-small" onclick="startEdit('+c.id+',\\'reading\\')">编辑</button></div>'+
      '<div class="field-row"><b>反馈：</b><span id="ftext_'+c.id+'">'+(c.feedback||'（未填写）')+'</span>'+
      ' <button class="btn btn-purple btn-small" onclick="startEdit('+c.id+',\\'feedback\\')">编辑</button></div></div>').join('') ||
      '<div class="list-item">暂无记录</div>';
  });
}

function startEdit(id, field){
  const spanId = (field==='reading') ? 'rtext_'+id : 'ftext_'+id;
  const span = document.getElementById(spanId);
  if(!span){ return; }
  const cur = span.textContent === '（未填写）' ? '' : span.textContent;
  span.innerHTML = '<textarea id="editbox_'+id+'_'+field+'" style="width:100%;min-height:50px;margin:4px 0;">'+cur+'</textarea>'+
    '<br><button class="btn btn-purple btn-small" onclick="saveField('+id+',\\''+field+'\\')">保存</button> '+
    '<button class="btn btn-small" style="background:#5a2c3c;color:#f0a0a0;" onclick="loadHistory()">取消</button>';
}
function saveField(id, field){
  const box = document.getElementById('editbox_'+id+'_'+field);
  if(!box){ return; }
  const val = box.value.trim();
  api('/api/update_field', {id, field, value:val}).then(res=>{
    if(res.ok){ alert((field==='reading'?'心得':'反馈')+'已保存'); loadHistory(); }
    else { alert(res.error||'失败'); }
  });
}

// ==================== 图文生成器 ====================
const ALL_CARDS = /*__CARDS__*/[];
let IG = { groups: [], singles: [], cover: 1, coverFile: "", all: [], fileMap: {}, last: null };
let IG_READY = false;
const IG_CN = ["一","二","三","四","五","六","七","八","九","十"];
const IG_MAX = 10;

function igEsc(s){
  return String(s==null?"":s)
    .replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}

function igCn(i){
  return IG_CN[i] || String(i+1);
}

function igStatus(msg, isErr){
  ["igStatus","igsStatus"].forEach(function(id){
    const s = document.getElementById(id);
    if(!s){ return; }
    s.style.display = "block";
    s.textContent = msg;
    s.className = isErr ? "status msg-err" : "status";
  });
}

/* ===== 每组单图独立页：组数据概览 ===== */
function igSingleRefresh(autoDraw){
}

function igInit(){
  if(IG_READY){ return; }
  IG_READY = true;
  let h = "";
  for(let i=1;i<=3;i++){
    h += '<div class="thumb'+(i===1?' on':'')+'" data-c="'+i+'" onclick="igPickCover('+i+')">'
       + '<img src="/assets/cover_'+i+'.png" alt="封面'+i+'">'
       + '<span>封面'+i+'</span></div>';
  }
  document.getElementById("igCovers").innerHTML = h;
  igDrawAll();
}

function igSyncCoverPick(){
  const ths = document.querySelectorAll("#igCovers .thumb");
  for(let k=0;k<ths.length;k++){
    const on = !IG.coverFile && Number(ths[k].getAttribute("data-c"))===IG.cover;
    ths[k].classList.toggle("on", on);
  }
}

function igPickCover(i){
  IG.cover = i;
  IG.coverFile = "";
  igSyncCoverPick();
  document.getElementById("igCoverTip").textContent = "当前使用：内置底图 " + i;
}

function igPickUploadCover(){
  const f = document.getElementById("igCoverFile");
  f.value = "";
  f.click();
}

function igDoUploadCover(inp){
  const f = inp.files && inp.files[0];
  if(!f){ return; }
  if(String(f.type||"").indexOf("image/") !== 0){ igStatus("请选择图片文件", true); return; }
  const reader = new FileReader();
  reader.onload = function(){
    igStatus("正在上传总封面…");
    api("/api/ig_upload", {kind:"cover", data:String(reader.result)}).then(function(res){
      if(res.error){ igStatus(res.error, true); return; }
      IG.coverFile = res.file;
      igSyncCoverPick();
      document.getElementById("igCoverTip").textContent =
        "当前使用：上传封面 " + res.file + "（" + res.width + "×" + res.height + "）";
      igStatus("总封面已上传，可直接生成长图");
    }).catch(function(e){ igStatus("上传失败：" + e, true); });
  };
  reader.readAsDataURL(f);
}

function igResetCover(){
  IG.coverFile = "";
  IG.cover = 1;
  igSyncCoverPick();
  document.getElementById("igCoverTip").textContent = "当前使用：内置底图 1";
}

function igBuildMap(all){
  IG.all = all || [];
  IG.fileMap = {};
  for(let i=0;i<IG.all.length;i++){ IG.fileMap[IG.all[i].name] = IG.all[i].file; }
}

function igRequestDraw(n, olds){
  igStatus("正在抽牌…");
  api("/api/ig_draw", {groups:n}).then(function(res){
    if(res.error){ igStatus(res.error, true); return; }
    igBuildMap(res.all);
    const old = olds || [];
    IG.groups = res.groups.map(function(g,i){
      const o = old[i] || {};
      return {
        label: o.label || g.label,
        text: o.text || "",
        analysis: o.analysis || o.text || "",
        advice: o.advice || "",
        subcover: o.subcover || "",
        cards: g.cards
      };
    });
    igRenderGroups();
    igSingleRefresh();
    igStatus("已抽牌：" + IG.groups.length + " 组，共 " + (IG.groups.length*3) + " 张");
  }).catch(function(e){ igStatus("抽牌失败：" + e, true); });
}

function igDrawAll(){
  igRequestDraw(IG.groups.length || 3, IG.groups);
}

function igNewCards(count){
  const used = {};
  for(let i=0;i<IG.groups.length;i++){
    for(let k=0;k<IG.groups[i].cards.length;k++){
      used[IG.groups[i].cards[k].name] = 1;
    }
  }
  const pool = ALL_CARDS.filter(function(n){ return !used[n]; });
  for(let k=pool.length-1;k>0;k--){
    const j = Math.floor(Math.random()*(k+1));
    const t = pool[k]; pool[k] = pool[j]; pool[j] = t;
  }
  const out = [];
  for(let k=0;k<count && k<pool.length;k++){
    out.push({name:pool[k], pos:(Math.random()<0.5?"逆":"正"), file: IG.fileMap[pool[k]]||""});
  }
  return out;
}

function igAddGroup(){
  if(IG.groups.length >= IG_MAX){ igStatus("最多 " + IG_MAX + " 组", true); return; }
  const gi = IG.groups.length;
  IG.groups.push({label:"第"+igCn(gi)+"组", text:"", analysis:"", advice:"", subcover:"", cards: igNewCards(3)});
  igRenderGroups();
  igStatus("已添加第" + igCn(gi) + "组，共 " + IG.groups.length + " 组");
}

function igDelGroup(gi){
  if(IG.groups.length <= 1){ igStatus("至少保留 1 组", true); return; }
  IG.groups.splice(gi, 1);
  for(let i=0;i<IG.groups.length;i++){
    const lb = String(IG.groups[i].label||"");
    if(!lb || /^第[一二三四五六七八九十]+组$/.test(lb)){
      IG.groups[i].label = "第" + igCn(i) + "组";
    }
  }
  igRenderGroups();
  igStatus("已删除一组，剩余 " + IG.groups.length + " 组");
}

function igPickSubCover(gi){
  const f = document.getElementById("igSubFile_"+gi);
  if(!f){ return; }
  f.value = "";
  f.click();
}

function igDoUploadSubCover(gi, inp){
  const f = inp.files && inp.files[0];
  if(!f){ return; }
  if(String(f.type||"").indexOf("image/") !== 0){ igStatus("请选择图片文件", true); return; }
  const reader = new FileReader();
  reader.onload = function(){
    igStatus("正在上传第" + igCn(gi) + "组子封面…");
    api("/api/ig_upload", {kind:"subcover", data:String(reader.result)}).then(function(res){
      if(res.error){ igStatus(res.error, true); return; }
      IG.groups[gi].subcover = res.file;
      igRenderGroups();
      igStatus("第" + igCn(gi) + "组子封面已上传（" + res.width + "×" + res.height + "）");
    }).catch(function(e){ igStatus("上传失败：" + e, true); });
  };
  reader.readAsDataURL(f);
}

function igClearSubCover(gi){
  IG.groups[gi].subcover = "";
  igRenderGroups();
  igStatus("已移除第" + igCn(gi) + "组子封面");
}

function igOptions(sel){
  let h = "";
  for(let i=0;i<ALL_CARDS.length;i++){
    const n = ALL_CARDS[i];
    h += '<option value="'+n+'"'+(n===sel?' selected':'')+'>'+n+'</option>';
  }
  return h;
}

function igSubCoverRow(gi, g){
  let thumb = '<i>未上传 · 该位置不占空</i>';
  if(g.subcover){
    thumb = '<img src="/assets/uploads/'+encodeURIComponent(g.subcover)+'" alt="子封面">';
  }
  return '<div class="sub-cover">'
    + '<div class="sc-thumb">'+thumb+'</div>'
    + '<div class="sc-ops">'
    + '<button class="btn btn-purple btn-small" onclick="igPickSubCover('+gi+')">上传子封面</button>'
    + '<button class="btn btn-small" onclick="igClearSubCover('+gi+')">移除子封面</button>'
    + '</div>'
    + '<input type="file" id="igSubFile_'+gi+'" accept="image/*" style="display:none;" onchange="igDoUploadSubCover('+gi+',this)">'
    + '</div>';
}

function igRenderGroups(){
  const box = document.getElementById("igGroupsBox");
  let h = "";
  for(let gi=0; gi<IG.groups.length; gi++){
    const g = IG.groups[gi];
    let slots = "";
    for(let ci=0; ci<g.cards.length; ci++){
      const c = g.cards[ci];
      const rot = (c.pos==="逆") ? ' style="transform:rotate(180deg);"' : '';
      slots += '<div class="slot">'
        + '<img src="/cards/'+encodeURIComponent(c.file)+'"'+rot+' alt="'+igEsc(c.name)+'" title="点击放大" onclick="igZoom(this.src)">'
        + '<select onchange="igSetCard('+gi+','+ci+',this.value)">'+igOptions(c.name)+'</select>'
        + '<select onchange="igSetPos('+gi+','+ci+',this.value)">'
        + '<option value="正"'+(c.pos==="正"?" selected":"")+'>正位</option>'
        + '<option value="逆"'+(c.pos==="逆"?" selected":"")+'>逆位</option>'
        + '</select></div>';
    }
    h += '<div class="grp">'
      + '<div class="grp-head">'
      + '<input type="text" style="flex:1;padding:8px 10px;" value="'+igEsc(g.label)+'" oninput="igSetLabel('+gi+',this.value)">'
      + '<button class="btn btn-purple btn-small" onclick="igReroll('+gi+')">本组重抽</button>'
      + '<button class="btn btn-small" style="background:#5a2c3c;color:#f0a0a0;" onclick="igDelGroup('+gi+')">删除该组</button></div>'
      + '<div class="slots">'+slots+'</div>'
      + igSubCoverRow(gi, g)
      + '<label>第'+igCn(gi)+'组 · 牌面解析（单图版白区上半段）</label>'
      + '<textarea id="igAn_'+gi+'" placeholder="粘贴该组的牌面解析文字" oninput="igSetAnalysis('+gi+',this.value)">'+igEsc(g.analysis||"")+'</textarea>'
      + '<label>第'+igCn(gi)+'组 · 给你的建议（单图版白区下半段）</label>'
      + '<textarea id="igAd_'+gi+'" placeholder="粘贴该组的建议 / 行动指引" oninput="igSetAdvice('+gi+',this.value)">'+igEsc(g.advice||"")+'</textarea>'
      + '<label>第'+igCn(gi)+'组解读文案（长图版用，留空则由上面两段自动拼接）</label>'
      + '<textarea id="igText_'+gi+'" placeholder="粘贴 AI 生成的解读文字，将原样排入长图" oninput="igSetText('+gi+',this.value)">'+igEsc(g.text)+'</textarea>'
      + '</div>';
  }
  box.innerHTML = h;
  const gc = document.getElementById("igGroupCount");
  if(gc){ gc.textContent = "当前 " + IG.groups.length + " 组（上限 " + IG_MAX + " 组）"; }
}

function igSetCard(gi, ci, name){
  IG.groups[gi].cards[ci].name = name;
  IG.groups[gi].cards[ci].file = IG.fileMap[name] || "";
  igRenderGroups();
}

function igSetPos(gi, ci, pos){
  IG.groups[gi].cards[ci].pos = pos;
  igRenderGroups();
}

function igSetLabel(gi, v){ IG.groups[gi].label = v; }
function igSetText(gi, v){ IG.groups[gi].text = v; }
function igSetAnalysis(gi, v){ IG.groups[gi].analysis = v; }
function igSetAdvice(gi, v){ IG.groups[gi].advice = v; }

function igReroll(gi){
  const used = {};
  for(let i=0;i<IG.groups.length;i++){
    if(i===gi){ continue; }
    for(let k=0;k<IG.groups[i].cards.length;k++){ used[IG.groups[i].cards[k].name] = 1; }
  }
  const pool = ALL_CARDS.filter(n=>!used[n]);
  for(let k=pool.length-1;k>0;k--){
    const j = Math.floor(Math.random()*(k+1));
    const t = pool[k]; pool[k] = pool[j]; pool[j] = t;
  }
  for(let k=0;k<3 && k<pool.length;k++){
    IG.groups[gi].cards[k] = {
      name: pool[k],
      pos: (Math.random() < 0.5 ? "逆" : "正"),
      file: IG.fileMap[pool[k]] || ""
    };
  }
  igRenderGroups();
}

function igBuildList(){
  const d = new Date();
  const p2 = v => (v<10?"0":"")+v;
  const ds = d.getFullYear()+"-"+p2(d.getMonth()+1)+"-"+p2(d.getDate());
  const NL = String.fromCharCode(10);
  const lines = ["【本次抽牌】"+ds, ""];
  for(let gi=0; gi<IG.groups.length; gi++){
    const g = IG.groups[gi];
    const arr = [];
    for(let ci=0;ci<g.cards.length;ci++){
      arr.push(g.cards[ci].name + " " + (g.cards[ci].pos==="逆" ? "逆位" : "正位"));
    }
    lines.push("第"+igCn(gi)+"组"+(g.label?"（"+g.label+"）":"")+"："+arr.join(" / "));
  }
  lines.push("");
  lines.push("请按上面" + IG.groups.length + "组牌分别写解读文案，每组 200-300 字，语气温柔贴近生活，结尾给一句行动建议。");
  return lines.join(NL);
}

function igCopyList(){
  const txt = igBuildList();
  const done = ()=>igStatus("抽牌结果清单已复制，可直接粘贴给 AI 生成文案");
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(txt).then(done).catch(()=>igFallbackCopy(txt, done));
  } else {
    igFallbackCopy(txt, done);
  }
}

function igFallbackCopy(txt, done){
  const ta = document.createElement("textarea");
  ta.value = txt;
  ta.style.position = "fixed";
  ta.style.left = "-9999px";
  document.body.appendChild(ta);
  ta.select();
  try { document.execCommand("copy"); done(); }
  catch(e) { igStatus("复制失败，请手动复制结果清单", true); }
  document.body.removeChild(ta);
}

function igPayload(){
  return {
    cover: IG.cover,
    cover_file: IG.coverFile || "",
    title: document.getElementById("igTitle").value,
    subtitle: document.getElementById("igSub").value,
    guide: document.getElementById("igGuide").value,
    footer: document.getElementById("igFooter").value,
    author: document.getElementById("igAuthor").value,
    avatar_file: IG.avatar || "",
    lead: document.getElementById("igLead").value,
    disclaimer: document.getElementById("igDisclaimer").value,
    groups: IG.groups.map(function(g){
      return {
        label: g.label,
        text: g.text || "",
        analysis: g.analysis || "",
        advice: g.advice || "",
        subcover: g.subcover || "",
        cards: g.cards.map(function(c){ return {name:c.name, pos:c.pos}; })
      };
    })
  };
}

function igSimpleStatus(msg, isErr){
  var el = document.getElementById("igsStatus");
  if(!el){ return; }
  el.textContent = msg || "";
  el.style.color = isErr ? "#ff6b6b" : "";
}
function igGenerateGroup(){
  const payload = igsPayload();
  igSimpleStatus("正在合并每组单图，请稍候…");
  api("/api/ig_generate_group", payload).then(function(res){
    if(res.error){ igSimpleStatus(res.error, true); return; }
    IGS.singles = res.images || [];
    igRenderSingles();
    igSimpleStatus("已生成 " + IGS.singles.length + " 张单图，保存于 output/groupimage/");
  }).catch(function(e){ igSimpleStatus("生成失败：" + e, true); });
}

var IG_ICO_EYE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7z"></path><circle cx="12" cy="12" r="3"></circle></svg>';
var IG_ICO_DL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"></path><path d="M7 11l5 5 5-5"></path><path d="M4 20h16"></path></svg>';

function igZoom(url){
  var d = document.createElement("div");
  d.style.cssText = "position:fixed;left:0;top:0;right:0;bottom:0;z-index:9999;background:rgba(6,6,12,.93);display:flex;align-items:center;justify-content:center;padding:20px;cursor:zoom-out;";
  var im = document.createElement("img");
  im.src = url;
  im.style.cssText = "max-width:100%;max-height:100%;border-radius:12px;box-shadow:0 0 48px rgba(0,0,0,.7);";
  d.appendChild(im);
  d.onclick = function(){ if(d.parentNode){ d.parentNode.removeChild(d); } };
  document.body.appendChild(d);
}

/* 悬浮图标：预览 / 下载 */
function igZoomAt(i){
  var s = (IGS.singles || [])[i];
  if(s && s.url){ igZoom(s.url); }
}
function igDownload(url, name){
  if(!url){ return; }
  var a = document.createElement("a");
  a.href = url;
  if(name){ a.download = name; }
  a.style.display = "none";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}
function igDownloadAt(i){
  var s = (IGS.singles || [])[i];
  if(s){ igDownload(s.url, s.filename); }
}
function igZoomLong(){
  var im = document.getElementById("igsPreviewImg");
  if(im && im.getAttribute("src")){ igZoom(im.getAttribute("src")); }
}
function igDownloadLong(){
  var im = document.getElementById("igsPreviewImg");
  var a = document.getElementById("igsDownload");
  var url = (a && a.getAttribute("href")) || (im && im.getAttribute("src"));
  if(!url || url === "#"){ return; }
  igDownload(url, (a && a.getAttribute("download")) || "");
}

function igRenderSingles(){
  const arr = IGS.singles || [];
  const box = document.getElementById("igSingleList");
  let h = "";
  for(let i=0;i<arr.length;i++){
    const s = arr[i];
    h += '<div class="seg-item"><b>' + igEsc(s.title) + '</b>'
      + '<span class="rg">' + s.width + '×' + s.height + '</span>'
      + '<div class="ig-thumb">'
      + '<img src="' + s.url + '" alt="' + igEsc(s.title) + '">'
      + '<div class="ig-acts">'
      + '<button type="button" class="ig-act" title="预览" onclick="igZoomAt(' + i + ')">' + IG_ICO_EYE + '</button>'
      + '<button type="button" class="ig-act" title="下载" onclick="igDownloadAt(' + i + ')">' + IG_ICO_DL + '</button>'
      + '</div></div>'
      + '<span class="rg">' + igEsc(s.filename) + '</span></div>';
  }
  box.innerHTML = h;
  document.getElementById("igSingleBox").style.display = arr.length ? "block" : "none";
  if(arr.length){
    document.getElementById("igSinglePath").textContent = "共 " + arr.length + " 张，文件目录：output/groupimage/";
  }
}

/* ===== 每组单图页：独立状态 + 独立长图出图（与「抽牌出图」长图页完全剥离） ===== */
var IGS = { singles: [], long: null, groups: [], all: [], fileMap: {}, avatar: "" };

/* ---- 单图页独立抽牌 + 牌面文案编辑（数据只存在 IGS.groups，不碰 IG.groups） ---- */
function igsLoadMap(){
  if(IGS.all && IGS.all.length){ return Promise.resolve(); }
  return api("/api/ig_draw", {groups:1}).then(function(res){
    IGS.all = res.all || [];
    IGS.fileMap = {};
    for(var i=0;i<IGS.all.length;i++){ IGS.fileMap[IGS.all[i].name] = IGS.all[i].file; }
  });
}
function igsDraw(){
  var el = document.getElementById("igsDrawCount");
  var n = el ? parseInt(el.value, 10) : 3;
  if(isNaN(n) || n < 1){ n = 3; }
  if(n > IG_MAX){ n = IG_MAX; }
  igSimpleStatus("正在抽牌…");
  api("/api/ig_draw", {groups:n}).then(function(res){
    if(res.error){ igSimpleStatus(res.error, true); return; }
    IGS.all = res.all || [];
    IGS.fileMap = {};
    for(var i=0;i<IGS.all.length;i++){ IGS.fileMap[IGS.all[i].name] = IGS.all[i].file; }
    var old = IGS.groups || [];
    IGS.groups = (res.groups || []).map(function(g, k){
      var o = old[k] || {};
      return {
        label: o.label || g.label,
        text: o.text || "",
        analysis: o.analysis || "",
        advice: o.advice || "",
        subcover: o.subcover || "",
        cards: g.cards
      };
    });
    IGS.singles = [];
    IGS.long = null;
    igsRenderGroups();
    igSimpleStatus("已抽牌：" + IGS.groups.length + " 组，共 " + (IGS.groups.length*3) + " 张");
  }).catch(function(e){ igSimpleStatus("抽牌失败：" + e, true); });
}
function igsInit(){
  if(IGS.groups && IGS.groups.length){ igsRenderGroups(); return; }
  igsDraw();
}
function igsResetGroups(){
  IGS.groups = [];
  igsDraw();
}
function igsNewCards(count){
  var used = {};
  for(var i=0;i<IGS.groups.length;i++){
    for(var k=0;k<IGS.groups[i].cards.length;k++){ used[IGS.groups[i].cards[k].name] = 1; }
  }
  var pool = ALL_CARDS.filter(function(n){ return !used[n]; });
  for(var j=pool.length-1;j>0;j--){
    var r = Math.floor(Math.random()*(j+1));
    var t = pool[j]; pool[j] = pool[r]; pool[r] = t;
  }
  var out = [];
  for(var m=0; m<count && m<pool.length; m++){
    out.push({name: pool[m], pos: (Math.random() < 0.5 ? "逆" : "正"), file: IGS.fileMap[pool[m]] || ""});
  }
  return out;
}
function igsAddGroup(){
  if(IGS.groups.length >= IG_MAX){ igSimpleStatus("最多 " + IG_MAX + " 组", true); return; }
  var go = function(){
    var gi = IGS.groups.length;
    IGS.groups.push({label:"第"+igCn(gi)+"组", text:"", analysis:"", advice:"", subcover:"", cards: igsNewCards(3)});
    igsRenderGroups();
    igSimpleStatus("已添加第" + igCn(gi) + "组，共 " + IGS.groups.length + " 组");
  };
  if(!(IGS.all && IGS.all.length)){
    igsLoadMap().then(go).catch(function(e){ igSimpleStatus("牌池加载失败：" + e, true); });
  } else { go(); }
}
function igsDelGroup(gi){
  if(IGS.groups.length <= 1){ igSimpleStatus("至少保留 1 组", true); return; }
  IGS.groups.splice(gi, 1);
  for(var i=0;i<IGS.groups.length;i++){
    var lb = String(IGS.groups[i].label || "");
    if(!lb || /^第[一二三四五六七八九十]+组$/.test(lb)){ IGS.groups[i].label = "第" + igCn(i) + "组"; }
  }
  igsRenderGroups();
  igSimpleStatus("已删除一组，剩余 " + IGS.groups.length + " 组");
}
function igsReroll(gi){
  var used = {};
  for(var i=0;i<IGS.groups.length;i++){
    if(i === gi){ continue; }
    for(var k=0;k<IGS.groups[i].cards.length;k++){ used[IGS.groups[i].cards[k].name] = 1; }
  }
  var pool = ALL_CARDS.filter(function(n){ return !used[n]; });
  for(var j=pool.length-1;j>0;j--){
    var r = Math.floor(Math.random()*(j+1));
    var t = pool[j]; pool[j] = pool[r]; pool[r] = t;
  }
  for(var m=0; m<3 && m<pool.length; m++){
    IGS.groups[gi].cards[m] = {name: pool[m], pos: (Math.random()<0.5?"逆":"正"), file: IGS.fileMap[pool[m]] || ""};
  }
  igsRenderGroups();
  igSimpleStatus("第" + igCn(gi) + "组已重抽");
}
function igsSetCard(gi, ci, name){
  IGS.groups[gi].cards[ci].name = name;
  IGS.groups[gi].cards[ci].file = IGS.fileMap[name] || "";
  igsRenderGroups();
}
function igsSetPos(gi, ci, pos){ IGS.groups[gi].cards[ci].pos = pos; igsRenderGroups(); }
function igsSetLabel(gi, v){ IGS.groups[gi].label = v; }
function igsSetAnalysis(gi, v){ IGS.groups[gi].analysis = v; }
function igsSetAdvice(gi, v){ IGS.groups[gi].advice = v; }
function igsPickSubCover(gi){
  var f = document.getElementById("igsSubFile_" + gi);
  if(!f){ return; }
  f.value = "";
  f.click();
}
function igsDoUploadSubCover(gi, inp){
  var f = inp.files && inp.files[0];
  if(!f){ return; }
  if(String(f.type||"").indexOf("image/") !== 0){ igSimpleStatus("请选择图片文件", true); return; }
  var reader = new FileReader();
  reader.onload = function(){
    igSimpleStatus("正在上传第" + igCn(gi) + "组子封面…");
    api("/api/ig_upload", {kind:"subcover", data:String(reader.result)}).then(function(res){
      if(res.error){ igSimpleStatus(res.error, true); return; }
      IGS.groups[gi].subcover = res.file;
      igsRenderGroups();
      igSimpleStatus("第" + igCn(gi) + "组子封面已上传（" + res.width + "×" + res.height + "）");
    }).catch(function(e){ igSimpleStatus("上传失败：" + e, true); });
  };
  reader.readAsDataURL(f);
}
function igsClearSubCover(gi){
  IGS.groups[gi].subcover = "";
  igsRenderGroups();
  igSimpleStatus("第" + igCn(gi) + "组子封面已移除");
}
function igsSubCoverRow(gi, g){
  var thumb = "<i>未上传 · 该位置不占空</i>";
  if(g.subcover){
    thumb = '<img src="/assets/uploads/' + encodeURIComponent(g.subcover) + '" alt="子封面">';
  }
  return '<div class="sub-cover">'
    + '<div class="sc-thumb">' + thumb + '</div>'
    + '<div class="sc-ops">'
    + '<button class="btn btn-purple btn-small" onclick="igsPickSubCover(' + gi + ')">上传子封面</button>'
    + '<button class="btn btn-small" onclick="igsClearSubCover(' + gi + ')">移除子封面</button>'
    + '</div>'
    + '<input type="file" id="igsSubFile_' + gi + '" accept="image/*" style="display:none;" onchange="igsDoUploadSubCover(' + gi + ',this)">'
    + '</div>';
}
function igsRenderGroups(){
  var box = document.getElementById("igsEditBox");
  if(!box){ return; }
  var h = "";
  for(var gi=0; gi<IGS.groups.length; gi++){
    var g = IGS.groups[gi];
    var slots = "";
    for(var ci=0; ci<g.cards.length; ci++){
      var c = g.cards[ci];
      var rot = (c.pos === "逆") ? ' style="transform:rotate(180deg);"' : '';
      slots += '<div class="slot">'
        + '<img src="/cards/' + encodeURIComponent(c.file || "") + '"' + rot + ' alt="' + igEsc(c.name) + '" title="点击放大" onclick="igZoom(this.src)">'
        + '<select onchange="igsSetCard(' + gi + ',' + ci + ',this.value)">' + igOptions(c.name) + '</select>'
        + '<select onchange="igsSetPos(' + gi + ',' + ci + ',this.value)">'
        + '<option value="正"' + (c.pos === "正" ? " selected" : "") + '>正位</option>'
        + '<option value="逆"' + (c.pos === "逆" ? " selected" : "") + '>逆位</option>'
        + '</select></div>';
    }
    h += '<div class="grp">'
      + '<div class="grp-head">'
      + '<input type="text" style="flex:1;padding:8px 10px;" value="' + igEsc(g.label) + '" oninput="igsSetLabel(' + gi + ',this.value)">'
      + '<button class="btn btn-purple btn-small" onclick="igsReroll(' + gi + ')">本组重抽</button>'
      + '<button class="btn btn-small" style="background:#5a2c3c;color:#f0a0a0;" onclick="igsDelGroup(' + gi + ')">删除该组</button></div>'
      + '<div class="slots">' + slots + '</div>'
      + igsSubCoverRow(gi, g)
      + '<label>第' + igCn(gi) + '组 · 牌面解析（单图版白区上半段）</label>'
      + '<textarea id="igsAn_' + gi + '" placeholder="粘贴该组的牌面解析文字" oninput="igsSetAnalysis(' + gi + ',this.value)">' + igEsc(g.analysis || "") + '</textarea>'
      + '<label>第' + igCn(gi) + '组 · 给你的建议（单图版白区下半段）</label>'
      + '<textarea id="igsAd_' + gi + '" placeholder="粘贴该组的建议 / 行动指引" oninput="igsSetAdvice(' + gi + ',this.value)">' + igEsc(g.advice || "") + '</textarea>'
      + '</div>';
  }
  box.innerHTML = h;
  var gc = document.getElementById("igsGroupCount");
  if(gc){ gc.textContent = "当前 " + IGS.groups.length + " 组（上限 " + IG_MAX + " 组）"; }
}
function igsPayload(){
  var gAuthor = document.getElementById("igAuthor");
  var gLead = document.getElementById("igLead");
  var gDis = document.getElementById("igDisclaimer");
  return {
    cover: IG.cover,
    cover_file: "",
    title: "",
    subtitle: "",
    guide: "",
    footer: "",
    author: gAuthor ? gAuthor.value : "",
    avatar_file: IGS.avatar || IG.avatar || "",
    lead: gLead ? gLead.value : "",
    disclaimer: gDis ? gDis.value : "",
    groups: IGS.groups.map(function(g){
      return {
        label: g.label,
        text: g.text || "",
        analysis: g.analysis || "",
        advice: g.advice || "",
        subcover: g.subcover || "",
        cards: g.cards.map(function(c){ return {name: c.name, pos: c.pos}; })
      };
    })
  };
}

function igsLongStatus(msg, isErr){
  var el = document.getElementById("igsLongStatus");
  if(!el){ return; }
  el.textContent = msg || "";
  el.style.color = isErr ? "#ff6b6b" : "";
}
function igsGap(){
  var el = document.getElementById("igsGap");
  var g = el ? parseInt(el.value, 10) : 0;
  if(isNaN(g)){ g = 0; }
  return Math.max(0, Math.min(120, g));
}
function igsGenerateLong(exportAll){
  var payload = igsPayload();
  payload.export_segments = !!exportAll;
  payload.gap = igsGap();
  igsLongStatus(exportAll ? "正在生成单图版长图并分段导出…" : "正在生成单图版长图…");
  api("/api/igs_generate_long", payload).then(function(res){
    if(res.error){ igsLongStatus(res.error, true); return; }
    IGS.long = res;
    document.getElementById("igsPreview").style.display = "block";
    document.getElementById("igsPreviewImg").src = res.url + "?t=" + Date.now();
    var dl = document.getElementById("igsDownload");
    dl.href = res.url;
    dl.setAttribute("download", res.filename);
    document.getElementById("igsLongPath").textContent =
      "已保存：" + res.path + "（" + res.width + "×" + res.height + "，" + res.count + " 组）";
    igsRenderSegs();
    igsLongStatus("单图版长图已生成，可下载整张或按组分段下载");
    if(exportAll){ igsDownloadAllSegs(); }
  }).catch(function(e){ igsLongStatus("生成失败：" + e, true); });
}
function igsRenderSegs(){
  var box = document.getElementById("igsSegList");
  var segs = (IGS.long && IGS.long.segments) || [];
  var h = "";
  for(var i=0;i<segs.length;i++){
    var s = segs[i];
    h += '<div class="seg-item"><b>' + igEsc(s.title) + '</b>';
    h += '<span class="rg">y ' + s.y0 + ' ~ ' + s.y1 + '（' + (s.y1-s.y0) + 'px）</span><br>';
    if(s.url){
      h += '<a href="' + s.url + '" download="' + igEsc(s.filename||"") + '">下载 ' + igEsc(s.filename||"") + '</a>';
    } else {
      h += '<button class="btn btn-purple btn-small" onclick="igsExportSeg(' + i + ')">导出该段</button>';
    }
    h += '</div>';
  }
  box.innerHTML = h;
  document.getElementById("igsSegBox").style.display = segs.length ? "block" : "none";
}
function igsExportSeg(i){
  var segs = (IGS.long && IGS.long.segments) || [];
  var s = segs[i];
  if(!s){ return; }
  if(s.url){ window.open(s.url, "_blank"); return; }
  api("/api/igs_crop", {filename: IGS.long.filename, y0:s.y0, y1:s.y1}).then(function(res){
    if(res.error){ igsLongStatus(res.error, true); return; }
    s.url = res.url; s.filename = res.filename;
    igsRenderSegs();
    igsLongStatus("已导出：" + res.filename);
  }).catch(function(e){ igsLongStatus("导出失败：" + e, true); });
}
function igsExportAll(){
  var segs = (IGS.long && IGS.long.segments) || [];
  if(!segs.length){ igsLongStatus("请先生成单图版长图", true); return; }
  var k = 0;
  (function step(){
    if(k >= segs.length){ igsLongStatus("全部分段已就绪，可逐个下载"); return; }
    var s = segs[k];
    if(s.url){ k++; step(); return; }
    api("/api/igs_crop", {filename: IGS.long.filename, y0:s.y0, y1:s.y1}).then(function(res){
      if(res.url){ s.url = res.url; s.filename = res.filename; }
      igsRenderSegs();
      k++;
      setTimeout(step, 120);
    }).catch(function(){ k++; setTimeout(step, 120); });
  })();
}
function igsDownloadAllSegs(){
  var segs = (IGS.long && IGS.long.segments) || [];
  if(!segs.length){ igsLongStatus("请先生成单图版长图", true); return; }
  var i = 0;
  (function step(){
    if(i >= segs.length){ igsLongStatus("已提交 " + segs.length + " 个分段下载"); return; }
    var s = segs[i];
    if(!s.url){
      api("/api/igs_crop", {filename: IGS.long.filename, y0:s.y0, y1:s.y1}).then(function(res){
        if(res.url){ s.url = res.url; s.filename = res.filename; }
        igsRenderSegs();
        i++;
        setTimeout(step, 200);
      }).catch(function(){ i++; setTimeout(step, 200); });
      return;
    }
    var a = document.createElement("a");
    a.href = s.url;
    a.download = s.filename || "";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    i++;
    setTimeout(step, 500);
  })();
}

function igDownloadSingles(){
  const arr = IGS.singles || [];
  if(!arr.length){ return; }
  let i = 0;
  (function step(){
    if(i >= arr.length){ igSimpleStatus("已提交 " + arr.length + " 张下载"); return; }
    const a = document.createElement("a");
    a.href = arr[i].url;
    a.download = arr[i].filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    i++;
    setTimeout(step, 600);
  })();
}

function igPickAvatar(){
  const f = document.getElementById("igAvatarFile");
  if(!f){ return; }
  f.value = "";
  f.click();
}

function igDoUploadAvatar(inp){
  const f = inp.files && inp.files[0];
  if(!f){ return; }
  const reader = new FileReader();
  reader.onload = function(){
    igStatus("正在上传头像…");
    api("/api/ig_upload", {kind:"avatar", data:String(reader.result)}).then(function(res){
      if(res.error){ igStatus(res.error, true); return; }
      IG.avatar = res.file;
      document.getElementById("igAvatarTip").textContent = "已上传：" + res.file + "（" + res.width + "×" + res.height + "）";
      igStatus("头像已上传，生成单图时会显示在组标签右侧");
    }).catch(function(e){ igStatus("上传失败：" + e, true); });
  };
  reader.readAsDataURL(f);
}

function igClearAvatar(){
  IG.avatar = "";
  document.getElementById("igAvatarTip").textContent = "未上传";
}

function igGenerate(exportAll){
  const payload = igPayload();
  payload.export_segments = !!exportAll;
  igStatus("正在合成 750px 长图，请稍候…");
  api("/api/ig_generate", payload).then(function(res){
    if(res.error){ igStatus(res.error, true); return; }
    IG.last = res;
    document.getElementById("igPreview").style.display = "block";
    document.getElementById("igPreviewImg").src = res.url + "?t=" + Date.now();
    const dl = document.getElementById("igDownload");
    dl.href = res.url;
    dl.setAttribute("download", res.filename);
    document.getElementById("igPath").textContent =
      "已保存：" + res.path + "（" + res.width + "×" + res.height + "）";
    igRenderSegs();
    igStatus("长图已生成，可预览或分段导出");
    if(exportAll){ igExportAll(true); }
  }).catch(function(e){ igStatus("生成失败：" + e, true); });
}

function igRenderSegs(){
  const box = document.getElementById("igSegList");
  const segs = (IG.last && IG.last.segments) || [];
  let h = "";
  for(let i=0;i<segs.length;i++){
    const s = segs[i];
    h += '<div class="seg-item"><b>' + igEsc(s.title) + '</b>';
    h += '<span class="rg">y ' + s.y0 + ' ~ ' + s.y1 + '（' + (s.y1-s.y0) + 'px）</span><br>';
    if(s.url){
      h += '<a href="' + s.url + '" download="' + igEsc(s.filename||"") + '">下载 ' + igEsc(s.filename||"") + '</a>';
    } else {
      h += '<button class="btn btn-purple btn-small" onclick="igExportSeg(' + i + ')">导出该段</button>';
    }
    h += '</div>';
  }
  box.innerHTML = h;
  document.getElementById("igSegBox").style.display = segs.length ? "block" : "none";
}

function igExportSeg(i){
  const segs = (IG.last && IG.last.segments) || [];
  const s = segs[i];
  if(!s){ return; }
  if(s.url){ window.open(s.url, "_blank"); return; }
  api("/api/ig_crop", {filename: IG.last.filename, y0:s.y0, y1:s.y1}).then(function(res){
    if(res.error){ igStatus(res.error, true); return; }
    s.url = res.url; s.filename = res.filename;
    igRenderSegs();
    igStatus("已导出：" + res.filename);
  }).catch(function(e){ igStatus("导出失败：" + e, true); });
}

function igExportAll(autoDownload){
  const segs = (IG.last && IG.last.segments) || [];
  if(!segs.length){ igStatus("请先生成长图", true); return; }
  let k = 0;
  function step(){
    if(k >= segs.length){
      igStatus("全部分段已就绪，可直接点击下载");
      if(autoDownload){ igDownloadAllFiles(); }
      return;
    }
    const s = segs[k];
    if(s.url){ k++; step(); return; }
    api("/api/ig_crop", {filename: IG.last.filename, y0:s.y0, y1:s.y1}).then(function(res){
      if(res.url){ s.url = res.url; s.filename = res.filename; }
      igRenderSegs();
      k++;
      setTimeout(step, 120);
    }).catch(function(){ k++; setTimeout(step, 120); });
  }
  step();
}

function igDownloadAllFiles(){
  const segs = (IG.last && IG.last.segments) || [];
  for(let i=0;i<segs.length;i++){
    (function(s, idx){
      if(!s.url){ return; }
      setTimeout(function(){
        const a = document.createElement("a");
        a.href = s.url;
        a.download = s.filename || "";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }, idx * 400);
    })(segs[i], i);
  }
}

</script>
<style>
.sitemask{position:fixed;inset:0;background:rgba(4,6,14,.68);z-index:90;display:none;align-items:center;justify-content:center;padding:16px}
.sitemask.on{display:flex}
.sitebox{width:100%;max-width:420px;max-height:86vh;overflow-y:auto;border-radius:16px;padding:18px;
border:1px solid rgba(240,215,156,.3);background:linear-gradient(160deg,#221a3d,#0e0c18);color:#eae4f6}
.sitebox h3{margin:0 0 14px;font-size:15px;color:#f0d79c;letter-spacing:2px}
.sitebox label{display:block;margin:12px 0 5px;font-size:12px;color:#9c93bd;letter-spacing:1px}
.sitebox input[type=text],.sitebox input:not([type]){width:100%;box-sizing:border-box;padding:9px 11px;
border-radius:10px;border:1px solid rgba(168,160,220,.3);background:rgba(12,10,22,.7);color:#eae4f6;font-size:13px;font-family:inherit}
.sitebox input[type=file]{width:100%;font-size:12px;color:#9c93bd}
.siteimgwrap{margin-top:6px;border-radius:12px;overflow:hidden;border:1px dashed rgba(168,160,220,.3);min-height:52px;display:flex;align-items:center;justify-content:center}
.siteimgwrap img{display:none;width:100%;height:auto}
.sitebtns{display:flex;gap:10px;margin-top:16px}
.sitebtns button{flex:1;padding:10px 0;border-radius:999px;border:none;font-size:13px;font-family:inherit;cursor:pointer}
#siteCancel{background:rgba(120,110,180,.18);color:#b6aedb;border:1px solid rgba(168,160,220,.3)}
#siteSave{background:linear-gradient(120deg,#f0d79c,#e0b978);color:#1a1428;font-weight:700}
.sitestatus{margin-top:10px;font-size:12px;color:#8e86ad;min-height:16px;text-align:center}
</style>
<div class="sitemask" id="siteMask">
  <div class="sitebox">
    <h3>首页设置</h3>
    <label>站点标题</label>
    <input id="siteTitle" placeholder="PPTAROT">
    <label>Banner 图片</label>
    <div class="siteimgwrap"><img id="sitePreview" alt=""></div>
    <input type="file" id="siteFile" accept="image/*">
    <label>跳转链接（点击 banner 去哪，可留空）</label>
    <input id="siteLink" placeholder="https://">
    <div class="sitebtns">
      <button id="siteCancel">取消</button>
      <button id="siteSave">保存</button>
    </div>
    <div class="sitestatus" id="siteStatus"></div>
  </div>
</div>
<script>
(function(){
  var mask = document.getElementById("siteMask");
  var titleEl = document.getElementById("siteTitle");
  var linkEl = document.getElementById("siteLink");
  var fileEl = document.getElementById("siteFile");
  var prev = document.getElementById("sitePreview");
  var st = document.getElementById("siteStatus");
  var curImg = "";

  function showPrev(u){
    if (u){ prev.src = u; prev.style.display = "block"; }
    else { prev.removeAttribute("src"); prev.style.display = "none"; }
  }

  function openSite(){
    mask.classList.add("on");
    st.textContent = "";
    fetch("/api/site", {cache:"no-store"}).then(function(r){ return r.json(); }).then(function(d){
      titleEl.value = d.site_title || "";
      linkEl.value = d.banner_link || "";
      curImg = d.banner_img || "";
      showPrev(curImg);
    }).catch(function(){ st.textContent = "读取失败"; });
  }

  window.openSitePanel = openSite;
  document.getElementById("siteCancel").onclick = function(){ mask.classList.remove("on"); };
  mask.onclick = function(e){ if (e.target === mask) mask.classList.remove("on"); };

  fileEl.onchange = function(){
    var f = fileEl.files && fileEl.files[0];
    if (!f) return;
    st.textContent = "处理中…";
    var fr = new FileReader();
    fr.onload = function(){
      var img = new Image();
      img.onload = function(){
        var sc = Math.min(1, 1080 / img.width);
        var cv = document.createElement("canvas");
        cv.width = Math.round(img.width * sc);
        cv.height = Math.round(img.height * sc);
        cv.getContext("2d").drawImage(img, 0, 0, cv.width, cv.height);
        var dataUrl = cv.toDataURL("image/jpeg", 0.86);
        fetch("/api/site_upload", {method:"POST", headers:{"Content-Type":"application/json"},
          body: JSON.stringify({data: dataUrl})}).then(function(r){ return r.json(); }).then(function(d){
          if (d && d.url){ curImg = d.url; showPrev(d.url); st.textContent = "图片已上传，记得点保存"; }
          else st.textContent = (d && d.error) || "上传失败";
        }).catch(function(){ st.textContent = "上传失败"; });
      };
      img.onerror = function(){ st.textContent = "图片读取失败"; };
      img.src = fr.result;
    };
    fr.readAsDataURL(f);
  };

  document.getElementById("siteSave").onclick = function(){
    st.textContent = "保存中…";
    fetch("/api/site_save", {method:"POST", headers:{"Content-Type":"application/json"},
      body: JSON.stringify({banner_img: curImg, banner_link: linkEl.value.trim(), site_title: titleEl.value.trim()})
    }).then(function(r){ return r.json(); }).then(function(d){
      if (d && d.ok) st.textContent = "已保存，刷新前台即可看到";
      else st.textContent = (d && d.error) || "保存失败";
    }).catch(function(){ st.textContent = "保存失败"; });
  };
})();
</script>
</main>
</div>
</body>
</html>"""


PAGE = PAGE.replace("/*__CARDS__*/[]", "/*__CARDS__*/" + json.dumps(CARD_NAMES, ensure_ascii=False))


# ==================== 前台抽牌页 ====================
FRONT_WECHAT = "PPHAVEAGOODNIGHT"


def _front_cards_json():
    out = []
    for _nm in CARD_NAMES:
        _f = card_file(_nm)
        out.append({"n": _nm,
                    "u": ("/cards/" + quote(_f)) if _f else "",
                    "k": get_keywords(_nm, "正"),
                    "kr": get_keywords(_nm, "逆").replace(INVERSE_SUFFIX, "")})
    return json.dumps(out, ensure_ascii=False)


try:
    from front_page import build_front as _build_front
except Exception as _e:
    print("前台模块加载失败：", _e)
    _build_front = None

if _build_front is None:
    FRONT_PAGE = "<h3 style='font-family:sans-serif'>前台页面缺失：front_page.py 未找到</h3>"
else:
    FRONT_PAGE = _build_front(_front_cards_json(), FRONT_WECHAT)

try:
    from front_page import build_login as _build_login
except Exception as _e2:
    print("登录页模块加载失败：", _e2)
    _build_login = None

if _build_login is None:
    LOGIN_PAGE = "<h3 style='font-family:sans-serif'>登录页缺失：front_page.py 未找到</h3>"
else:
    LOGIN_PAGE = _build_login()


# ==================== 管理后台登录鉴权 ====================
# 账号密码不写死在代码里：优先级 config.py > 环境变量 > 默认值
try:
    import config as _local_config
except Exception:
    _local_config = None


def _cfg(name, default=""):
    v = getattr(_local_config, name, None) if _local_config else None
    if v:
        return v
    return os.environ.get("PPTAROT_" + name, default)


ADMIN_USER = _cfg("ADMIN_USER", "admin")
ADMIN_PASS = _cfg("ADMIN_PASS", "")
if not ADMIN_PASS:
    ADMIN_PASS = secrets.token_urlsafe(9)
    print("[启动] 未配置后台密码，本次随机密码：%s" % ADMIN_PASS)

SESSION_TTL = 12 * 3600          # 登录有效期 12 小时
SESSIONS = {}                    # token -> 过期时间戳


def new_session():
    token = secrets.token_urlsafe(24)
    SESSIONS[token] = time.time() + SESSION_TTL
    return token


def session_valid(token):
    if not token:
        return False
    exp = SESSIONS.get(token)
    if not exp:
        return False
    if exp < time.time():
        SESSIONS.pop(token, None)
        return False
    return True


# ==================== HTTP 服务 ====================

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    # ---- 登录态 ----
    def _cookie_token(self):
        raw = self.headers.get("Cookie", "") or ""
        for part in raw.split(";"):
            k, _, v = part.strip().partition("=")
            if k == "ppt_session":
                return v
        return None

    def _authed(self):
        return session_valid(self._cookie_token())

    def _client_ip(self):
        """取真实客户端 IP：优先代理头，其次直连地址。"""
        for h in ("X-Forwarded-For", "X-Real-IP", "CF-Connecting-IP"):
            v = self.headers.get(h)
            if v:
                return v.split(",")[0].strip()
        return (self.client_address[0] if self.client_address else "") or ""

    def _redirect(self, location):
        self.send_response(302)
        self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _send_json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def _serve_static(self, prefix, base_dir):
        rel = unquote(self.path[len(prefix):]).split("?")[0]
        rel = rel.replace("\\", "/").strip("/")
        if not rel or ".." in rel.split("/"):
            self.send_response(404)
            self.end_headers()
            return
        fp = os.path.normpath(os.path.join(base_dir, rel))
        if not fp.startswith(os.path.normpath(base_dir)) or not os.path.isfile(fp):
            self.send_response(404)
            self.end_headers()
            return
        low = fp.lower()
        if low.endswith(".png"):
            ctype = "image/png"
        elif low.endswith((".jpg", ".jpeg")):
            ctype = "image/jpeg"
        elif low.endswith(".webp"):
            ctype = "image/webp"
        elif low.endswith(".gif"):
            ctype = "image/gif"
        else:
            ctype = "application/octet-stream"
        with open(fp, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        _path = urlparse(self.path).path
        if _path in ("/login", "/login.html"):
            if self._authed():
                self._redirect("/admin")
                return
            body = LOGIN_PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif _path == "/api/site":
            conn = db_conn()
            try:
                self._send_json(get_site(conn))
            finally:
                conn.close()
        elif _path == "/api/poster":
            try:
                import share_poster
                _q = urlparse(self.path).query or ""
                _v = ""
                for _kv in _q.split("&"):
                    if _kv.startswith("variant="):
                        _v = unquote(_kv.split("=", 1)[1]).upper()
                # 未指定 variant 时，在 B（黄道环+塔罗牌背）与 C（星尘螺旋流）间随机
                if _v not in ("A", "B", "C"):
                    _v = random.choice(("B", "C"))
                body = share_poster.poster_bytes(variant=_v, fmt="JPEG")
                self.send_response(200)
                self.send_header("Content-Type", "image/jpeg")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
                self.end_headers()
                self.wfile.write(body)
            except Exception as _e:
                self._send_json({"ok": False, "err": str(_e)})
        elif _path in ("/", "/index.html", "/front"):
            body = FRONT_PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif _path in ("/admin", "/admin/", "/admin.html"):
            if not self._authed():
                self._redirect("/login")
                return
            body = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path.startswith("/cards/"):
            self._serve_static("/cards/", CARD_DIR)
        elif self.path.startswith("/assets/"):
            self._serve_static("/assets/", ASSET_DIR)
        elif self.path.startswith("/longimage/"):
            if not self._authed():
                self._redirect("/login")
                return
            self._serve_static("/longimage/", LONG_DIR)
        elif self.path.startswith("/groupimage/"):
            if not self._authed():
                self._redirect("/login")
                return
            self._serve_static("/groupimage/", SINGLE_DIR)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        data = self._read_json()

        # ---- 登录 / 登出（不需要登录态）----
        if self.path == "/api/login":
            u = (data.get("username") or "").strip()
            pw = data.get("password") or ""
            if u == ADMIN_USER and pw == ADMIN_PASS:
                token = new_session()
                body = json.dumps({"ok": True}, ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Set-Cookie",
                                 "ppt_session=%s; Path=/; Max-Age=%d; HttpOnly; SameSite=Lax" % (token, SESSION_TTL))
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self._send_json({"error": "账号或密码不对"}, 401)
            return

        if self.path == "/api/logout":
            tk = self._cookie_token()
            if tk:
                SESSIONS.pop(tk, None)
            body = json.dumps({"ok": True}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Set-Cookie", "ppt_session=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # ---- 星盘/运势（公开，供前台客户使用，不需要登录）----
        if self.path == "/api/fortune":
            if fortune_engine is None:
                self._send_json({"ok": False, "error": "运势引擎没加载，请检查 pyswisseph 是否已安装"})
                return
            try:
                uid = (data.get("uid") or "").strip()
                cid = int(data.get("id") or 0)
                try:
                    offset = int(data.get("offset") or 0)
                except Exception:
                    offset = 0
                if offset < -7:
                    offset = -7
                if offset > 7:
                    offset = 7
                if cid:
                    row = chart_get(uid, cid)
                else:
                    items = chart_list(uid, 1)
                    row = chart_get(uid, items[0]["id"]) if items else None
                if not row:
                    self._send_json({"ok": False, "no_arch": True, "error": "还没有生日档案"})
                    return
                birth = row.get("birth") or ""
                dp = birth.split(" ")[0].split("-")
                tp = (birth.split(" ")[1] if " " in birth else "12:00").split(":")
                y = int(dp[0] or 2000)
                mo = int(dp[1] or 1)
                d = int(dp[2] or 1)
                hh = int(tp[0] or 12)
                mi = int(tp[1] or 0) if len(tp) > 1 else 0
                rep = fortune_engine.fortune_report(
                    y, mo, d, hh, mi, float(row["lat"]), float(row["lon"]),
                    bool(row.get("time_known", 1)), offset)
                rep["arch"] = {
                    "id": row["id"], "name": row["name"], "birth": row["birth"],
                    "region": row["region"], "sun": row["sun"], "moon": row["moon"],
                    "asc": row["asc"], "time_known": bool(row.get("time_known", 1)),
                }
                self._send_json(rep)
            except Exception as e:
                self._send_json({"ok": False, "error": "算不出来：%s" % e})
            return

        if self.path == "/api/astro":
            if astro_engine is None:
                self._send_json({"ok": False, "error": "星盘引擎没加载，请检查 pyswisseph 是否已安装"})
                return
            try:
                y = int(data.get("y") or 0); mo = int(data.get("m") or 0); d = int(data.get("d") or 0)
                hh = int(data.get("hh") or 12); mi = int(data.get("mm") or 0)
                time_known = bool(data.get("time_known", True))
                lat = data.get("lat"); lon = data.get("lon")
                if lat is None or lon is None:
                    self._send_json({"ok": False, "error": "请选择出生城市"}); return
                if not (1900 <= y <= 2100 and 1 <= mo <= 12 and 1 <= d <= 31):
                    self._send_json({"ok": False, "error": "生日填得不对"}); return
                if time_known and not (0 <= hh <= 23 and 0 <= mi <= 59):
                    self._send_json({"ok": False, "error": "出生时间填得不对"}); return
                rep = astro_engine.daily_report(y, mo, d, hh, mi, float(lat), float(lon), time_known)
                rep["city"] = data.get("city") or ""
                self._send_json(rep)
            except Exception as e:
                self._send_json({"ok": False, "error": "算不出来：%s" % e})
            return

        # ---- 星盘档案：前台保存 / 列表 / 删除（公开，供客户自己管理）----
        if self.path in ("/api/chart_save", "/api/chart_list", "/api/chart_del", "/api/chart_get"):
            try:
                uid = (data.get("uid") or "").strip()
                if self.path == "/api/chart_list":
                    self._send_json({"ok": True, "items": chart_list(uid)})
                    return
                if self.path == "/api/chart_get":
                    row = chart_get(uid, int(data.get("id") or 0))
                    if row:
                        self._send_json({"ok": True, "item": row})
                    else:
                        self._send_json({"ok": False, "error": "这条档案不在了"})
                    return
                if self.path == "/api/chart_del":
                    n = chart_del(uid, int(data.get("id") or 0))
                    self._send_json({"ok": True, "deleted": n})
                    return
                # chart_save
                if astro_engine is None:
                    self._send_json({"ok": False, "error": "星盘引擎没加载，请检查 pyswisseph 是否已安装"})
                    return
                y = int(data.get("y") or 0); mo = int(data.get("m") or 0); d = int(data.get("d") or 0)
                hh = int(data.get("hh") or 12); mi = int(data.get("mm") or 0)
                time_known = bool(data.get("time_known", True))
                lat = data.get("lat"); lon = data.get("lon")
                if lat is None or lon is None:
                    self._send_json({"ok": False, "error": "请选择出生城市"}); return
                if not (1900 <= y <= 2100 and 1 <= mo <= 12 and 1 <= d <= 31):
                    self._send_json({"ok": False, "error": "生日填得不对"}); return
                if time_known and not (0 <= hh <= 23 and 0 <= mi <= 59):
                    self._send_json({"ok": False, "error": "出生时间填得不对"}); return
                rep = astro_engine.daily_report(y, mo, d, hh, mi, float(lat), float(lon), time_known)
                rep["city"] = data.get("city") or ""
                chart = rep.get("chart") or {}
                birth = "%d-%02d-%02d %02d:%02d" % (y, mo, d, hh, mi)
                nid = chart_save(uid, (data.get("name") or "").strip(), birth, time_known,
                                 (data.get("city") or "").strip(), float(lat), float(lon),
                                 rep.get("sun") or "", rep.get("moon") or "", rep.get("asc") or "",
                                 json.dumps(chart, ensure_ascii=False),
                                 (data.get("relation") or "").strip())
                rep["id"] = nid
                rep["ok"] = True
                self._send_json(rep)
            except Exception as e:
                self._send_json({"ok": False, "error": "算不出来：%s" % e})
            return

        # ---- 前台行为埋点（公开，匿名，仅供本人后台统计）----
        if self.path == "/api/track":
            try:
                ip = self._client_ip()
                ua = (self.headers.get("User-Agent") or "")[:300]
                vid = (data.get("vid") or "").strip()[:64] or ("ip_" + ip)
                etype = (data.get("etype") or "").strip()
                if not _rate_ok(ip, 300 if etype == "visit" else TRACK_LIMIT):
                    self._send_json({"ok": True, "skip": 1})
                    return
                if etype == "visit":
                    track_visit(vid, ip, ua)
                elif etype in EVENT_TYPES:
                    track_event(vid, ip, ua, etype,
                                data.get("cat") or "", data.get("result") or "",
                                data.get("detail") or "", data.get("q") or "")
                else:
                    self._send_json({"ok": False, "error": "类型不对"})
                    return
                self._send_json({"ok": True})
            except Exception as e:
                self._send_json({"ok": False, "error": str(e)})
            return

        # ---- 其余接口一律要求已登录 ----
        if not self._authed():
            self._send_json({"error": "未登录或登录已过期，请重新登录"}, 401)
            return

        conn = db_conn()
        try:
            if self.path == "/api/ig_draw":
                self._send_json(random_draw(data.get("groups", 3)))

            elif self.path == "/api/ig_upload":
                self._send_json(save_upload_image(data.get("data"), data.get("kind", "cover")))

            elif self.path == "/api/ig_crop":
                self._send_json(crop_long_image(data))

            elif self.path == "/api/ig_generate":
                self._send_json(compose_long_image(data))

            elif self.path == "/api/ig_generate_group":
                self._send_json(compose_group_images(data))

            elif self.path == "/api/igs_generate_long":
                self._send_json(compose_single_long_image(data))

            elif self.path == "/api/igs_crop":
                self._send_json(crop_long_image(data))

            elif self.path == "/api/check":
                name = data.get("name", "")
                history = get_history(conn, name) if name else []
                summary = []
                for h in history:
                    line = f"<div class='item'>[{h['date']}] {h['q_type']} | {h['question']} ｜ 牌：{h['cards']}"
                    if h["feedback"]:
                        line += f" ｜ 反馈：{h['feedback']}"
                    line += "</div>"
                    summary.append(line)
                self._send_json({"is_old": bool(history), "count": len(history),
                                 "summary_html": "".join(summary)})

            elif self.path == "/api/charts":
                self._send_json({"ok": True, "items": admin_charts()})

            # ---- 数据统计（登录后可见）----
            elif self.path == "/api/stats":
                self._send_json(dict(admin_stats(data.get("days") or 14), ok=True))

            elif self.path == "/api/events":
                self._send_json(admin_events(
                    etype=(data.get("etype") or "").strip(),
                    kw=(data.get("kw") or "").strip(),
                    days=int(data.get("days") or 0),
                    limit=int(data.get("limit") or 100),
                    offset=int(data.get("offset") or 0)))

            elif self.path == "/api/visitors":
                self._send_json({"ok": True, "items": admin_visitors(
                    limit=int(data.get("limit") or 300), kw=(data.get("kw") or "").strip())})

            elif self.path == "/api/visitor_del":
                self._send_json({"ok": True, "deleted": admin_visitor_del((data.get("vid") or "").strip())})

            elif self.path == "/api/visitor_note":
                admin_visitor_note((data.get("vid") or "").strip(), (data.get("note") or "").strip())
                self._send_json({"ok": True})

            elif self.path == "/api/chart_remove":
                self._send_json({"ok": True, "deleted": admin_chart_del(int(data.get("id") or 0))})

            elif self.path == "/api/site_save":
                self._send_json(set_site(conn, data))

            elif self.path == "/api/site_upload":
                self._send_json(save_site_banner(data.get("data")))

            elif self.path == "/api/parse":
                cards = parse_cards(data.get("cards", ""))
                self._send_json({"cards": cards})

            elif self.path == "/api/prompt":
                name = data.get("name", "")
                history = get_history(conn, name) if name else []
                cards = parse_cards(data.get("cards", ""))
                if not cards:
                    self._send_json({"error": "牌面格式不正确"}, 400)
                    return
                prompt = build_prompt(name, history, data.get("qtype", "综合"),
                                      data.get("question", ""), data.get("spread", ""), cards)
                save_prompt_log(name, prompt)
                self._send_json({"prompt": prompt, "cards": cards})

            elif self.path == "/api/save":
                name = (data.get("name") or "").strip()
                if not name:
                    self._send_json({"error": "客户称呼必填，用于后续搜索"}, 400)
                    return
                conn2 = conn
                client_id = get_client_id(conn2, name)
                c = conn2.cursor()
                c.execute("""INSERT INTO cases (client_id, date, q_type, question, spread, cards, reading)
                             VALUES (?, ?, ?, ?, ?, ?, ?)""",
                          (client_id, datetime.date.today().isoformat(), data.get("qtype", "综合"),
                           data.get("question", ""), data.get("spread", ""),
                           data.get("cards", ""), data.get("reading", "")))
                conn2.commit()
                self._send_json({"ok": True})

            elif self.path == "/api/cases":
                name = data.get("name", "")
                history = get_history(conn, name)
                if not history:
                    self._send_json({"error": "未找到该客户记录"}, 404)
                    return
                ids = get_case_ids(conn, name)
                for i, h in enumerate(history):
                    h["id"] = ids[i]
                self._send_json({"cases": history})

            elif self.path == "/api/feedback":
                cid = data.get("id")
                feedback = data.get("feedback", "")
                if not cid or not feedback:
                    self._send_json({"error": "参数不完整"}, 400)
                    return
                c = conn.cursor()
                c.execute("UPDATE cases SET feedback = ? WHERE id = ?", (feedback, cid))
                conn.commit()
                self._send_json({"ok": True})

            elif self.path == "/api/update_field":
                cid = data.get("id")
                field = data.get("field", "")
                value = data.get("value", "")
                if not cid or field not in ("reading", "feedback"):
                    self._send_json({"error": "参数不完整"}, 400)
                    return
                c = conn.cursor()
                c.execute(f"UPDATE cases SET {field} = ? WHERE id = ?", (value, cid))
                conn.commit()
                self._send_json({"ok": True})

            elif self.path == "/api/history":
                name = data.get("name", "")
                if name == "*":
                    clients = all_clients(conn)
                    if not clients:
                        self._send_json({"error": "暂无客户记录"}, 404)
                    else:
                        self._send_json({"clients": clients})
                else:
                    history = get_history(conn, name)
                    if not history:
                        self._send_json({"error": "未找到该客户记录"}, 404)
                    else:
                        ids = get_case_ids(conn, name)
                        for i, h in enumerate(history):
                            h["id"] = ids[i]
                        self._send_json({"cases": history})
            else:
                self._send_json({"error": "not found"}, 404)
        except Exception as e:
            self._send_json({"error": str(e)}, 500)
        finally:
            conn.close()


def main():
    init_db()
    base = f"http://127.0.0.1:{PORT}"
    url = base + "/"
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    print(f"PPTAROT 管理后台：{url}")
    print(f"前台抽牌页（发给客户）：{base}/")
    print("按 Ctrl+C 停止服务")
    try:
        ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")


if __name__ == "__main__":
    main()
