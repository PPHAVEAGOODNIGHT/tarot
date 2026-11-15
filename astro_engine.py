# -*- coding: utf-8 -*-
"""PPTAROT 星盘/运势引擎 v0.3
本命盘(Placidus宫位) + 三层时间行运(今日月亮/本周快行星/长期慢行星)
依赖 pyswisseph(Moshier算法,无需星历文件)
"""
import os
import swisseph as swe
from datetime import datetime, timedelta
import astro_words as AW

FLG = swe.FLG_MOSEPH | swe.FLG_SPEED
# 小行星(婚神星)需要星历文件 seas_18.se1，随项目放 ephe/ 目录
EPHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ephe")

def _ensure_ephe():
    """每次算盘前兜底设置星历目录，避免 import 时机/cwd 变化导致路径没生效"""
    try:
        swe.set_ephe_path(EPHE_DIR)
        return True
    except Exception as e:
        import sys
        print("[astro] set_ephe_path 失败:", repr(e), file=sys.stderr)
        return False

_ensure_ephe()

SIGNS=["白羊","金牛","双子","巨蟹","狮子","处女","天秤","天蝎","射手","摩羯","水瓶","双鱼"]
PLANETS=[("太阳",swe.SUN),("月亮",swe.MOON),("水星",swe.MERCURY),("金星",swe.VENUS),
         ("火星",swe.MARS),("木星",swe.JUPITER),("土星",swe.SATURN),
         ("天王星",swe.URANUS),("海王星",swe.NEPTUNE),("冥王星",swe.PLUTO),
         ("婚神星",swe.JUNO)]
PID=dict(PLANETS)
ASPECTS=[("合",0),("冲",180),("刑",90),("拱",120),("六分",60)]
MOON_SIGN={"白羊":"急,想马上动手","金牛":"稳,想抓点实在的","双子":"话多,脑子转不停",
 "巨蟹":"软,想缩回壳里","狮子":"想要被看见","处女":"挑刺,想把事情理干净",
 "天秤":"想找人陪,怕落单","天蝎":"沉,想挖到底","射手":"想跑,待不住",
 "摩羯":"硬撑,把情绪压下去","水瓶":"抽离,冷眼旁观","双鱼":"散,容易共情过头"}

def is_dst(d): return 1986<=d.year<=1991 and (4,15)<=(d.month,d.day)<=(9,15)
def jd_of(d): return swe.julday(d.year,d.month,d.day,d.hour+d.minute/60.0+d.second/3600.0)
def to_ut(d,tz=8.0): return d - timedelta(hours=tz-(1.0 if is_dst(d) else 0.0))
def lon_of(jd,p):
    r,_=swe.calc_ut(jd,p,FLG); return r[0]%360.0
def fmt(l):
    s=int(l//30); x=l-s*30; return "%s%02d°%02d'"%(SIGNS[s],int(x),int((x-int(x))*60))
def house_of(lon,cs):
    c=[cs[i]%360.0 for i in range(12)]
    for i in range(12):
        a=c[i]; b=c[(i+1)%12]
        if (a<=lon<b) if a<=b else (lon>=a or lon<b): return i+1
    return 1
def natal(dt,lat,lon,tz=8.0):
    _ensure_ephe()
    jd=jd_of(to_ut(dt,tz)); cs,am=swe.houses(jd,lat,lon,b"P")
    ch={"jd":jd,"asc":am[0],"mc":am[1],"cusps":[cs[i]%360.0 for i in range(12)],"planets":{}}
    for n,p in PLANETS:
        try:
            L=lon_of(jd,p); r,_=swe.calc_ut(jd,p,FLG)
        except Exception as e:
            if n=="婚神星":
                import sys
                print("[astro] 婚神星跳过:", repr(e), "ephe=", os.path.join(os.path.dirname(os.path.abspath(__file__)),"ephe"), file=sys.stderr)
                continue      # 星历文件缺失时跳过小行星，不影响主盘
            raise
        ch["planets"][n]={"lon":L,"sign":int(L//30),"house":house_of(L,cs),"retro":r[3]<0}
    return ch
def adiff(a,b):
    d=abs((a-b)%360.0); return min(d,360.0-d)
def scan(ch,when,group,orb):
    jd=jd_of(to_ut(when)); out=[]
    for tp in group:
        tl=lon_of(jd,PID[tp])
        tgt=[(k,v["lon"]) for k,v in ch["planets"].items()]+[("上升",ch["asc"]),("天顶",ch["mc"])]
        for tn,nl in tgt:
            for an,dg in ASPECTS:
                d=adiff(tl,nl)
                if abs(d-dg)<=orb:
                    out.append({"t":tp,"a":an,"n":tn,"orb":round(abs(d-dg),2),"s":round(1-abs(d-dg)/orb,2)})
    out.sort(key=lambda x:-x["s"]); return out

# ---- A方案文案骨架(示例句,后续由你扩充成词库) ----
MOON_ASP={"合":"这件事和你贴得太近,分不出是情绪还是事实","冲":"有人在对面推你,别急着回嘴",
 "刑":"心里堵着一块,说出来会轻一点","拱":"顺着,想做的事今天就做","六分":"有个小口子,主动一点就成"}
WEEK={"太阳":"你这几天在被人看见","水星":"这几天信息和沟通密集","金星":"这几天关系和钱是重点",
 "火星":"这几天你有力气往前推","木星":"这几天机会在往外扩","土星":"这几天该扛的责任压下来",
 "天王星":"这几天有突然的变动","海王星":"这几天容易看不清","冥王星":"这几天底下在翻旧账"}
TW={"太阳":"自我","月亮":"情绪","水星":"想法","金星":"关系和钱","火星":"行动力",
 "木星":"运气","土星":"要扛的责任","天王星":"要变的那部分","海王星":"边界",
 "冥王星":"藏得最深的那块","上升":"外在形象","天顶":"事业","婚神星":"你想找的那个人"}
def T(n):
    return "你的" + TW.get(n, n)

def natal_aspects(ch, orb=6.0):
    """本命盘内部的行星相位，供星盘画线用"""
    out=[]; ns=list(ch["planets"].keys())
    for i in range(len(ns)):
        for j in range(i+1,len(ns)):
            a=ch["planets"][ns[i]]["lon"]; b=ch["planets"][ns[j]]["lon"]
            d=adiff(a,b)
            for an,dg in ASPECTS:
                if abs(d-dg)<=orb:
                    out.append({"a":ns[i],"b":ns[j],"t":an,"orb":round(abs(d-dg),2)})
                    break
    out.sort(key=lambda x:x["orb"])
    return out


def chart_data(ch, time_known=True):
    """给前端画星盘用的原始度数"""
    return {
        "asc": round(ch["asc"],3),
        "mc": round(ch["mc"],3),
        "cusps": [round(ch["cusps"][i],3) for i in range(12)],
        "planets": [{"n":k,"lon":round(v["lon"],3),
                     "sign":int(v["lon"]//30),
                     "house":v["house"],
                     "retro":v["retro"]} for k,v in ch["planets"].items()],
        "aspects": natal_aspects(ch),
    }


def daily(ch, when=None):
    when=when or datetime.now()
    jd=jd_of(to_ut(when))
    mn=lon_of(jd,swe.MOON); msign=int(mn//30)
    moon_hits=scan(ch,when,["月亮"],5.0)[:2]
    week_hits=scan(ch,when,["太阳","水星","金星","火星"],2.0)[:2]
    slow_hits=scan(ch,when,["木星","土星","天王星","海王星","冥王星"],2.0)[:2]
    return {"msign":msign,"moon":moon_hits,"week":week_hits,"slow":slow_hits}

def render(ch,r):
    L=[]
    L.append("今天月亮在%s——%s。" % (SIGNS[r["msign"]], MOON_SIGN[SIGNS[r["msign"]]]))
    for h in r["moon"]:
        L.append("· 行运月亮%s%s:%s。" % (h["a"],T(h["n"]),MOON_ASP[h["a"]]))
    if r["week"]:
        L.append("本周:")
        for h in r["week"]:
            L.append("· 行运%s%s%s,%s。" % (h["t"],h["a"],T(h["n"]),WEEK.get(h["t"],"")))
    if r["slow"]:
        L.append("长期:")
        for h in r["slow"]:
            L.append("· 行运%s%s%s,还在继续。" % (h["t"],h["a"],T(h["n"])))
    return "\n".join(L)


# ==================== 前台统一入口 ====================
def daily_report(y, m, d, hh=12, mm=0, lat=None, lon=None, time_known=True, tz=8.0):
    """返回可直接 JSON 化的 dict，供 /api/astro 使用"""
    if lat is None or lon is None:
        raise ValueError("缺少出生地经纬度")
    if not time_known:
        hh, mm = 12, 0
    dt = datetime(y, m, d, hh, mm)
    ch = natal(dt, lat, lon, tz)
    r = daily(ch)

    today = ["今天月亮在%s——%s。" % (SIGNS[r["msign"]], MOON_SIGN[SIGNS[r["msign"]]])]
    for h in r["moon"]:
        today.append("行运月亮%s%s：%s。" % (h["a"], T(h["n"]), MOON_ASP[h["a"]]))
    blocks = [{"t": "今天", "lines": today}]
    if r["week"]:
        blocks.append({"t": "本周", "lines": [
            "行运%s%s%s，%s。" % (h["t"], h["a"], T(h["n"]), WEEK.get(h["t"], "")) for h in r["week"]]})
    if r["slow"]:
        blocks.append({"t": "这段时间", "lines": [
            "行运%s%s%s，还在继续。" % (h["t"], h["a"], T(h["n"])) for h in r["slow"]]})

    cd = chart_data(ch, time_known)
    if not time_known:
        cd["asc"] = None; cd["cusps"] = None

    # ---------- 星象卡牌（前台星盘页：九宫格 + 详解 + 星盘按钮）----------
    pf = ch["planets"]
    cards = []

    def _deg(nm_pos):
        sg = SIGNS[int(pf[nm_pos]["sign"])] if nm_pos in pf else ""
        return sg, (fmt(pf[nm_pos]["lon"])[len(sg):] if nm_pos in pf else "")

    if time_known:
        sg = SIGNS[int((ch["asc"] % 360.0) // 30)]
        cards.append({"n": "上升", "sym": AW.SYMBOL["上升"], "en": AW.EN["上升"],
                      "sign": sg, "deg": fmt(ch["asc"])[len(sg):], "house": 1,
                      "retro": False, "tag": AW.card_tag("上升", sg),
                      "hname": AW.house_name(1), "htext": AW.house_text("上升", 1),
                      "detail": AW.detail_text("上升", sg),
                      "combo": AW.combo_text("上升", sg, 1), "motto": AW.motto("上升")})
    for nm in AW.CARD_ORDER:
        if nm == "上升" or nm not in pf:
            continue
        p = pf[nm]
        sg = SIGNS[int(p["sign"])]
        hs = p["house"] if time_known else None
        cards.append({"n": nm, "sym": AW.SYMBOL.get(nm, ""), "en": AW.EN.get(nm, ""),
                      "sign": sg, "deg": fmt(p["lon"])[len(sg):],
                      "house": hs,
                      "retro": bool(p["retro"]), "tag": AW.card_tag(nm, sg),
                      "hname": AW.house_name(hs), "htext": AW.house_text(nm, hs),
                      "detail": AW.detail_text(nm, sg),
                      "combo": AW.combo_text(nm, sg, hs) if hs else "",
                      "motto": AW.motto(nm)})

    details = []
    for nm in ("太阳", "月亮", "上升", "婚神星"):
        if nm == "上升":
            if not time_known:
                continue
            sg = SIGNS[int((ch["asc"] % 360.0) // 30)]
        else:
            if nm not in pf:
                continue
            sg = SIGNS[int(pf[nm]["sign"])]
        full = AW.detail_text(nm, sg)
        parts = [x for x in full.split("\n") if x.strip()]
        details.append({"n": nm, "sign": sg, "motto": AW.motto(nm),
                        "text": parts[0] if parts else "",
                        "more": "".join(parts[1:])})

    return {
        "ok": True,
        "time_known": bool(time_known),
        "sun": fmt(ch["planets"]["太阳"]["lon"]),
        "moon": fmt(ch["planets"]["月亮"]["lon"]),
        "asc": fmt(ch["asc"]) if time_known else None,
        "mc": fmt(ch["mc"]) if time_known else None,
        "sun_sign": SIGNS[int(ch["planets"]["太阳"]["sign"])],
        "moon_sign_real": SIGNS[int(ch["planets"]["月亮"]["sign"])],
        "cards": cards,
        "details": details,
        "moon_sign": SIGNS[r["msign"]],
        "moon_note": MOON_SIGN[SIGNS[r["msign"]]],
        "blocks": blocks,
        "planets": [{"n": k, "pos": fmt(v["lon"]),
                     "house": (v["house"] if time_known else None),
                     "retro": v["retro"]} for k, v in ch["planets"].items()],
        "chart": cd,
    }

if __name__=="__main__":
    ch=natal(datetime(1994,8,15,14,30),39.9042,116.4074)
    print("A 北京 上升",fmt(ch["asc"]))
    for k in range(3):
        d=datetime.now()+timedelta(days=k)
        print("-"*50); print(d.strftime("%m-%d"))
        print(render(ch,daily(ch,d)))
