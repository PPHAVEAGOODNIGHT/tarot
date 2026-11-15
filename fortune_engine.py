# -*- coding: utf-8 -*-
"""PPTAROT 日运引擎 v1.0
输入本命出生信息，输出前台「今日运势」页所需的结构化数据：
分数 / 星级 / 状态标签 / 六维指标 / 幸运色·数字·方向 / 水晶 / 分模块文案。
同一个人同一天结果固定（用出生信息+日期做种子），保证用户刷新不跳变。
"""
import hashlib
from datetime import datetime, timedelta

import astro_engine as AE

# ---------- 文案词库 ----------

# 月亮落在各星座时，今天的情绪底色（说人话，不掉术语）
MOON_PSY = {
    "白羊": "情绪来得快，一有不满就想当场解决，忍不了含糊",
    "金牛": "只想抓点摸得着的东西，虚的话听着就烦",
    "双子": "脑子转得比嘴快，想法一堆，反而抓不住重点",
    "巨蟹": "特别容易被一句话戳到，第一反应是躲回自己的壳里",
    "狮子": "很想被认真对待，哪怕只是一句真心的认可",
    "处女": "看什么都不太顺眼，得把事情理干净才踏实",
    "天秤": "不太想一个人待着，需要有人回应你、跟你站一边",
    "天蝎": "容易钻牛角尖，非要把事情背后那层挖出来",
    "射手": "坐不住，想往外跑，琐事一件都不想管",
    "摩羯": "习惯性把情绪往下压，先把事做完再说心里的事",
    "水瓶": "有点抽离，站在旁边看别人热闹，自己不想下场",
    "双鱼": "共情开得太大，别人的情绪容易被你当成自己的",
}

# 行星在你身上的具体所指（比术语好懂）
F_TW = {
    "太阳": "自我", "月亮": "情绪", "水星": "表达和思路", "金星": "关系和钱",
    "火星": "行动力", "木星": "运气", "土星": "责任", "天王星": "变动",
    "海王星": "边界感", "冥王星": "藏得最深的那块", "上升": "对外的样子", "天顶": "事业",
}

# 行运相位 → 一句话现象（口语版）
ASPECT_SAY = {
    "合": "正好压在「%s」上",
    "冲": "顶着你的「%s」",
    "刑": "和「%s」卡住了",
    "拱": "顺着你的「%s」",
    "六分": "给你的「%s」开了个小口",
}

# 相位调性：(分数修正, 现象, 建议)
ASPECT_TONE = {
    "合": (4, "有件事贴得太近，你已经分不清是情绪还是事实", "先退一步看清楚，再决定要不要动"),
    "六分": (5, "有个小口子能钻，主动一点就成", "挑一件最想做的，推它一把"),
    "拱": (9, "整体是顺的，想做的事容易接上", "别把好状态浪费在反复纠结上"),
    "刑": (-8, "心里堵着一块，越忍越胀", "找个出口讲出来，别自己咽下去"),
    "冲": (-9, "有人或有事在对面推你，一碰就容易起火", "先弄清对方真正想要什么，别急着回嘴"),
}

# 月相：(分数修正, 一句话)
PHASE = {
    "新月": (3, "新月刚起头，适合播种，不适合验收"),
    "上弦": (0, "上弦月推到一半，最容易卡在中间"),
    "满月": (2, "满月情绪满到边，憋着的话容易脱口而出"),
    "下弦": (-1, "下弦月该收尾了，别再硬开新坑"),
}

# 幸运色：按当日月亮星座给一组候选，用种子选一个
COLORS = {
    "白羊": [("正红", "#e2564a"), ("砖橙", "#d97a3d")],
    "金牛": [("奶油白", "#f2e6d2"), ("苔绿", "#7c9b6a")],
    "双子": [("亮黄", "#f0d264"), ("雾蓝", "#8fb6d9")],
    "巨蟹": [("月白", "#e8ecef"), ("银灰", "#b8c0cc")],
    "狮子": [("金棕", "#d9a441"), ("暖橘", "#e88b4a")],
    "处女": [("豆沙绿", "#9bb08a"), ("亚麻", "#d8cdb8")],
    "天秤": [("藕粉", "#e8a0b8"), ("浅蓝", "#a7c4e0")],
    "天蝎": [("深酒红", "#8c2a3e"), ("墨黑", "#2b2530")],
    "射手": [("宝蓝", "#3f6fd1"), ("紫罗兰", "#8f6fd1")],
    "摩羯": [("炭灰", "#5a5866"), ("深棕", "#6b5342")],
    "水瓶": [("电光蓝", "#4fb6d9"), ("雾紫", "#a99bcf")],
    "双鱼": [("海雾紫", "#b3a5d6"), ("青碧", "#6fc0b8")],
}

# 幸运方位：按月亮星座
DIRS = {
    "白羊": "正东", "金牛": "东南", "双子": "东偏南", "巨蟹": "正北",
    "狮子": "正南", "处女": "西南", "天秤": "正西", "天蝎": "西北",
    "射手": "南偏西", "摩羯": "正北", "水瓶": "西偏南", "双鱼": "东北",
}

# 推荐水晶：按月亮星座
CRYSTAL = {
    "白羊": ("红玛瑙", "火气冲的时候握一下，把急劲过一遍"),
    "金牛": ("绿幽灵", "想稳住节奏、把钱抓牢的时候戴"),
    "双子": ("海蓝宝", "话多心乱时压一压，别把话说满"),
    "巨蟹": ("月光石", "情绪容易被带走时贴着皮肤放，先照顾自己"),
    "狮子": ("金发晶", "需要被看见的场合，帮你把气场立住"),
    "处女": ("白水晶", "想太多的时候清一清脑子，只留一件要紧事"),
    "天秤": ("粉晶", "等人回应、心里没底的时候用"),
    "天蝎": ("黑曜石", "钻牛角尖的时候挡一挡，别往死里想"),
    "射手": ("黄水晶", "要行动、要出门、要开场的时候用"),
    "摩羯": ("茶晶", "扛事扛到累的时候托一下，别硬撑"),
    "水瓶": ("萤石", "脑子抽离、理不清思路的时候戴"),
    "双鱼": ("紫水晶", "共情过头、睡不好觉的时候放枕边"),
}

# 六维指标定义：key / 名称 / 相关行星
DIMS = [
    ("love", "情感", ["月亮", "金星"]),
    ("career", "事业", ["太阳", "火星", "土星"]),
    ("money", "财富", ["金星", "木星"]),
    ("study", "学业", ["水星", "木星"]),
    ("social", "人际", ["月亮", "金星", "火星"]),
    ("energy", "状态", ["太阳", "火星", "月亮"]),
]

# 分模块文案：按该维度分数分三档，每档多条，用种子挑
LOVE_TXT = {
    "high": [
        "感情这块今天不费劲。你自然的样子就有人接住，想说的话直接说，别绕弯子。",
        "今天你不需要表现得更好，对方要的就是你现在这个样子。",
        "有想联系的人，今天开口的时机是好的。别再把话在心里过第三遍。",
    ],
    "mid": [
        "感情上没什么大风浪，但也别指望对方猜。你说一句，比等一天管用。",
        "今天适合把话说清楚，不适合试探。试探只会让你自己更累。",
        "关系里那点小别扭，今天说开就过去了，攒着会变味。",
    ],
    "low": [
        "今天容易把对方一句普通的话听成别的意思。听完先别回，隔十分钟再想。",
        "你现在的难受，多半来自你自己在猜。猜出来的答案不算答案。",
        "今天不适合摊牌，也不适合追问。先把自己哄好，再谈关系。",
    ],
}

CAREER_TXT = {
    "high": [
        "手上的事今天推得动。挑最难的那件先做，趁状态好一次过。",
        "今天适合主动开口要资源、要机会，你的表达比平时有分量。",
        "有需要拍板的事，今天拍。拖到状态掉下去只会更犹豫。",
    ],
    "mid": [
        "工作上按部就班就行，别贪多。做完一件划掉一件，今天要的是进度不是完美。",
        "今天适合把手头的活理清楚，把不该你扛的事交回去。",
        "有个小卡点会自己松开，别提前焦虑。",
    ],
    "low": [
        "今天别在会上硬碰。你现在的火气，说出口的话容易被人记住。",
        "做事之前先确认一遍对方的要求，今天最容易返工。",
        "状态不好就少接活，硬撑出来的成果，回头还得重做一次。",
    ],
}

MONEY_TXT = {
    "high": [
        "钱这块今天有进项或者好消息。该谈的价格可以谈，别自己先让一步。",
        "适合把账理一理，你会比平时更容易看清哪笔钱不该花。",
        "有小财进来的迹象，跟钱有关的事今天主动一点。",
    ],
    "mid": [
        "财运平平，别乱动。今天赚不到快钱，但也不会亏。",
        "有想买的东西，先放一天。明天还想要，再买也不迟。",
        "今天适合记账，不适合下单。",
    ],
    "low": [
        "今天容易因为情绪花钱，尤其是被人激到的时候。卡先收起来。",
        "涉及借钱、垫付、担保的事，今天一律往后推。",
        "别听人画饼。今天你对数字的判断容易被情绪带偏。",
    ],
}

HEADLINES = {
    "high": [
        "状态在线，挑最要紧的那件去推。",
        "顺的时候别省力，今天可以多走一步。",
        "该你做决定的事，今天就做。",
        "有人会接你的话茬，说的时候说清楚。",
    ],
    "mid": [
        "先把自己稳住，别急着解释。",
        "今天不适合硬撑，适合挑重点。",
        "该说的说清楚，猜的部分放下。",
        "慢一点，今天快反而容易错。",
        "把力气花在一件事上，别撒开。",
    ],
    "low": [
        "先别做决定，等这口气过去。",
        "把力气收回来，今天别往外撒。",
        "你不是不行，是时机不对。",
        "少揽事，今天顾好自己就够。",
    ],
}


def _seed(*parts):
    s = "|".join(str(p) for p in parts)
    h = hashlib.md5(s.encode("utf-8")).hexdigest()
    return int(h[:8], 16)


def _rnd(seed, lo, hi, salt=0):
    x = (seed * 1103515245 + 12345 + (salt + 7) * 2654435761) & 0x7FFFFFFF
    return lo + x % (hi - lo + 1)


def _pick(seed, arr, salt=0):
    if not arr:
        return ""
    return arr[_rnd(seed, 0, len(arr) - 1, salt)]


def _phase_of(sun_lon, moon_lon):
    d = (moon_lon - sun_lon) % 360.0
    if d < 45 or d >= 315:
        return "新月"
    if d < 135:
        return "上弦"
    if d < 225:
        return "满月"
    return "下弦"


def _retro(when, pname):
    try:
        import swisseph as swe
        jd = AE.jd_of(AE.to_ut(when))
        r, _ = swe.calc_ut(jd, AE.PID[pname], AE.FLG)
        return r[3] < 0
    except Exception:
        return False


def _clamp(v, lo, hi):
    return max(lo, min(hi, int(v)))


def fortune_report(y, m, d, hh=12, mm=0, lat=None, lon=None, time_known=True, offset=0, tz=8.0):
    """返回今日（或前后几天）运势结构化数据"""
    if lat is None or lon is None:
        raise ValueError("缺少出生地经纬度")
    if not time_known:
        hh, mm = 12, 0
    birth = datetime(y, m, d, hh, mm)
    ch = AE.natal(birth, float(lat), float(lon), tz)

    day = (datetime.now() + timedelta(days=int(offset))).date()
    when = datetime(day.year, day.month, day.day, 10, 0)

    jd = AE.jd_of(AE.to_ut(when))
    moon_lon = AE.lon_of(jd, AE.PID["月亮"])
    sun_lon = AE.lon_of(jd, AE.PID["太阳"])
    msign = int(moon_lon // 30)
    msign_name = AE.SIGNS[msign]
    phase = _phase_of(sun_lon, moon_lon)

    hits_moon = AE.scan(ch, when, ["月亮"], 5.0)
    hits_fast = AE.scan(ch, when, ["太阳", "水星", "金星", "火星"], 2.5)
    hits_slow = AE.scan(ch, when, ["木星", "土星", "天王星", "海王星", "冥王星"], 2.0)
    all_hits = hits_moon[:2] + hits_fast[:3] + hits_slow[:2]

    seed = _seed(y, m, d, hh, mm, day.isoformat())

    # ---- 分数 ----
    fix = 0
    main_hit = hits_moon[0] if hits_moon else None
    if main_hit:
        fix += ASPECT_TONE[main_hit["a"]][0]
    fix += PHASE[phase][0]
    mercury_retro = _retro(when, "水星")
    if mercury_retro:
        fix -= 4
    score = _clamp(70 + fix + _rnd(seed, -6, 6, 1), 46, 96)

    # ---- 星级 / 标签 ----
    stars = round(score / 100.0 * 5 * 2) / 2.0
    if score >= 88:
        tag, level = "顺势", 1
    elif score >= 78:
        tag, level = "稳中有进", 2
    elif score >= 68:
        tag, level = "平常心", 3
    elif score >= 58:
        tag, level = "收一收", 4
    else:
        tag, level = "慢下来", 5

    # ---- 六维 ----
    dims = []
    for idx, (key, dname, plist) in enumerate(DIMS):
        val = float(score)
        for h in all_hits:
            if h["t"] in plist or h["n"] in plist:
                val += ASPECT_TONE[h["a"]][0] * 0.55
        val += _rnd(seed, -5, 5, 10 + idx)
        dims.append({"k": key, "n": dname, "v": _clamp(val, 45, 99)})
    dv = {x["k"]: x["v"] for x in dims}

    # ---- 幸运项 ----
    col = COLORS.get(msign_name, [("月白", "#e8ecef")])[_rnd(seed, 0, len(COLORS.get(msign_name, [1])) - 1, 20)]
    n1 = _rnd(seed, 1, 9, 21)
    n2 = _rnd(seed, 1, 9, 22)
    if n2 == n1:
        n2 = n1 % 9 + 1
    crystal = CRYSTAL.get(msign_name, ("白水晶", "想太多的时候清一清脑子"))

    # ---- 文案 ----
    def tier(v):
        if v >= 82:
            return "high"
        if v >= 66:
            return "mid"
        return "low"

    head_tier = "high" if score >= 82 else ("mid" if score >= 66 else "low")
    lines_head = _pick(seed, HEADLINES[head_tier], 30)
    if main_hit:
        tone = ASPECT_TONE[main_hit["a"]]
        adv = tone[2]
        asp_sentence = "月亮%s——%s。" % (
            ASPECT_SAY.get(main_hit["a"], "碰到你的「%s」") % F_TW.get(main_hit["n"], main_hit["n"]),
            tone[1],
        )
        tail = "今天该做的是：%s。" % adv
    else:
        asp_sentence = "今天没有哪股力量逼着你，反而是难得的空档。"
        tail = "今天该做的是：把一直拖着的那件小事做完，比什么都实在。"

    overall = "月亮今天在%s——%s。%s%s%s" % (
        msign_name,
        MOON_PSY.get(msign_name, "情绪起伏比平时明显"),
        asp_sentence,
        PHASE[phase][1] + "。",
        tail,
    )

    sections = [
        {"t": "情感", "lines": [_pick(seed, LOVE_TXT[tier(dv["love"])], 40)]},
        {"t": "事业", "lines": [_pick(seed, CAREER_TXT[tier(dv["career"])], 41)]},
        {"t": "财富", "lines": [_pick(seed, MONEY_TXT[tier(dv["money"])], 42)]},
    ]

    caution = _pick(seed, [
        "今天别在情绪最满的那十分钟做决定。",
        "有人来问你要答案，你有权说再想想。",
        "今天容易把别人的情绪接过来，记得那是他的，不是你的。",
        "别用猜代替问。想问就直接问。",
        "累了就停，今天的效率靠的是清醒，不是硬撑。",
    ], 50)

    wd = "一二三四五六日"[day.weekday()]
    return {
        "ok": True,
        "date": day.isoformat(),
        "dateLabel": "%d月%d日 周%s" % (day.month, day.day, wd),
        "offset": int(offset),
        "time_known": bool(time_known),
        "sun_sign": AE.SIGNS[int(ch["planets"]["太阳"]["sign"])],
        "moon_sign": msign_name,
        "moon_phase": phase,
        "score": score,
        "stars": stars,
        "tag": tag,
        "tag_level": level,
        "headline": lines_head,
        "dims": dims,
        "lucky": {
            "color": {"n": col[0], "hex": col[1]},
            "number": "%d·%d" % (n1, n2),
            "dir": DIRS.get(msign_name, "正东"),
        },
        "crystal": {"n": crystal[0], "use": crystal[1]},
        "overall": overall,
        "sections": sections,
        "caution": caution,
        "raw": {
            "aspect": main_hit["a"] if main_hit else "",
            "planet": main_hit["n"] if main_hit else "",
            "transit": main_hit["t"] if main_hit else "",
            "mercury_retro": bool(mercury_retro),
        },
    }
