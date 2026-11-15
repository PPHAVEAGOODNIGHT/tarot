# -*- coding: utf-8 -*-
"""
PPTAROT 前台抽牌页
供客户使用：底部牌堆可横向滑动、拖到桌面自由摆放、轻点翻牌、再点看牌意。
右上角「合作咨询」弹出联系方式卡，可一键复制微信号。
"""

FRONT_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<meta name="theme-color" content="#0b1220">
<title>PPTAROT</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{--cw:64px;--ch:110px}
@media (min-width:560px){:root{--cw:84px;--ch:145px}}
html,body{height:100%}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;color:#eae4f6;overflow:hidden;
background:radial-gradient(1200px 700px at 18% 0%,#2a1f4d 0%,#141a30 45%,#070b14 100%);
user-select:none;-webkit-user-select:none;position:fixed;left:0;top:0;right:0;bottom:0}
#app{display:flex;flex-direction:column;height:100%}
header{position:relative;z-index:30;display:grid;grid-template-columns:max-content 1fr;align-items:center;
column-gap:9px;row-gap:0;padding:13px 12px 10px;min-height:50px;flex:0 0 auto}
.brand{position:static;left:auto;right:auto;top:auto;text-align:left;grid-column:1;grid-row:1;
justify-self:start;cursor:pointer;
-webkit-tap-highlight-color:transparent;font-size:17px;letter-spacing:3px;
color:#f0d79c;font-weight:700;text-shadow:0 0 16px rgba(240,215,156,.45)}
.brand:active{opacity:.72}
#view-home{display:flex;flex-direction:column;flex:1;min-height:0;overflow-y:auto;padding:8px 14px 24px}
#view-draw{display:flex;flex-direction:column;flex:1;min-height:0;position:relative}
.bnr{display:block;position:relative;border-radius:14px;overflow:hidden;margin:0;height:100%;
border:1px solid rgba(240,215,156,.25);background:linear-gradient(160deg,#2a1f4d,#141327);
box-shadow:0 8px 20px rgba(0,0,0,.4);text-decoration:none;min-height:112px}
.bnr img{display:block;width:100%;height:100%;object-fit:cover}
.bnr .ph{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;
height:100%;min-height:112px;text-align:center;padding:12px}
.bnr .ph b{font-size:14px;letter-spacing:2px;color:#f0d79c;font-weight:700}
.bnr .ph span{font-size:11.5px;color:#8e86ad;letter-spacing:1px;line-height:1.6}
.homebody{margin-top:14px;display:flex;flex-direction:column;gap:12px}
/* ==================== 第二层：塔罗牌方向选择页（塔罗牌 + 蝴蝶） ==================== */
#view-dir{position:relative;display:flex;flex-direction:column;flex:1;min-height:0;overflow-y:auto;
-webkit-overflow-scrolling:touch;padding:0 16px}
/* 内容靠上排布（不再垂直居中），避免小屏顶部留白过大 */
.dirWrap{position:relative;z-index:1;display:flex;flex-direction:column;
margin:0 0 auto;padding:18px 0 14px;width:100%}
/* 中轴星轨：四张窄卡压在线上，像一条牌阵 */
.dirWrap::before{content:"";position:absolute;left:50%;top:clamp(30px,5.4vh,46px);bottom:6px;
width:1px;margin-left:-.5px;z-index:0;
background:linear-gradient(180deg,transparent,rgba(240,215,156,.26) 10%,
rgba(143,233,221,.18) 52%,rgba(240,215,156,.10) 88%,transparent)}
.dirBg{position:absolute;left:0;top:0;right:0;bottom:0;pointer-events:none;overflow:hidden;z-index:0}
.dirBg .glow{position:absolute;left:50%;top:46%;width:580px;height:580px;margin:-290px 0 0 -290px;border-radius:50%;
background:radial-gradient(circle,rgba(120,86,190,.30),rgba(80,60,140,.09) 46%,transparent 67%)}
.dirBg .ring{position:absolute;left:50%;top:46%;border-radius:50%;transform:translate(-50%,-50%);
border:1px solid rgba(240,215,156,.10)}
.dirBg .r1{width:326px;height:326px}
.dirBg .r2{width:418px;height:418px;border-style:dashed;border-color:rgba(143,233,221,.13)}
.dirBg .r3{width:520px;height:520px;border-color:rgba(240,215,156,.055)}
.dirBg .sg{position:absolute;font-size:12px;color:rgba(240,215,156,.24);line-height:1}
.dirBg .rn{position:absolute;font-size:8.5px;color:rgba(143,233,221,.20);letter-spacing:.6px;line-height:1}
.dirTop{position:relative;display:flex;flex-direction:column;gap:5px;
padding:0 2px clamp(10px,2vh,18px)}
.dirTop b{font-size:15px;letter-spacing:5px;color:#f0d79c;font-weight:700;
text-shadow:0 0 14px rgba(240,215,156,.34)}
.dirTop span{font-size:10.5px;color:#8b83a8;letter-spacing:.6px;line-height:1.7}
#view-dir .cats{position:relative;display:flex;flex-direction:column;gap:clamp(8px,1.5vh,13px)}

/* 卡片：单列宽卡，深紫发光 */
.dtc{--pw:clamp(28px,6.6vh,40px);
position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;justify-content:center;
gap:clamp(5px,1.1vh,9px);width:33.33%;margin:0 auto;
padding:clamp(9px,1.5vh,14px) 8px clamp(8px,1.4vh,13px);text-align:center;
border-radius:18px;cursor:pointer;-webkit-tap-highlight-color:transparent;
border:1px solid rgba(240,215,156,.26);
background:linear-gradient(118deg,rgba(66,47,116,.78),rgba(26,21,46,.90) 62%,rgba(18,15,32,.94));
box-shadow:0 8px 22px rgba(0,0,0,.38),inset 0 1px 0 rgba(255,255,255,.05),
inset 0 0 26px rgba(143,233,221,.045);transition:transform .16s ease,border-color .16s ease,box-shadow .16s ease}
.dtc:active{transform:translateY(1px);border-color:rgba(240,215,156,.55);
box-shadow:0 10px 26px rgba(0,0,0,.42),0 0 20px rgba(240,215,156,.16)}

/* 小塔罗牌 */
.dtc .dpp{position:relative;flex:0 0 auto;width:var(--pw);height:calc(var(--pw)*1.55);border-radius:6px;
display:flex;align-items:center;justify-content:center;
background:linear-gradient(165deg,#43316f,#281e4c 55%,#1a1533);
border:1px solid rgba(240,215,156,.5);
box-shadow:0 5px 14px rgba(0,0,0,.5),0 0 14px rgba(240,215,156,.14),
inset 0 0 12px rgba(143,233,221,.09)}
.dtc .dpp::before{content:"";position:absolute;left:4px;top:4px;right:4px;bottom:4px;
border-radius:4px;border:1px solid rgba(240,215,156,.22)}
.dtc .dpp::after{content:"";position:absolute;left:50%;top:8px;bottom:8px;width:1px;margin-left:-.5px;
background:linear-gradient(180deg,transparent,rgba(240,215,156,.16),transparent)}
.dtc .dpp i{position:relative;font-style:normal;font-size:calc(var(--pw)*.40);line-height:1;color:#f0d79c;
text-shadow:0 0 12px rgba(240,215,156,.62);z-index:2}
.dtc .dpp span{position:absolute;left:50%;width:3px;height:3px;margin-left:-1.5px;border-radius:50%;z-index:2}
.dtc .dpp .d1{top:5px;background:#8fe9dd;box-shadow:0 0 6px #8fe9dd}
.dtc .dpp .d2{bottom:5px;background:rgba(240,215,156,.8);box-shadow:0 0 6px rgba(240,215,156,.65)}

/* 文案 */
.dtxc{display:flex;flex-direction:column;gap:5px;min-width:0;width:100%;align-items:center}
.dtxc b{font-size:clamp(13px,2.05vh,15px);letter-spacing:3px;color:#f3e9d2;font-weight:700}

/* 蝴蝶 */
.dtfy{position:absolute;right:4px;top:4px;width:clamp(16px,3.2vh,24px);height:auto;pointer-events:none;
filter:drop-shadow(0 0 6px rgba(240,215,156,.34))}
.dtfy .wl,.dtfy .wr{transform-box:view-box;transform-origin:60px 50px}
.dtfy .wl{animation:dFlapL 3.6s ease-in-out infinite}
.dtfy .wr{animation:dFlapR 3.6s ease-in-out infinite}
@keyframes dFlapL{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.76)}}
@keyframes dFlapR{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.76)}}

/* 备选：同样的三分之一宽窄卡，排成 2×2 */
#view-dir.vg .cats{flex-direction:row;flex-wrap:wrap;justify-content:center;gap:12px}
#view-dir.vg .dtc{flex:0 0 33.33%;width:33.33%;margin:0}
@keyframes dpk{from{opacity:0;transform:translateY(-5px)}to{opacity:1;transform:none}}
.hcard.picked{border-color:rgba(240,215,156,.62);
background:linear-gradient(150deg,rgba(240,215,156,.16),rgba(20,19,36,.96))}
.cta{width:100%;border:none;border-radius:999px;padding:14px 0;font-family:inherit;
font-size:14.5px;letter-spacing:2px;font-weight:700;color:#1a1428;
background:linear-gradient(120deg,#f0d79c,#e0b978);box-shadow:0 10px 26px rgba(240,215,156,.22)}
.cta:active{opacity:.86}
.astroEnt{display:flex;cursor:pointer;align-items:center;justify-content:space-between;gap:10px;
padding:13px 15px;border-radius:12px;text-decoration:none;
border:1px solid rgba(240,215,156,.32);background:linear-gradient(120deg,rgba(240,215,156,.10),rgba(255,255,255,.02))}
.astroEnt{cursor:pointer}
.astroEnt:active{opacity:.85}
.astroEnt .aeL{display:flex;flex-direction:column;gap:4px}
.astroEnt .aeL b{font-size:13.5px;letter-spacing:1.5px;color:#f0d79c;font-weight:700}
.astroEnt .aeL span{font-size:11.5px;letter-spacing:.5px;color:#9c93bd}
.astroEnt .aeR{font-style:normal;color:#f0d79c;font-size:14px}
.aTip{text-align:center;font-size:11.5px;color:#6f6788;letter-spacing:1px;margin:4px 0 2px}

/* ===== 顶部 banner 海报 ===== */
.bnrTop{display:block;position:relative;border-radius:16px;overflow:hidden;line-height:0;
border:1px solid rgba(240,215,156,.22);box-shadow:0 10px 26px rgba(0,0,0,.45);
background:linear-gradient(160deg,#2a1f4d,#141327);text-decoration:none;aspect-ratio:3 / 1}
.bnrTop img{display:block;width:100%;height:100%;object-fit:cover}
/* 背景模糊层：同一张图放大高斯模糊，用来把主图两侧的空白填满，视觉上是同色延续 */
.bnrTop .bnrBg{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;
filter:blur(18px) saturate(1.35) brightness(.95);transform:scale(1.2);transform-origin:center center}
/* 前景主图：完整不裁切，居中显示 */
.bnrTop #bnrImg{position:relative;z-index:1;object-fit:contain}
/* PC 宽屏：贴边铺满整行，高度固定，两侧交给模糊层延展 */
@media (min-width:720px){.bnrTop{aspect-ratio:auto;height:400px}}
.bnrTop .ph{position:absolute;left:0;top:0;right:0;bottom:0;line-height:1.5;
flex-direction:column;align-items:center;justify-content:center;gap:6px;padding:14px;text-align:center}
.bnrTop .ph b{font-size:14px;letter-spacing:2px;color:#f0d79c;font-weight:700}
.bnrTop .ph span{font-size:11.5px;color:#8e86ad;letter-spacing:1px}
.bnrTop:active{opacity:.92}
/* banner 蝴蝶扇翅：底图为无蝴蝶版，左右半翅各自绕中轴开合 */
.bnrTop .bnrFly{position:absolute;left:0;top:0;right:0;bottom:0;pointer-events:none;z-index:2}
.bnrTop .bnrFly .wl,.bnrTop .bnrFly .wr{position:absolute;left:0;top:0;transform-origin:50% 50%;
will-change:transform;backface-visibility:hidden}
.bnrTop .bnrFly .wl img,.bnrTop .bnrFly .wr img{display:block;width:100%;height:100%;object-fit:fill}
.bnrTop .bnrFly .wl{transform-origin:100% 50%;animation:bnrFlapL 10s ease-in-out .3s infinite}
.bnrTop .bnrFly .wr{transform-origin:0% 50%;animation:bnrFlapR 10s ease-in-out .3s infinite}
@keyframes bnrFlapL{
0%,1%{transform:scaleX(1) rotate(0deg);filter:brightness(1)}
4%{transform:scaleX(.60) rotate(-1.1deg);filter:brightness(.9)}
7.5%{transform:scaleX(.94) rotate(0deg);filter:brightness(.98)}
9.5%{transform:scaleX(.72) rotate(-.5deg);filter:brightness(.93)}
14%,100%{transform:scaleX(1) rotate(0deg);filter:brightness(1)}
}
@keyframes bnrFlapR{
0%,1%{transform:scaleX(1) rotate(0deg);filter:brightness(1)}
4%{transform:scaleX(.60) rotate(1.1deg);filter:brightness(.9)}
7.5%{transform:scaleX(.94) rotate(0deg);filter:brightness(.98)}
9.5%{transform:scaleX(.72) rotate(.5deg);filter:brightness(.93)}
14%,100%{transform:scaleX(1) rotate(0deg);filter:brightness(1)}
}
@media (prefers-reduced-motion:reduce){
.bnrTop .bnrFly .wl,.bnrTop .bnrFly .wr{animation:none}
}

/* ===== 每日塔罗 ===== */
#view-daily{display:flex;flex-direction:column;flex:1;min-height:0;overflow-y:auto;padding:0 14px 22px}
.dlyTop{text-align:center;margin-top:2px}
.dlyTop b{display:block;font-size:15px;letter-spacing:7px;color:#8fe9dd;font-weight:700;
text-shadow:0 0 18px rgba(127,233,220,.42)}
.dlyTop span{display:block;margin-top:8px;font-size:11.5px;color:#8b83a8;letter-spacing:.8px}
.dlyStage{position:relative;display:flex;align-items:center;justify-content:center;height:290px;margin-top:4px}
.dlyHalo{position:absolute;width:228px;height:228px;border-radius:50%;pointer-events:none;
background:radial-gradient(circle,rgba(127,233,220,.2) 0%,rgba(96,126,220,.11) 45%,transparent 73%);
animation:ansPulse 4.8s ease-in-out infinite}
.dlyRing{position:absolute;border-radius:50%;border:1px dashed rgba(240,215,156,.15);pointer-events:none}
.dlyRing.r1{width:252px;height:252px;animation:ansSpin 36s linear infinite}
.dlyRing.r2{width:196px;height:196px;border-color:rgba(127,233,220,.15);
animation:ansSpin 23s linear infinite reverse}
.dlyCardWrap{position:relative;width:148px;height:246px;perspective:900px;transform-style:preserve-3d}
.dlyBack,.dlyFace{position:absolute;left:0;top:0;width:100%;height:100%;border-radius:13px;
-webkit-backface-visibility:hidden;backface-visibility:hidden;
transition:transform .58s cubic-bezier(.3,1.3,.5,1),opacity .34s ease}
.dlyBack{display:flex;align-items:center;justify-content:center;
border:1px solid rgba(240,215,156,.45);box-shadow:0 12px 30px rgba(0,0,0,.55),inset 0 0 36px rgba(127,233,220,.13);
background:
repeating-linear-gradient(45deg,rgba(240,215,156,.05) 0 2px,transparent 2px 9px),
radial-gradient(120% 90% at 50% 16%,rgba(127,233,220,.17),transparent 62%),
linear-gradient(160deg,#2c2152,#191332 62%,#120f24)}
.dlyBack i{font-style:normal;font-size:34px;line-height:1;color:#f0d79c;
text-shadow:0 0 20px rgba(240,215,156,.55)}
.dlyBack em{position:absolute;left:0;right:0;bottom:18px;text-align:center;font-style:normal;
font-size:9.5px;letter-spacing:3.5px;color:rgba(240,215,156,.55)}
.dlyFace{opacity:0;transform:rotateY(180deg)}
.dlyFace img{display:block;width:100%;height:100%;border-radius:13px;object-fit:cover;
box-shadow:0 12px 30px rgba(0,0,0,.55)}
.dlyCardWrap.rev .dlyFace img{transform:rotate(180deg)}
.dlyCardWrap.open .dlyBack{transform:rotateY(-180deg);opacity:0}
.dlyCardWrap.open .dlyFace{opacity:1;transform:rotateY(0)}
.dlyCardWrap.shake{animation:dlyShake .62s ease}
@keyframes dlyShake{0%,100%{transform:translateY(0) rotate(0)}
25%{transform:translateY(-10px) rotate(-2.4deg)}55%{transform:translateY(4px) rotate(2.2deg)}
78%{transform:translateY(-3px) rotate(-1deg)}}
.dlyAsk{margin-top:10px;text-align:center}
.dlyAsk b{display:block;font-size:13px;letter-spacing:2px;color:#eae4f6;font-weight:700}
.dlyAsk span{display:block;margin-top:8px;font-size:11.5px;line-height:1.85;color:#8b83a8}
.dlyBtn{margin-top:14px}
.dlyRes{display:none;width:100%;margin-top:15px}
.dlyName{text-align:center;font-size:19px;letter-spacing:3px;color:#f0d79c;font-weight:700;
text-shadow:0 0 16px rgba(240,215,156,.35)}
.dlyPos{text-align:center;margin-top:9px}
.dlyPos em{display:inline-block;font-style:normal;font-size:11px;letter-spacing:2px;padding:4px 13px;
border-radius:999px;border:1px solid rgba(127,233,220,.4);color:#8fe9dd;background:rgba(127,233,220,.09)}
.dlyPos em.neg{border-color:rgba(232,160,180,.42);color:#f0b7c6;background:rgba(232,160,180,.1)}
.dlyKw{text-align:center;margin-top:11px;font-size:12px;line-height:1.9;color:#9c93bd;letter-spacing:.6px}
.dlySec{margin-top:13px;padding:14px 15px;border-radius:13px;
border:1px solid rgba(240,215,156,.16);
background:linear-gradient(150deg,rgba(52,39,92,.72),rgba(22,20,40,.82))}
.dlySec h4{margin:0 0 8px;font-size:11.5px;letter-spacing:2.4px;color:#8fe9dd;font-weight:700}
.dlySec p{margin:0;font-size:14.6px;line-height:1.95;color:#f2eefb;letter-spacing:.4px}
.dlyFoot{margin:18px 0 4px;text-align:center;font-size:11px;color:#6f6788;letter-spacing:1px}

/* ===== 首页板块化布局 ===== */
.hboard{display:flex;flex-direction:column;gap:11px}
.hrow{display:flex;gap:11px;align-items:stretch;height:132px}
.hrow>.hcard{flex:1 1 0;min-width:0}
.hrow>.bnr{flex:1.12 1 0;min-width:0}
.hcard{position:relative;display:flex;flex-direction:column;justify-content:center;gap:7px;
padding:13px;border-radius:14px;cursor:pointer;overflow:hidden;min-height:112px;
border:1px solid rgba(240,215,156,.26);text-decoration:none;
background:linear-gradient(150deg,rgba(52,38,92,.92),rgba(18,17,34,.96));
box-shadow:0 7px 18px rgba(0,0,0,.34)}
.hcard:active{opacity:.88}
.hcard .hi{font-size:18px;line-height:1}
.hcard b{display:block;font-size:13.5px;letter-spacing:1.6px;color:#f0d79c;font-weight:700;margin:0}
.hcard span{display:block;font-size:10.8px;line-height:1.55;color:#9c93bd;margin-top:4px;letter-spacing:.3px}
.hcard .ha{position:absolute;right:11px;top:11px;font-size:13px;color:#f0d79c;opacity:.7}
.hcard.gold{background:linear-gradient(150deg,#f4e2b4,#dcb473);border-color:rgba(255,255,255,.42)}
.hcard.gold .hi,.hcard.gold b,.hcard.gold .ha{color:#241a45}
.hcard.gold span{color:rgba(36,26,69,.68)}
.hsec{display:flex;align-items:baseline;justify-content:space-between;margin:7px 2px 0}
.hsec b{font-size:12px;letter-spacing:2.5px;color:#c9b98d;font-weight:600}
.hsec span{font-size:10.5px;color:#6f6788;letter-spacing:.5px}
.cats{display:grid;grid-template-columns:1fr 1fr;gap:9px}
.cat{display:flex;align-items:center;gap:9px;padding:11px 12px;border-radius:12px;cursor:pointer;
border:1px solid rgba(240,215,156,.22);
background:linear-gradient(120deg,rgba(240,215,156,.10),rgba(255,255,255,.02))}
.cat:active{background:rgba(240,215,156,.18)}
.cat i{font-style:normal;font-size:17px;line-height:1}
.cat .ct b{display:block;font-size:12.5px;color:#ece2c8;letter-spacing:1.2px;font-weight:600}
.cat .ct em{display:block;font-style:normal;font-size:10px;color:#8b83a8;margin-top:2px;letter-spacing:.3px}
/* 抽牌台分类条 */
.dcats{display:flex;gap:7px;overflow-x:auto;padding:2px 14px 9px;flex:0 0 auto}
.dcats::-webkit-scrollbar{display:none}
.dcat{flex:0 0 auto;padding:6px 13px;border-radius:999px;font-size:11.5px;letter-spacing:1px;cursor:pointer;
color:#9c93bd;border:1px solid rgba(240,215,156,.22);background:rgba(255,255,255,.03)}
.dcat.on{color:#1a1428;font-weight:700;border-color:transparent;
background:linear-gradient(120deg,#f0d79c,#e0b978)}
.dcatTip{font-size:11px;color:#8b83a8;text-align:center;letter-spacing:.5px;padding:0 14px 6px;line-height:1.7;flex:0 0 auto}
/* 星盘档案 */
.aFormTop{display:flex;align-items:center;justify-content:space-between;
border-bottom:1px dashed rgba(240,215,156,.2);padding-bottom:10px}
.aFormTop b{font-size:13px;color:#f0d79c;letter-spacing:1.5px;font-weight:600}
.aFormTop span{font-size:12px;color:#8e86ad;letter-spacing:1px;cursor:pointer;padding:2px 4px}
#aName{width:100%;box-sizing:border-box;background:rgba(0,0,0,.32);
border:1px solid rgba(255,255,255,.12);border-radius:9px;padding:11px 12px;
color:#eae6f5;font-family:inherit;font-size:13.5px;letter-spacing:.5px}
#aName::placeholder{color:#5d5680}
.archBox{display:flex;flex-direction:column;gap:9px}
.archItem{display:flex;align-items:center;gap:10px;padding:12px 13px;border-radius:12px;cursor:pointer;
border:1px solid rgba(240,215,156,.22);
background:linear-gradient(150deg,rgba(42,31,77,.82),rgba(19,18,36,.92))}
.archItem:active{opacity:.86}
.archItem .ail{flex:1;min-width:0}
.archItem .ail b{display:block;font-size:13px;color:#f0d79c;letter-spacing:.8px}
.archItem .ail span{display:block;font-size:10.8px;color:#9c93bd;margin-top:3px;letter-spacing:.3px}
.archItem .aigo{font-size:12.5px;color:#f0d79c;opacity:.8;white-space:nowrap}
.archItem .ail em{font-style:normal}
.archItem .archDel{background:transparent;border:none;color:#6f6788;font-size:11px;
letter-spacing:1px;padding:5px 3px;font-family:inherit;cursor:pointer}
.archItem .archDel:active{color:#e08a8a}
.aEmpty{font-size:12px;color:#7d759a;line-height:1.9;text-align:center;padding:16px 10px;letter-spacing:.6px}
.aspTable th{font-size:10.5px;color:#8e86ad;font-weight:400;letter-spacing:1px;
padding:0 4px 5px;border-bottom:1px solid rgba(240,215,156,.2);text-align:left}
.aBtns{display:flex;gap:9px;justify-content:center;flex-wrap:wrap}
.aBtns .aAgain{align-self:auto;flex:1;min-width:0}
.aAgain.ghost{border-color:rgba(255,255,255,.16);color:#9c93bd}
#aArchWrap{display:flex;flex-direction:column;gap:11px}
.archDel{background:transparent;border:none;color:#6f6788;font-size:15px;line-height:1;
padding:5px 4px;font-family:inherit;cursor:pointer}
.aAdd{width:100%;padding:12px;border-radius:12px;cursor:pointer;
border:1px dashed rgba(240,215,156,.42);background:rgba(240,215,156,.06);
color:#f0d79c;font-family:inherit;font-size:12.5px;letter-spacing:1.5px}
.aAdd:active{background:rgba(240,215,156,.14)}
/* 相位表 */
.aspTable{width:100%;border-collapse:collapse;font-size:11.5px;margin:0 0 4px}
.aspTable td{padding:5px 4px;border-bottom:1px solid rgba(255,255,255,.06);color:#c9c2e0;letter-spacing:.3px}
.aspTable td:last-child{text-align:right;color:#8e86ad;white-space:nowrap}
.aspLegend{display:flex;flex-wrap:wrap;gap:9px;font-size:10.5px;color:#8e86ad;margin:0 0 6px}
.aspLegend i{font-style:normal;color:#d8cda9}
.aCard{border:1px solid rgba(240,215,156,.20);border-radius:14px;padding:15px;
background:linear-gradient(160deg,rgba(42,31,77,.85),rgba(20,19,39,.9));
display:flex;flex-direction:column;gap:12px}
.aField{display:flex;flex-direction:column;gap:7px}
.aField label{font-size:12px;color:#9c93bd;letter-spacing:1px}
.aIns{display:flex;gap:8px}
.aIns input{flex:1;min-width:0;background:rgba(0,0,0,.32);border:1px solid rgba(255,255,255,.12);
border-radius:9px;padding:10px 8px;color:#eae6f5;font-family:inherit;font-size:13px;text-align:center}
.aIns input:disabled{opacity:.35}
.aIns input::placeholder{color:#5d5680}
.aPick{display:flex;align-items:center;justify-content:space-between;gap:8px;width:100%;
background:rgba(0,0,0,.32);border:1px solid rgba(255,255,255,.12);border-radius:9px;
padding:12px 12px;color:#eae6f5;font-family:inherit;font-size:13.5px;letter-spacing:.5px;text-align:left}
.aPick i{font-style:normal;color:#7a5cc4;font-size:16px;line-height:1}
.aPick:active{background:rgba(0,0,0,.45)}
.aPick.off{opacity:.4}
.aPick .ph{color:#5d5680}
.pkMask{position:fixed;left:0;top:0;right:0;bottom:0;background:rgba(4,6,14,.62);
opacity:0;pointer-events:none;transition:.2s;z-index:120}
.pkMask.show{opacity:1;pointer-events:auto}
.pkSheet{position:absolute;left:0;right:0;bottom:0;border-radius:16px 16px 0 0;
border-top:1px solid rgba(240,215,156,.28);
background:linear-gradient(170deg,#241a45,#120f1f);padding:0 0 14px;
transform:translateY(18px);transition:.22s}
.pkMask.show .pkSheet{transform:none}
.pkBar{display:flex;align-items:center;justify-content:space-between;padding:13px 16px 4px}
.pkBar b{font-size:12.5px;color:#9c93bd;letter-spacing:2px;font-weight:400}
.pkBar span{font-size:13px;letter-spacing:1px;padding:4px 4px;cursor:pointer}
.pkCancel{color:#8e86ad}
.pkOk{color:#f0d79c}
.pkWrap{position:relative;display:flex;height:220px;overflow:hidden}
.pkWrap:before,.pkWrap:after{content:"";position:absolute;left:0;right:0;height:62px;pointer-events:none;z-index:3}
.pkWrap:before{top:0;background:linear-gradient(#241a45,rgba(36,26,69,0))}
.pkWrap:after{bottom:0;background:linear-gradient(rgba(18,15,31,0),#120f1f)}
.pkSel{position:absolute;left:10px;right:10px;top:50%;margin-top:-22px;height:44px;
pointer-events:none;z-index:2;border-radius:9px;background:rgba(240,215,156,.055);
border-top:1px solid rgba(240,215,156,.20);border-bottom:1px solid rgba(240,215,156,.20)}
.pkCol{flex:1;min-width:0;height:220px;overflow-y:auto;overflow-x:hidden;
scroll-snap-type:y mandatory;-webkit-overflow-scrolling:touch;
padding:88px 0;box-sizing:border-box;scrollbar-width:none;touch-action:pan-y;position:relative;z-index:1}
.pkCol::-webkit-scrollbar{display:none}
.pkItem{height:44px;line-height:44px;text-align:center;font-size:15px;color:#8e86ad;
letter-spacing:.4px;scroll-snap-align:center;white-space:nowrap;overflow:hidden;
text-overflow:ellipsis;transition:color .12s}
.pkItem.on{color:#f0d79c;font-weight:600}
.aChk{display:flex;align-items:center;gap:7px;font-size:12px;color:#9c93bd;letter-spacing:.5px}
.aChk input{width:15px;height:15px;accent-color:#f0d79c}
.aErr{font-size:12px;color:#e08a8a;text-align:center;min-height:14px;letter-spacing:.5px}
.aRes{gap:14px}
.aBadge{align-self:center;font-size:11px;letter-spacing:2px;color:#1a1428;padding:4px 12px;
border-radius:999px;background:linear-gradient(120deg,#f0d79c,#e0b978)}
.aMain{display:flex;flex-direction:column;gap:6px;border-bottom:1px dashed rgba(240,215,156,.22);padding-bottom:12px}
.aLn{display:flex;justify-content:space-between;font-size:12.5px;color:#9c93bd;letter-spacing:.5px}
.aLn b{color:#f0d79c;font-weight:600}
.aSec h4{margin:0 0 7px;font-size:12px;color:#f0d79c;letter-spacing:2px;font-weight:600}
.aSec p{margin:0 0 6px;font-size:12.5px;line-height:1.85;color:#c9c2e0;letter-spacing:.4px}
.aNo{font-size:11.5px;color:#8a8299;line-height:1.7;border-top:1px dashed rgba(255,255,255,.10);padding-top:10px}
.aAgain{align-self:center;background:transparent;border:1px solid rgba(240,215,156,.3);color:#f0d79c;
border-radius:999px;padding:8px 22px;font-family:inherit;font-size:12px;letter-spacing:1.5px}
.aFoot{text-align:center;font-size:11px;color:#5d5680;letter-spacing:1px;line-height:1.8;margin:10px 0 4px}
#view-astro{flex-direction:column;gap:12px;padding-top:12px;overflow-y:auto;flex:1 1 0%;min-height:0}
#view-astro::-webkit-scrollbar{width:0;height:0}
#aResult{flex-direction:column;align-items:stretch;gap:12px;width:100%}
#aResult>*{min-width:0}
/* ==================== 星象卡牌（星盘结果页） ==================== */
.apTop{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:0 2px}
.apWho{display:flex;flex-direction:column;gap:5px;min-width:0;flex:1}
.apName{display:flex;align-items:center;gap:7px;flex-wrap:wrap;font-size:16px;color:#f0d79c;
letter-spacing:.6px;font-weight:600;line-height:1.3}
.apName .apSg{font-size:10.5px;color:#1a1428;background:linear-gradient(120deg,#f0d79c,#e0b978);
border-radius:999px;padding:2px 9px;letter-spacing:1px;font-weight:700}
.apName .apBd{font-size:11px;color:#8e86ad;letter-spacing:.6px;font-weight:400}
.apMe{flex:0 0 auto;display:flex;align-items:center;gap:5px;font-size:11px;color:#e2cf9d;
border:1px solid rgba(240,215,156,.26);border-radius:999px;padding:7px 11px;
background:rgba(240,215,156,.07);font-family:inherit;letter-spacing:.8px;cursor:pointer}
.apMe:active{background:rgba(240,215,156,.18)}
.apMe i{font-style:normal;font-size:12px;line-height:1}
.apGrid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.apCard{position:relative;display:flex;flex-direction:column;align-items:center;gap:5px;
border-radius:13px;padding:12px 6px 11px;text-align:center;overflow:hidden;cursor:pointer;
border:1px solid rgba(240,215,156,.18);
background:linear-gradient(165deg,rgba(52,38,92,.92),rgba(19,18,36,.95))}
.apCard:active{transform:scale(.972)}
.apCard .apSym{width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;
font-size:17px;color:#fff;line-height:1;letter-spacing:0;
background:radial-gradient(circle at 32% 26%,rgba(255,255,255,.5),rgba(255,255,255,0) 58%),
linear-gradient(140deg,var(--c1,#6d5aa8),var(--c2,#2a2350));
box-shadow:0 0 13px rgba(240,215,156,.14)}
.apCard .apSym.asc{font-size:9.5px;letter-spacing:.5px;font-weight:700}
.apCard .apPn{font-size:10.5px;color:#9c93bd;letter-spacing:1.2px;margin-top:1px}
.apCard .apSgn{font-size:13px;color:#f2ead6;letter-spacing:1.2px;font-weight:600}
.apCard .apTag{max-width:100%;font-size:9.8px;line-height:1.5;color:#d7c79c;
padding:2px 7px;border-radius:999px;background:rgba(240,215,156,.10);
letter-spacing:.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.apCard .apDeg{position:absolute;right:6px;top:5px;font-size:8.5px;color:#5d5680;letter-spacing:0}
.apCard .apRetro{position:absolute;left:6px;top:5px;font-size:8.5px;color:#c98b3f}
.apCard .apHs{display:block;font-size:8.8px;color:#8b81b4;letter-spacing:.5px;margin-top:-1px}
.apCard:active .apHs{color:#f0d79c}
.plSheet .plHead{display:flex;align-items:center;gap:11px}
.plSheet .plSym{flex:0 0 auto;width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;
font-size:18px;color:#fff;line-height:1;letter-spacing:0;
background:radial-gradient(circle at 32% 26%,rgba(255,255,255,.5),rgba(255,255,255,0) 58%),
linear-gradient(140deg,var(--c1,#6d5aa8),var(--c2,#2a2350));
box-shadow:0 0 14px rgba(240,215,156,.16)}
.plSheet .plSym.asc{font-size:10.5px;font-weight:700;letter-spacing:.5px}
.plSheet .plName{font-size:13px;color:#f2ead6;font-weight:600;letter-spacing:1px}
.plSheet .plSub{font-size:9.8px;color:#9c93bd;letter-spacing:.4px;margin-top:3px}
.plSheet .plMotto{margin-left:auto;flex:0 0 auto;font-size:9.5px;color:#d7c79c;letter-spacing:1.2px;font-style:italic}
.plSheet .plH{display:inline-flex;align-items:center;font-size:10.5px;color:#f0d79c;letter-spacing:1.1px;
padding:4px 11px;border-radius:999px;background:rgba(240,215,156,.10);border:1px solid rgba(240,215,156,.22)}
.plSheet .plSec{font-size:9.8px;color:#8e86ad;letter-spacing:1.7px;margin:15px 0 6px;padding-left:1px}
.plSheet .plP{font-size:12px;line-height:1.95;color:rgba(232,223,246,.87);letter-spacing:.35px}
.apDet{display:flex;flex-direction:column;gap:8px;border-radius:14px;padding:13px 14px;
border:1px solid rgba(240,215,156,.18);
background:linear-gradient(160deg,rgba(42,31,77,.85),rgba(20,19,39,.9))}
.apDetTop{display:flex;align-items:center;gap:8px}
.apDetTop b{font-size:13px;color:#f0d79c;letter-spacing:1.4px;font-weight:600}
.apDetTop i{font-style:normal;font-size:9.5px;color:#1a1428;background:linear-gradient(120deg,#efd69b,#ddb877);
border-radius:4px;padding:1.5px 6px;letter-spacing:.7px;font-weight:700}
.apDet p{margin:0;font-size:12.5px;line-height:1.92;color:#c9c2e0;letter-spacing:.3px}
.apDet .apM{padding-top:8px;border-top:1px dashed rgba(240,215,156,.16)}
.apMoreBtn{align-self:flex-end;background:none;border:none;font-family:inherit;cursor:pointer;
font-size:11px;color:#f0d79c;letter-spacing:1.2px;padding:2px 0;opacity:.85}
.apChartBtn{width:100%;display:flex;align-items:center;justify-content:center;gap:8px;
padding:13px;border-radius:13px;cursor:pointer;font-family:inherit;font-size:12.5px;
letter-spacing:2px;color:#f0d79c;border:1px solid rgba(240,215,156,.3);
background:linear-gradient(120deg,rgba(240,215,156,.14),rgba(240,215,156,.05))}
.apChartBtn:active{background:rgba(240,215,156,.24)}
.apChartBtn i{font-style:normal;font-size:14px;line-height:1}
.chartMask{position:fixed;left:0;top:0;right:0;bottom:0;z-index:140;background:rgba(4,6,14,.78);
display:flex;align-items:center;justify-content:center;padding:16px;
opacity:0;pointer-events:none;transition:.2s}
.chartMask.show{opacity:1;pointer-events:auto}
.chartSheet{position:relative;width:100%;max-width:430px;max-height:88vh;overflow-y:auto;
border-radius:16px;padding:16px 14px 18px;border:1px solid rgba(240,215,156,.26);
background:linear-gradient(170deg,#241a45,#120f1f);display:flex;flex-direction:column;gap:12px}
.chartSheet .csTop{display:flex;align-items:center;justify-content:space-between}
.chartSheet .csTop b{font-size:12.5px;color:#f0d79c;letter-spacing:2px}
.chartSheet .csTop span{font-size:16px;color:#8e86ad;line-height:1;padding:2px 6px;cursor:pointer}
.chartSheet .csSvg{display:flex;justify-content:center}
.chartSheet .csPl{font-size:10.5px;line-height:2;color:rgba(230,220,245,.62);letter-spacing:.2px}
.chartSheet .csSec{font-size:10px;color:#8e86ad;letter-spacing:1.6px;margin:12px 0 3px;padding-left:1px}
.chartSheet .csSec:first-of-type{margin-top:10px}
.chartSheet .csPos td{padding:5px 4px}
.chartSheet .csPos td:nth-child(2){color:#e3dbc9}
.chartSheet .csPos .rR{font-size:8.5px;color:#c98b3f;margin-left:2px;vertical-align:1px}
/* 切换档案浮层 */
.archPickSheet{gap:10px;max-height:78vh}
.archPickSheet .archBox{max-height:54vh;overflow-y:auto;padding-right:2px}
.archPickSheet .archItem.isCur{border-color:rgba(240,215,156,.6);
background:linear-gradient(150deg,rgba(240,215,156,.16),rgba(19,18,36,.92))}
.archPickSheet .archItem.isCur .ail b::after{content:"当前";font-size:8.5px;color:#1a1428;
background:linear-gradient(120deg,#f0d79c,#e0b978);border-radius:999px;padding:1px 6px;
margin-left:6px;letter-spacing:.5px;vertical-align:2px;font-weight:700}
.apPickMore{align-self:center;background:none;border:none;font-family:inherit;cursor:pointer;
font-size:11px;color:#f0d79c;letter-spacing:1.2px;padding:2px 0;opacity:.85}
/* ==================== 今日运势 ==================== */
#view-fortune{flex-direction:column;gap:12px;padding:12px 14px 24px;flex:1;min-height:0;overflow-y:auto}
.zBar{display:flex;align-items:center;gap:1px;margin-top:10px;padding:9px 5px 7px;border-radius:13px;background:rgba(255,255,255,.035);border:1px solid rgba(240,215,156,.14)}
.zBar .zI{flex:1 1 0;min-width:0;text-align:center;line-height:1;transition:transform .2s,color .2s}
.zBar .zI i{font-style:normal;font-size:14.5px;color:#4d466c;font-family:"Segoe UI Symbol","Segoe UI",sans-serif}
.zBar .zI.cur i{color:#f0d79c;font-size:16px;text-shadow:0 0 9px rgba(240,215,156,.6)}
.zBar .zI.cur{transform:translateY(-1px)}
#fBody{display:flex;flex-direction:column;gap:12px}
.fWho{display:flex;flex-direction:column;gap:5px;text-align:center;padding:2px 0 2px}
.fWhoRow{display:flex;align-items:center;gap:10px;position:relative}
.fWhoRow .fWho{flex:1;min-width:0}
.fWhoRow .fSw{flex:0 0 auto;font-size:10px;padding:3px 7px;border:1px solid rgba(240,215,156,.22);
border-radius:999px;text-decoration:none;letter-spacing:.6px}
@media (min-width:720px){
  .fWhoRow{justify-content:center}
  .fWhoRow .fWho{flex:0 1 520px}
  .fWhoRow .fSw{position:absolute;right:0;top:50%;transform:translateY(-50%)}
}
.fWho b{font-size:14px;color:#f0d79c;letter-spacing:1.5px}
.fWho span{font-size:11px;color:#8e86ad;letter-spacing:.6px}
.fSwRow{display:flex;justify-content:center;margin-top:-4px}
.fSw{background:transparent;border:none;color:#7d759a;font-family:inherit;font-size:10.5px;
letter-spacing:1.2px;padding:2px 6px;cursor:pointer;text-decoration:underline;text-underline-offset:3px}
.fSw:active{color:#f0d79c}
.fNav{display:flex;align-items:center;justify-content:space-between;gap:10px;
border:1px solid rgba(240,215,156,.18);border-radius:12px;padding:8px 10px;
background:linear-gradient(150deg,rgba(42,31,77,.8),rgba(19,18,36,.9))}
.fArr{width:30px;height:30px;border-radius:50%;border:1px solid rgba(240,215,156,.25);
background:rgba(240,215,156,.06);color:#f0d79c;font-family:inherit;font-size:15px;line-height:1;cursor:pointer}
.fArr:disabled{opacity:.28}
.fArr:active{background:rgba(240,215,156,.18)}
.fNavMid{display:flex;flex-direction:column;align-items:center;gap:3px;flex:1}
.fNavMid b{font-size:13px;color:#eae4f6;letter-spacing:1.2px}
.fNavMid em{font-style:normal;font-size:10.5px;color:#8e86ad;letter-spacing:1px}
.fNavMid em.now{color:#f0d79c}
.fHero{position:relative;border:1px solid rgba(240,215,156,.22);border-radius:16px;
padding:16px 14px;display:flex;align-items:center;gap:15px;overflow:hidden;
background:radial-gradient(120% 140% at 0% 0%,rgba(240,215,156,.14),rgba(30,24,54,.94) 55%,rgba(16,14,28,.96))}
.fScoreW{display:flex;flex-direction:column;align-items:center;gap:3px;min-width:78px}
.fScore{font-size:44px;font-weight:700;line-height:1;color:#f0d79c;
text-shadow:0 0 22px rgba(240,215,156,.45);font-variant-numeric:tabular-nums}
.fSl{font-size:10px;letter-spacing:2px;color:#9c93bd}
.fHeroR{flex:1;min-width:0;display:flex;flex-direction:column;gap:7px}
.fStarBox{position:relative;display:inline-block;font-size:14px;line-height:1;letter-spacing:1px}
.fStarBg{color:rgba(255,255,255,.16)}
.fStarFg{position:absolute;left:0;top:0;overflow:hidden;white-space:nowrap;color:#f0d79c;
text-shadow:0 0 10px rgba(240,215,156,.5);letter-spacing:1px}
.fTag{align-self:flex-start;font-size:10.5px;letter-spacing:1.5px;padding:3px 10px;border-radius:999px}
.fTag.lv1{color:#0f1a14;background:linear-gradient(120deg,#8fe0b0,#5fc9a0)}
.fTag.lv2{color:#1a1428;background:linear-gradient(120deg,#f0d79c,#e0b978)}
.fTag.lv3{color:#12101f;background:linear-gradient(120deg,#cfc6ea,#a99bcf)}
.fTag.lv4{color:#1d1420;background:linear-gradient(120deg,#e8b3a0,#d08a7c)}
.fTag.lv5{color:#f3eef7;background:linear-gradient(120deg,#6d6490,#4a4468)}
.fHeadline{font-size:11.8px;color:#c9c2e0;line-height:1.7;letter-spacing:.4px}
.fCard{border:1px solid rgba(240,215,156,.20);border-radius:14px;padding:14px;
background:linear-gradient(160deg,rgba(42,31,77,.85),rgba(20,19,39,.9));display:flex;flex-direction:column;gap:11px}
.fCardT{display:flex;align-items:baseline;justify-content:space-between;gap:8px}
.fCardT b{font-size:12.5px;color:#f0d79c;letter-spacing:2px}
.fCardT span{font-size:10px;color:#7d759a;letter-spacing:.6px}
.fDim{display:flex;align-items:center;gap:9px}
.fDimN{width:34px;font-size:11.5px;color:#9c93bd;letter-spacing:.6px;flex:0 0 auto}
.fDimBar{flex:1;height:6px;border-radius:999px;background:rgba(255,255,255,.09);overflow:hidden}
.fDimBar i{display:block;height:100%;border-radius:999px;transition:width .5s}
.fDim.hi .fDimBar i{background:linear-gradient(90deg,#f0d79c,#e8a0b8)}
.fDim.mid .fDimBar i{background:linear-gradient(90deg,#a99bcf,#8f7fd0)}
.fDim.low .fDimBar i{background:linear-gradient(90deg,#6d6490,#5a5478)}
.fDimV{width:26px;text-align:right;font-size:11.5px;color:#c9c2e0;font-variant-numeric:tabular-nums}
.fLucky{display:flex;gap:9px}
.fLk{flex:1;border:1px solid rgba(240,215,156,.18);border-radius:12px;padding:10px 8px;
display:flex;flex-direction:column;align-items:center;gap:5px;
background:linear-gradient(160deg,rgba(42,31,77,.7),rgba(18,17,33,.9))}
.fLk em{font-style:normal;font-size:10px;color:#8e86ad;letter-spacing:1px}
.fLk b{font-size:13px;color:#f0d79c;letter-spacing:1px}
.fLk .fDot{width:14px;height:14px;border-radius:50%;box-shadow:0 0 0 3px rgba(255,255,255,.06)}
.fP{font-size:12px;line-height:1.9;color:#c9c2e0;letter-spacing:.4px;margin:0}
.fSecBlock{display:flex;flex-direction:column;gap:6px;border-top:1px dashed rgba(240,215,156,.18);padding-top:10px}
.fSecBlock b{font-size:11.5px;color:#f0d79c;letter-spacing:2px}
.fWarn{border:1px solid rgba(232,160,184,.28);border-radius:14px;padding:12px 14px;
background:linear-gradient(160deg,rgba(60,30,54,.6),rgba(22,17,34,.9));display:flex;flex-direction:column;gap:6px}
.fWarn b{font-size:11px;color:#e8a0b8;letter-spacing:2px}
.fWarn p{font-size:12px;line-height:1.85;color:#d8cfe4;letter-spacing:.4px;margin:0}
.fCrys{width:100%;border:1px solid rgba(240,215,156,.3);border-radius:12px;padding:11px;
background:rgba(240,215,156,.06);color:#f0d79c;font-family:inherit;font-size:12.5px;
letter-spacing:1.5px;cursor:pointer}
.fCrys:active{background:rgba(240,215,156,.16)}
.fCrysBody{border:1px solid rgba(240,215,156,.2);border-radius:12px;padding:12px;
background:linear-gradient(160deg,rgba(42,31,77,.8),rgba(18,17,33,.9));
font-size:12px;line-height:1.85;color:#c9c2e0}
.fCrysBody b{color:#f0d79c;letter-spacing:1px}
.fEmptyCard{border:1px solid rgba(240,215,156,.24);border-radius:14px;padding:18px 14px;
display:flex;flex-direction:column;align-items:center;gap:11px;text-align:center;
background:linear-gradient(160deg,rgba(42,31,77,.85),rgba(19,18,36,.92))}
.fEmptyCard b{font-size:13px;color:#f0d79c;letter-spacing:1.5px}
.fEmptyCard span{font-size:11.5px;color:#9c93bd;line-height:1.8;letter-spacing:.4px}
@media (max-width:360px){
  .brand{font-size:15px;letter-spacing:2px}
  .hrow{height:120px}
  .hcard b{font-size:12.5px}
}
/* ===== 首页六入口宫格：H5 两列 / 宽屏一行六个 ===== */
.hgrid{display:flex;flex-wrap:wrap;gap:9px}
.hgrid>.hcard{flex:1 1 calc(50% - 5px);min-width:0;min-height:82px;padding:12px 8px;
align-items:center;justify-content:center;text-align:center;gap:7px}
.hgrid>.hcard .hi{font-size:19px}
.hgrid>.hcard b{font-size:13px;letter-spacing:1.2px;text-align:center}
.hgrid>.hcard .ha{display:none}
@media (min-width:720px){
  .hgrid>.hcard{flex:1 1 calc(16.6667% - 8px);min-height:86px}
  .hgrid>.hcard b{font-size:12px;letter-spacing:.6px}
  .hgrid>.hcard .hi{font-size:20px}
}
/* ===== 今日运气 + 六项运势 合并为一行双栏 ===== */
.fHeroCard{border:1px solid rgba(240,215,156,.22);border-radius:16px;padding:13px 12px;
display:flex;flex-direction:column;gap:10px;overflow:hidden;
background:radial-gradient(120% 140% at 0% 0%,rgba(240,215,156,.14),rgba(30,24,54,.94) 55%,rgba(16,14,28,.96))}
.fHeroTop{display:flex;align-items:center;gap:12px}
.fHeroTop .fScoreW{min-width:58px;gap:2px}
.fHeroTop .fScore{font-size:37px}
.fHeroTop .fSl{font-size:9.5px;letter-spacing:1.6px}
.fHeroTop .fStarBox{font-size:10px;letter-spacing:0}
.fDims{flex:1;min-width:0;display:flex;flex-direction:column;gap:6px}
.fDims .fDim{gap:7px}
.fDims .fDimN{width:30px;font-size:11px}
.fDims .fDimV{width:22px;font-size:11px}
.fDims .fDimBar{height:5px}
.fHeroBot{display:flex;align-items:center;gap:8px;
border-top:1px dashed rgba(240,215,156,.18);padding-top:9px}
.fHeroBot .fTag{flex:0 0 auto;font-size:10px;padding:3px 9px}
.fHeroBot .fHeadline{flex:1;min-width:0;font-size:11.5px;line-height:1.6;margin:0}
@media (min-width:720px){
  .fHeroTop .fScore{font-size:42px}
  .fHeroTop .fScoreW{min-width:86px}
  .fDims{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));
  column-gap:22px;row-gap:7px}
  .fDims .fDimN{width:36px;font-size:11.5px}
  .fDims .fDimV{width:26px;font-size:11.5px}
}
.pp{border:1px solid rgba(240,215,156,.55);background:rgba(240,215,156,.10);color:#f0d79c;
border-radius:999px;padding:6px 14px;font-size:12.5px;letter-spacing:1px}
.pp:active{background:rgba(240,215,156,.24)}
.hbtns{position:absolute;right:11px;top:9px;display:flex;align-items:center;gap:8px}
.pback{position:static;left:auto;top:auto;margin:7px 0 0;display:none;grid-column:1;grid-row:2;
justify-self:start;align-items:center;gap:2px;padding:6px 11px 6px 9px;
border-radius:999px;font-family:inherit;font-size:12.5px;letter-spacing:1px;color:#d9d0f2;cursor:pointer;
background:rgba(38,32,66,.7);border:1px solid rgba(168,160,220,.32);
-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.pback.on{display:inline-flex}
.pback:active{background:rgba(240,215,156,.16);color:#f0d79c;border-color:rgba(240,215,156,.42)}
.pback i{font-style:normal;font-size:15px;line-height:1;margin-top:-1px}
.pp.mbtn{padding:6px 11px;font-size:14px;line-height:1}
.mmask{position:fixed;left:0;top:0;right:0;bottom:0;background:rgba(4,6,14,.5);opacity:0;pointer-events:none;transition:.18s;z-index:60}
.mmask.show{opacity:1;pointer-events:auto}
.mpanel{position:fixed;right:12px;top:52px;width:152px;z-index:70;border-radius:14px;overflow:hidden;
border:1px solid rgba(240,215,156,.35);background:linear-gradient(160deg,rgba(42,31,77,.98),rgba(15,13,26,.98));
box-shadow:0 14px 34px rgba(0,0,0,.55);opacity:0;transform:translateY(-6px);pointer-events:none;transition:.18s}
.mpanel.show{opacity:1;transform:none;pointer-events:auto}
.mitem{padding:12px 16px;font-size:13.5px;color:#e6dff6;letter-spacing:1px;border-bottom:1px solid rgba(255,255,255,.06)}
.mitem:last-child{border-bottom:none}
.mitem:active{background:rgba(240,215,156,.16);color:#f0d79c}
.pstMask{position:fixed;left:0;top:0;right:0;bottom:0;background:rgba(3,5,12,.86);opacity:0;pointer-events:none;transition:.2s;z-index:120}
.pstMask.show{opacity:1;pointer-events:auto}
.pstPanel{position:fixed;left:50%;top:50%;transform:translate(-50%,-47%) scale(.96);width:min(88vw,340px);z-index:130;opacity:0;pointer-events:none;transition:.24s cubic-bezier(.2,.7,.3,1);display:flex;flex-direction:column;align-items:center;gap:12px}
.pstPanel.show{opacity:1;pointer-events:auto;transform:translate(-50%,-50%) scale(1)}
.pstImgWrap{position:relative;width:min(100%,calc((90vh - 96px)*0.5622));aspect-ratio:750/1334;border-radius:16px;overflow:hidden;
border:1px solid rgba(240,215,156,.18);
box-shadow:0 0 42px rgba(96,220,208,.20),0 18px 40px rgba(0,0,0,.6);background:#070a14}
.pstImgWrap img{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;display:block;opacity:0;transition:opacity .4s ease}
.pstImgWrap.ready img{opacity:1}
.pstHold{position:absolute;left:0;top:0;right:0;bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:15px;
background:radial-gradient(120% 80% at 50% 34%,rgba(96,220,208,.10),rgba(120,96,200,.10) 46%,transparent 72%),#070a14;
transition:opacity .34s ease}
.pstImgWrap.ready .pstHold{opacity:0;pointer-events:none}
.pstHold .pHalo{position:relative;width:62px;height:62px;border-radius:50%;
border:1px solid rgba(96,220,208,.26);box-shadow:inset 0 0 22px rgba(96,220,208,.16),0 0 18px rgba(96,220,208,.12)}
.pstHold .pHalo::before{content:"";position:absolute;left:-1px;top:-1px;right:-1px;bottom:-1px;border-radius:50%;
border:2px solid transparent;border-top-color:#f0d79c;border-right-color:rgba(96,220,208,.75);animation:pSpin 1.5s linear infinite}
.pstHold .pHalo::after{content:"";position:absolute;left:50%;top:50%;width:22px;height:22px;margin:-11px 0 0 -11px;border-radius:50%;
background:radial-gradient(circle at 35% 32%,#fff8e2,#f0d79c 42%,#b99358 72%);box-shadow:0 0 16px rgba(240,215,156,.7);animation:pPulse 2.2s ease-in-out infinite}
@keyframes pSpin{to{transform:rotate(360deg)}}
@keyframes pPulse{0%,100%{transform:scale(.9);opacity:.82}50%{transform:scale(1.06);opacity:1}}
.pstHold .pTip{font-size:12.5px;letter-spacing:2px;color:#c9c2e2}
.pstHold .pTip b{color:#f0d79c;font-weight:700}
.pstBarWrap{position:relative;width:62%;height:3px;border-radius:3px;background:rgba(255,255,255,.10);overflow:hidden;transition:opacity .24s}
.pstBar{height:100%;width:0;border-radius:3px;background:linear-gradient(90deg,#f0d79c,#8fe6d6,#60dcd0);
box-shadow:0 0 10px rgba(96,220,208,.65);transition:width .22s ease}
.pstHold .pPct{font-size:10.5px;letter-spacing:1px;color:#7f8aa0;margin-top:-7px;font-variant-numeric:tabular-nums;transition:opacity .24s}
.pstImgWrap.fail .pstBarWrap,.pstImgWrap.fail .pPct{opacity:0}
.pstImgWrap.fail .pHalo::before{animation:none;border-top-color:#ff9aa2;border-right-color:rgba(255,154,162,.28)}
.pstImgWrap.fail .pHalo::after{animation:none;box-shadow:0 0 12px rgba(255,154,162,.35)}
.pstImgWrap.fail .pTip{color:#ff9aa2}
.pstBtn.dis{opacity:.42;pointer-events:none}
.pstHint{font-size:11.5px;color:#8c9bb0;letter-spacing:1px;text-align:center;margin-top:-2px}
.pstBtns{display:flex;gap:10px;width:100%}
.pstBtn{flex:1;padding:11px 0;border-radius:11px;font-size:13.5px;letter-spacing:1.5px;text-align:center;cursor:pointer;border:1px solid rgba(240,215,156,.42);background:linear-gradient(135deg,rgba(240,215,156,.92),rgba(214,178,110,.92));color:#20180a;font-weight:700;text-decoration:none}
.pstBtn.ghost{background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.18);color:#cfd6e2;font-weight:400}
.pstBtn:active{transform:translateY(1px)}
.loginwrap{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
.loginbox{width:100%;max-width:340px}
.lgbrand{text-align:center;font-size:22px;letter-spacing:4px;color:#f0d79c;font-weight:700;text-shadow:0 0 18px rgba(240,215,156,.45);margin-bottom:6px}
.lgsub{text-align:center;font-size:12px;color:#8e86ad;letter-spacing:2px;margin-bottom:24px}
.lgcard{background:rgba(255,255,255,.045);border:1px solid rgba(240,215,156,.22);border-radius:18px;padding:22px 20px 16px}
.lgcard label{display:block;font-size:12px;color:#9c93bd;letter-spacing:1px;margin:0 0 6px}
.lgcard input{width:100%;background:rgba(10,10,20,.55);border:1px solid rgba(168,160,220,.35);border-radius:10px;
color:#eae4f6;font-size:14px;padding:11px 12px;margin-bottom:14px;font-family:inherit;outline:none;user-select:text;-webkit-user-select:text}
.lgcard input:focus{border-color:rgba(240,215,156,.7)}
.lgbtn{width:100%;border:none;border-radius:10px;padding:12px;font-size:14px;letter-spacing:2px;font-family:inherit;
background:linear-gradient(120deg,#f0d79c,#e0b978);color:#1a1428;font-weight:700;cursor:pointer}
.lgbtn:active{opacity:.85}
.lgbtn:disabled{opacity:.55}
.lgerr{min-height:18px;text-align:center;font-size:12px;color:#ff9aa2;margin-top:10px;letter-spacing:.5px}
.lgback{display:block;text-align:center;font-size:12px;color:#8e86ad;margin-top:16px;text-decoration:none;letter-spacing:1px}
#stage{position:relative;flex:1;min-height:0;margin:0 8px;border-radius:16px;overflow:hidden;
isolation:isolate;z-index:1;
background:radial-gradient(620px 420px at 50% 30%,rgba(120,96,200,.24),transparent 74%)}
.sDeco{position:absolute;inset:0;pointer-events:none;z-index:0;overflow:hidden}
.sDeco svg{position:absolute}
.dMoon{left:-5%;top:-9%;width:42%;opacity:.5;filter:drop-shadow(0 0 10px rgba(240,215,156,.35))}
.dPlanet{right:-3%;top:3%;width:33%;opacity:.42;filter:drop-shadow(0 0 8px rgba(168,156,216,.45))}
.dFly{left:3%;bottom:-3%;width:33%;opacity:.42;filter:drop-shadow(0 0 8px rgba(240,215,156,.3))}
.dStar{position:absolute;width:2px;height:2px;border-radius:50%;background:#f0d79c;
box-shadow:0 0 7px rgba(240,215,156,.9);opacity:.55;animation:dTw 3.8s ease-in-out infinite}
@keyframes dTw{0%,100%{opacity:.18;transform:scale(.8)}50%{opacity:.85;transform:scale(1.25)}}
#stage .hint{position:absolute;left:0;right:0;top:42%;text-align:center;color:#5e5b7a;
font-size:12.5px;line-height:2;letter-spacing:1px}
.tcard{position:absolute;width:var(--cw);height:var(--ch);perspective:700px;touch-action:none;z-index:2}
.tcard .inner{position:relative;width:100%;height:100%;transform-style:preserve-3d;
transition:transform .45s cubic-bezier(.2,.8,.3,1)}
.tcard.flip .inner{transform:rotateY(180deg)}
.face,.back{position:absolute;left:0;top:0;width:100%;height:100%;border-radius:8px;overflow:hidden;
backface-visibility:hidden;-webkit-backface-visibility:hidden;box-shadow:0 6px 16px rgba(0,0,0,.55)}
.back{background:linear-gradient(150deg,#2a1f4d,#161327 55%,#241a3f);
border:1px solid rgba(240,215,156,.42);display:flex;align-items:center;justify-content:center}
.back:before{content:"";position:absolute;left:5px;top:5px;right:5px;bottom:5px;
border:1px solid rgba(240,215,156,.26);border-radius:5px}
.back i{font-style:normal;font-size:9px;letter-spacing:1px;color:#f0d79c;opacity:.9}
.face{transform:rotateY(180deg);background:#fff}
.face img{width:100%;height:100%;object-fit:cover;display:block}
.face.rev img{transform:rotate(180deg)}
.tcard .del{position:absolute;top:-7px;right:-7px;width:19px;height:19px;border-radius:50%;border:none;
background:rgba(18,14,30,.92);color:#f0d79c;font-size:12px;line-height:19px;display:none;z-index:5}
.tcard.flip .del{display:block}
.bar{display:flex;align-items:center;gap:8px;padding:9px 16px 4px}
.bar .cnt{font-size:11.5px;color:#8e86ad;flex:1;letter-spacing:.5px}
.bar button{border:1px solid rgba(168,160,220,.4);background:rgba(120,110,180,.18);
color:#cfc6ea;border-radius:999px;padding:5px 12px;font-size:11.5px}
.bar button:active{background:rgba(120,110,180,.34)}
#deck{display:flex;gap:7px;overflow-x:auto;overflow-y:hidden;padding:20px 14px 18px;
touch-action:pan-x;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch}
#deck::-webkit-scrollbar{display:none}
.dcard{flex:0 0 auto;width:46px;height:79px;border-radius:6px;position:relative;
border:1px solid rgba(240,215,156,.34);background:linear-gradient(150deg,#2a1f4d,#161327 55%,#241a3f);
box-shadow:0 3px 10px rgba(0,0,0,.5);touch-action:pan-x}
.dcard:before{content:"";position:absolute;left:4px;top:4px;right:4px;bottom:4px;
border:1px solid rgba(240,215,156,.22);border-radius:4px}
.dcard i{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);text-align:center;
font-style:normal;font-size:8.5px;color:rgba(240,215,156,.75);letter-spacing:.5px}
.dcard.taken{background:rgba(255,255,255,.03);border:1px dashed rgba(240,215,156,.20);
box-shadow:none;cursor:default}
.dcard.taken:before{border-color:rgba(240,215,156,.10)}
.dcard.taken i{display:none}
.dcard.taken .dno{color:#6b6588}
.dcard .dno{position:absolute;left:0;right:0;top:-15px;text-align:center;font-style:normal;
font-weight:600;font-size:9.5px;color:#8e86ad;letter-spacing:0}
@keyframes shfJit{
  0%{transform:translate3d(0,0,0) rotate(0deg)}
  28%{transform:translate3d(-9px,-5px,0) rotate(-7deg)}
  58%{transform:translate3d(9px,3px,0) rotate(6deg)}
  80%{transform:translate3d(-4px,-2px,0) rotate(-3deg)}
  100%{transform:translate3d(0,0,0) rotate(0deg)}
}
@keyframes dealIn{
  0%{opacity:0;transform:translate3d(0,16px,0) scale(.88)}
  100%{opacity:1;transform:translate3d(0,0,0) scale(1)}
}
#deck.deckHide .dcard{opacity:0}
#shfLayer{position:absolute;left:0;top:0;right:0;bottom:0;overflow:hidden;pointer-events:none;z-index:12}
.pickGhost{position:fixed;width:46px;height:79px;border-radius:6px;pointer-events:none;z-index:900;
transform:translate(-50%,-50%) scale(1.06);display:flex;align-items:center;justify-content:center;
font-style:normal;font-size:8.5px;letter-spacing:.5px;color:rgba(240,215,156,.9);
border:1px solid rgba(240,215,156,.7);
background:linear-gradient(150deg,#2a1f4d,#161327 55%,#241a3f);
box-shadow:0 10px 24px rgba(0,0,0,.6),0 0 16px rgba(240,215,156,.35)}
#shfLayer .sc{position:absolute;width:46px;height:79px;border-radius:6px;display:flex;
align-items:center;justify-content:center;font-style:normal;font-size:8.5px;letter-spacing:.5px;
color:rgba(240,215,156,.78);border:1px solid rgba(240,215,156,.5);
background:linear-gradient(150deg,#2a1f4d,#161327 55%,#241a3f);
box-shadow:0 6px 16px rgba(0,0,0,.5),0 0 12px rgba(240,215,156,.22);will-change:transform,opacity}
#shfLayer .sc:before{content:"";position:absolute;left:4px;top:4px;right:4px;bottom:4px;
border:1px solid rgba(240,215,156,.22);border-radius:4px}
/* 层级约定：#stage(1) < 牌堆/洗牌层(12) < 分享弹窗(120/130) < 牌义/其它弹窗(1000) < 首次引导(1200) */
.mask{position:fixed;left:0;top:0;right:0;bottom:0;background:rgba(6,8,16,.74);
display:none;align-items:center;justify-content:center;padding:22px;z-index:1000}
.mask.on{display:flex}
.ppcard{width:100%;max-width:340px;background:#fff;border-radius:18px;overflow:hidden;position:relative}
.ppcard img{width:100%;display:block}
.ppcard .wx{padding:10px 16px 16px;text-align:center;color:#3a3350;font-size:12px}
.ppcard .wx b{color:#7a5cc4;font-size:15px;letter-spacing:.5px;display:block;margin:5px 0 11px}
.cbtn{width:100%;border:none;border-radius:999px;padding:11px 0;
background:linear-gradient(90deg,#8a6fd6,#5b48a8);color:#fff;font-size:13.5px;letter-spacing:1px}
.copyok{font-size:11px;color:#4e9d76;text-align:center;height:14px;margin-top:6px}
.close{position:absolute;top:8px;right:10px;width:26px;height:26px;border:none;border-radius:50%;
background:rgba(0,0,0,.35);color:#fff;font-size:15px;line-height:26px;z-index:6}
.meanbox{width:100%;max-width:330px;background:linear-gradient(160deg,#1d1a33,#141327);
border:1px solid rgba(240,215,156,.35);border-radius:16px;padding:22px 18px 18px;position:relative}
.meanbox h3{color:#f0d79c;font-size:16px;letter-spacing:1px;margin-bottom:6px;text-align:center}
.meanbox .pos{text-align:center;font-size:11.5px;color:#9c93bd;letter-spacing:3px;margin-bottom:14px}
.meanbox .kw{font-size:13.5px;line-height:1.95;color:#e6e0f5}
.meanbox .foot{margin-top:14px;font-size:11px;color:#7b739a;line-height:1.8;
border-top:1px dashed rgba(255,255,255,.12);padding-top:10px}
.cfbox{width:100%;max-width:300px;background:linear-gradient(160deg,#1d1a33,#141327);
border:1px solid rgba(240,215,156,.35);border-radius:16px;padding:22px 18px 16px;text-align:center}
.cfbox h3{color:#f0d79c;font-size:15.5px;letter-spacing:2px;margin-bottom:9px}
.cfbox .cfmsg{font-size:12.5px;color:#a79ec6;line-height:1.85;letter-spacing:.5px;margin-bottom:18px}
.cfbtns{display:flex;gap:10px}
.cfbtns button{flex:1;border-radius:999px;padding:11px 0;font-family:inherit;font-size:13.5px;letter-spacing:1px}
.cfbtns .cbtnCancel{border:1px solid rgba(168,160,220,.42);background:rgba(120,110,180,.16);color:#cfc6ea}
.cfbtns .cbtnCancel:active{background:rgba(120,110,180,.32)}
.cfbtns .cbtnOk{border:none;background:linear-gradient(120deg,#f0d79c,#e0b978);color:#1a1428;font-weight:700}
.cfbtns .cbtnOk:active{opacity:.86}
/* ===== 答案之书 ===== */
.hcard.anscard{background:linear-gradient(150deg,rgba(26,76,84,.94),rgba(15,17,32,.97));
border-color:rgba(127,233,220,.34)}
.hcard.anscard .hi,.hcard.anscard b,.hcard.anscard .ha{color:#8fe9dd}
.hcard.anscard span{color:#88a6ad}
/* ===== 星骰 ===== */
.hcard.dicecard{background:linear-gradient(150deg,rgba(60,36,100,.94),rgba(15,17,32,.97));border-color:rgba(240,215,156,.32)}
.hcard.dicecard .hi,.hcard.dicecard b,.hcard.dicecard .ha{color:#f0d79c}
.hcard.dicecard span{color:#a49bc4}
#view-dice{display:none;flex-direction:column;flex:1;min-height:0;overflow-y:auto;padding:4px 16px 18px}
.dcWrap{display:flex;flex-direction:column;align-items:center;gap:12px;flex:1;min-height:0;width:100%;max-width:430px;margin:0 auto}
.dcTop{text-align:center;margin-top:4px}
.dcTop b{display:block;font-size:15px;letter-spacing:7px;color:#f0d79c;font-weight:700;text-shadow:0 0 18px rgba(240,215,156,.42)}
.dcTop span{display:block;margin-top:8px;font-size:11.5px;color:#8b83a8;letter-spacing:.8px}
.dcStage{position:relative;width:100%;height:228px;display:flex;align-items:center;justify-content:center;gap:10px;overflow:hidden}
.dcGlow{position:absolute;left:50%;top:50%;width:206px;height:206px;margin:-103px 0 0 -103px;border-radius:50%;
background:radial-gradient(circle,rgba(178,152,255,.3),rgba(127,233,220,.09) 52%,transparent 72%);
filter:blur(9px);animation:dcBreath 5.2s ease-in-out infinite;pointer-events:none}
@keyframes dcBreath{0%,100%{opacity:.45;transform:scale(.94)}50%{opacity:.9;transform:scale(1.07)}}
.dcRing{position:absolute;left:50%;top:50%;border-radius:50%;border:1px dashed rgba(178,152,255,.24);pointer-events:none}
.dcRing.r1{width:172px;height:172px;margin:-86px 0 0 -86px;animation:dcSpin 26s linear infinite}
.dcRing.r2{width:214px;height:214px;margin:-107px 0 0 -107px;border-color:rgba(240,215,156,.14);animation:dcSpin 40s linear infinite reverse}
@keyframes dcSpin{to{transform:rotate(360deg)}}
.dcDice{position:relative;z-index:2;width:84px;display:flex;flex-direction:column;align-items:center;gap:9px;
--c1:#fce9c4;--c2:#e4b170;--c3:#a86e35;--edge:#fff7dd;--ink:#241a45;
filter:drop-shadow(0 15px 15px rgba(4,6,20,.55)) drop-shadow(0 3px 4px rgba(4,6,20,.45))}
.dcDice.sign{--c1:#e8dcff;--c2:#a98ae0;--c3:#63429c;--edge:#efe5ff;--ink:#1c1135}
.dcDice.house{--c1:#d3f8f1;--c2:#5fb6c7;--c3:#28627a;--edge:#defff9;--ink:#08222b}
.dcCube{position:relative;width:74px;height:84px;display:flex;align-items:center;justify-content:center;
clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
background:linear-gradient(168deg,var(--edge),rgba(255,255,255,.55) 46%,var(--c3));
color:var(--ink);font-size:25px;line-height:1;
font-family:"Segoe UI Symbol","Segoe UI","Arial Unicode MS",serif}
.dcCube::before{content:"";position:absolute;inset:1.8px;
clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
background:
radial-gradient(88% 58% at 30% 10%,rgba(255,255,255,.82),rgba(255,255,255,0) 60%),
linear-gradient(176deg,rgba(255,255,255,.45) 0%,rgba(255,255,255,0) 30%,rgba(0,0,0,.12) 68%,rgba(0,0,0,.4) 100%),
linear-gradient(160deg,var(--c1),var(--c2) 48%,var(--c3) 100%);
box-shadow:inset 0 -14px 18px -11px rgba(38,14,0,.8),inset 0 10px 12px -9px rgba(255,255,255,.95);
pointer-events:none}
.dcCube::after{content:"";position:absolute;left:9%;top:7%;width:54%;height:26%;border-radius:50%;
background:radial-gradient(closest-side,rgba(255,255,255,.9),rgba(255,255,255,0) 100%);
filter:blur(2.2px);pointer-events:none}
.dcCube span{position:relative;z-index:2;display:block;
text-shadow:0 1px 0 rgba(255,255,255,.55),0 2px 5px rgba(0,0,0,.26)}
.dcCube.roll{animation:dcShake .3s linear infinite}
@keyframes dcShake{0%,100%{transform:translateY(0) rotate(-3deg)}50%{transform:translateY(-7px) rotate(3deg)}}
.dcCube.lit{filter:brightness(1.14) saturate(1.08)}
.dcLab{font-size:10.5px;color:#b9b0d4;letter-spacing:1.2px;text-align:center;line-height:1.35}
.dcLab em{display:block;font-style:normal;color:#6f6788;font-size:9.5px;margin-top:3px;letter-spacing:.4px}
.dcAsk{width:100%;display:flex;flex-direction:column;gap:9px}
.dcAsk input{width:100%;background:rgba(20,26,48,.74);border:1px solid rgba(168,160,220,.3);border-radius:12px;
padding:11px 13px;color:#eae4f6;font-family:inherit;font-size:13px;letter-spacing:.4px;outline:none}
.dcAsk input::placeholder{color:#645c80}
.dcAsk input:focus{border-color:rgba(240,215,156,.5)}
.dcChips{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}
.dcChip{font-size:11.5px;color:#c9bfe8;border:1px solid rgba(168,160,220,.26);background:rgba(120,110,180,.13);
border-radius:999px;padding:6px 11px;cursor:pointer;letter-spacing:.3px}
.dcChip:active{background:rgba(240,215,156,.16);color:#f0d79c;border-color:rgba(240,215,156,.4)}
.dcGo{width:100%;border:none;border-radius:999px;padding:13px 0;font-family:inherit;font-size:14px;letter-spacing:2px;
font-weight:700;color:#1a1428;background:linear-gradient(120deg,#f0d79c,#dcb473);box-shadow:0 8px 26px rgba(240,215,156,.22)}
.dcGo:active{opacity:.86}
.dcGo[disabled]{opacity:.55;box-shadow:none}
.dcRes{display:none;width:100%;flex-direction:column;gap:9px}
.dcRes.on{display:flex}
.dcQ{font-size:11.5px;color:#8b83a8;letter-spacing:.4px;text-align:center;line-height:1.5}
.dcTri{display:flex;gap:7px}
.dcCell{flex:1;border-radius:12px;padding:11px 10px;background:linear-gradient(160deg,rgba(44,52,86,.94),rgba(26,30,52,.92));border:1px solid rgba(168,160,220,.26)}
.dcCell b{display:block;font-size:10.5px;letter-spacing:1.4px;color:#f0d79c;margin-bottom:7px;font-weight:600}
.dcCell p{font-size:12px;line-height:1.78;color:#e2dcf5;margin:0}
.dcCell.sign b{color:#c6aeff}
.dcCell.sign{border-color:rgba(198,174,255,.24)}
.dcCell.house b{color:#8fe9dd}
.dcCell.house{border-color:rgba(143,233,221,.22)}
.dcLine{font-size:12.5px;line-height:1.8;color:#e6dff6;padding:11px 12px;border-radius:12px;
background:linear-gradient(150deg,rgba(60,36,100,.62),rgba(15,17,32,.72));border:1px solid rgba(240,215,156,.2)}
.dcFoot{font-size:10.5px;color:#6f6788;letter-spacing:.6px;text-align:center;padding:2px 0 4px}
#view-answer{display:none;flex-direction:column;flex:1;min-height:0;overflow-y:auto;padding:6px 20px 22px}
.ansWrap{display:flex;flex-direction:column;align-items:center;justify-content:flex-start;gap:18px;flex:1;min-height:0}
#view-answer.hasAns .ansWrap{gap:18px}
#view-answer.hasAns .ansResult{padding:8px 0;margin:-10px 0 10px;display:flex;flex-direction:column;justify-content:center;align-items:stretch;flex:0 0 auto;height:286px;width:100%}
.ansTop{text-align:center;margin:0 0 2px}
.ansTop b{display:block;font-size:clamp(20px,5.6vw,25px);letter-spacing:5px;color:#8fe9dd;font-weight:700;
line-height:1.25;text-shadow:0 0 18px rgba(127,233,220,.42),0 0 34px rgba(127,233,220,.2)}
.ansTop span{display:block;margin-top:8px;font-size:11.5px;color:#8b83a8;letter-spacing:.8px;line-height:1.7}
.ansStage{position:relative;width:100%;max-width:330px;height:286px;display:flex;
align-items:center;justify-content:center;flex:0 0 auto}
.ansOrbit{position:absolute;border-radius:50%;border:1px dashed rgba(127,233,220,.22);pointer-events:none}
.ansOrbit.o1{width:212px;height:212px;animation:ansSpin 24s linear infinite}
.ansOrbit.o2{width:286px;height:286px;border-style:solid;border-color:rgba(240,215,156,.13);
animation:ansSpin 40s linear infinite reverse}
.ansOrbit.o3{width:156px;height:156px;border-color:rgba(127,233,220,.13);animation:ansSpin 16s linear infinite}
@keyframes ansSpin{to{transform:rotate(360deg)}}
.ansGlow{position:absolute;width:176px;height:176px;border-radius:50%;pointer-events:none;
background:radial-gradient(circle,rgba(127,233,220,.2) 0%,rgba(96,126,220,.11) 44%,transparent 72%);
animation:ansPulse 4.4s ease-in-out infinite}
@keyframes ansPulse{0%,100%{transform:scale(1);opacity:.72}50%{transform:scale(1.14);opacity:1}}
.ansDust{position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none;overflow:hidden}
.ansDust i{position:absolute;display:block;width:3px;height:3px;border-radius:50%;
background:rgba(200,255,250,.92);box-shadow:0 0 8px rgba(127,233,220,.9);
animation-name:ansUp;animation-timing-function:linear;animation-iteration-count:infinite}
@keyframes ansUp{from{transform:translateY(26px);opacity:0}28%{opacity:.9}to{transform:translateY(-124px);opacity:0}}
.ansFly{position:relative;width:130px;height:102px;transition:transform .55s ease;
animation:ansHover 5.2s ease-in-out infinite;z-index:2}
@keyframes ansHover{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
.ansWing{position:absolute;border:1px solid rgba(196,255,250,.48);
background:
radial-gradient(circle at 30% 28%,rgba(255,255,255,.62) 0%,rgba(255,255,255,0) 32%),
radial-gradient(circle at 64% 70%,rgba(200,255,250,.34) 0%,rgba(200,255,250,0) 30%),
linear-gradient(135deg,rgba(152,246,233,.92),rgba(118,158,255,.44) 58%,rgba(152,246,233,.12));
box-shadow:0 0 20px rgba(127,233,220,.5),inset 0 0 14px rgba(255,255,255,.3)}
.ansWing.up{width:57px;height:60px}
.ansWing.dn{width:42px;height:38px;opacity:.84;top:58px}
.ansWing.up.l{left:5px;top:4px;border-radius:80% 6% 32% 66%;transform-origin:right bottom;
animation:ansFlapUL 1.15s ease-in-out infinite}
.ansWing.up.r{right:5px;top:4px;border-radius:6% 80% 66% 32%;transform-origin:left bottom;
animation:ansFlapUR 1.15s ease-in-out infinite}
.ansWing.dn.l{left:11px;border-radius:70% 8% 54% 46%;transform-origin:right top;
animation:ansFlapDL 1.15s ease-in-out infinite}
.ansWing.dn.r{right:11px;border-radius:8% 70% 46% 54%;transform-origin:left top;
animation:ansFlapDR 1.15s ease-in-out infinite}
@keyframes ansFlapUL{0%,100%{transform:rotate(-21deg) scaleX(1)}50%{transform:rotate(-7deg) scaleX(.4)}}
@keyframes ansFlapUR{0%,100%{transform:rotate(21deg) scaleX(1)}50%{transform:rotate(7deg) scaleX(.4)}}
@keyframes ansFlapDL{0%,100%{transform:rotate(-13deg) scaleX(1)}50%{transform:rotate(-2deg) scaleX(.36)}}
@keyframes ansFlapDR{0%,100%{transform:rotate(13deg) scaleX(1)}50%{transform:rotate(2deg) scaleX(.36)}}
.ansBody{position:absolute;left:50%;top:11px;width:11px;height:86px;margin-left:-5.5px;border-radius:50%;
background:linear-gradient(180deg,#f7f2c6,#8fe9dd 46%,rgba(127,233,220,.22));
box-shadow:0 0 12px rgba(240,215,156,.55)}
.ansAnt{position:absolute;left:50%;top:2px;width:36px;height:20px;margin-left:-18px;
border-top:1px solid rgba(240,215,156,.72);border-radius:50% 50% 0 0}
.ansHint{display:none}
.ansResult{display:none;width:100%;max-width:330px;text-align:center;animation:ansIn .55s ease both;padding:6px 0 2px}
@keyframes ansIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
.ansText{font-size:28px;line-height:1.95;letter-spacing:4px;color:#eaf7f4;font-weight:600;
text-shadow:0 0 24px rgba(127,233,220,.34)}
.ansEn{margin-top:11px;font-size:10.5px;letter-spacing:3.6px;color:rgba(127,233,220,.82);
text-transform:uppercase}
.ansNote{margin-top:15px;font-size:12.2px;line-height:1.92;color:#a9a1c6;letter-spacing:.6px;
padding:13px 15px;border-radius:13px;text-align:left;
border:1px solid rgba(127,233,220,.17);
background:linear-gradient(140deg,rgba(127,233,220,.075),rgba(255,255,255,.015))}
.ansBtn{width:100%;max-width:330px;border:none;border-radius:999px;padding:16px 0;margin:4px 0 calc(2px + env(safe-area-inset-bottom,0px));font-family:inherit;
font-size:14px;letter-spacing:3px;font-weight:700;color:#07201d;cursor:pointer;
background:linear-gradient(120deg,#8fe9dd,#cbf2a6);box-shadow:0 10px 26px rgba(127,233,220,.2)}
.ansBtn:active{opacity:.86}
.ansBtn:disabled{opacity:.52}
.ansFoot{text-align:center;font-size:11px;color:#6f6788;letter-spacing:.6px;padding:2px 0 6px}
/* ===== 按钮防抖加载态 ===== */
@keyframes btnSpin{to{transform:rotate(360deg)}}
.isBusy{pointer-events:none !important;cursor:default}
button.isBusy,.pp.isBusy,.cta.isBusy,.mitem.isBusy,.cat.isBusy,.chip.isBusy{
  color:transparent !important;text-shadow:none !important;position:relative}
button.isBusy::after,.pp.isBusy::after,.cta.isBusy::after,.mitem.isBusy::after,.cat.isBusy::after,.chip.isBusy::after{
  content:"";position:absolute;left:50%;top:50%;width:15px;height:15px;margin:-7.5px 0 0 -7.5px;border-radius:50%;
  border:2px solid rgba(240,215,156,.92);border-right-color:transparent;border-bottom-color:transparent;
  animation:btnSpin .62s linear infinite}
.hcard.isBusy,.bnrTop.isBusy,.archItem.isBusy{opacity:.6}
.brand.isBusy{opacity:.55}
.hcard.isBusy::after,.bnrTop.isBusy::after,.archItem.isBusy::after{
  content:"";position:absolute;right:9px;top:9px;width:13px;height:13px;border-radius:50%;
  border:2px solid rgba(240,215,156,.92);border-right-color:transparent;border-bottom-color:transparent;
  animation:btnSpin .62s linear infinite}
/* ===== 首次抽牌引导（分步遮罩） ===== */
.gdWrap{position:fixed;left:0;top:0;right:0;bottom:0;z-index:1200;display:none}
.gdWrap.on{display:block}
.gdBlock{position:absolute;left:0;top:0;right:0;bottom:0;z-index:1;background:transparent}
.gdSpot{position:absolute;z-index:2;pointer-events:none;border-radius:18px;
box-shadow:0 0 0 1.5px rgba(96,220,208,.62),0 0 26px rgba(96,220,208,.34),0 0 0 9999px rgba(3,6,14,.82);
transition:left .28s cubic-bezier(.2,.8,.3,1),top .28s cubic-bezier(.2,.8,.3,1),
width .28s cubic-bezier(.2,.8,.3,1),height .28s cubic-bezier(.2,.8,.3,1)}
.gdSpot.plain{box-shadow:0 0 0 9999px rgba(3,6,14,.82)}
.gdBack{position:absolute;left:0;top:0;width:100%;height:100%;border-radius:inherit;overflow:hidden;
display:none;background:linear-gradient(150deg,#2a1f4d,#161327 55%,#241a3f);
box-shadow:inset 0 0 0 1px rgba(240,215,156,.42),inset 0 0 26px rgba(3,6,14,.55)}
.gdSpot.showBack .gdBack{display:block}
.gdBack svg{display:block;width:100%;height:100%}
.gdTip{position:absolute;z-index:3;width:min(86vw,308px);box-sizing:border-box;
padding:16px 17px 13px;border-radius:20px;text-align:left;
border:1px solid rgba(96,220,208,.34);
background:linear-gradient(165deg,rgba(22,34,50,.985),rgba(11,14,26,.985));
-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);
box-shadow:0 0 30px rgba(96,220,208,.16),0 16px 40px rgba(0,0,0,.62);
opacity:0;transform:translateY(8px) scale(.985);transition:opacity .24s ease,transform .24s cubic-bezier(.2,.8,.3,1)}
.gdTip.in{opacity:1;transform:none}
.gdFly{position:absolute;right:12px;top:10px;width:44px;opacity:.5;pointer-events:none}
.gdBadge{display:inline-block;font-size:10.5px;letter-spacing:1.4px;color:#7fe6da;
border:1px solid rgba(96,220,208,.36);background:rgba(96,220,208,.10);
border-radius:999px;padding:2px 9px;margin-bottom:9px}
.gdTitle{display:block;font-size:15px;color:#eafcfa;letter-spacing:1.2px;line-height:1.5;margin:0 34px 6px 0}
.gdText{margin:0;font-size:12.5px;line-height:1.95;color:#9fc4c6;letter-spacing:.7px}
.gdDots{display:flex;gap:6px;margin:13px 0 12px}
.gdDots i{width:5px;height:5px;border-radius:50%;background:rgba(159,196,198,.32);transition:.2s}
.gdDots i.on{width:16px;border-radius:999px;background:rgba(96,220,208,.92);box-shadow:0 0 9px rgba(96,220,208,.6)}
.gdBtns{display:flex;align-items:center;gap:9px}
.gdBtn{flex:1;text-align:center;border-radius:999px;padding:10px 0;font-size:13px;
letter-spacing:1.4px;cursor:pointer;user-select:none;-webkit-user-select:none;
border:1px solid rgba(96,220,208,.45);background:linear-gradient(135deg,rgba(96,220,208,.92),rgba(66,178,190,.92));
color:#04211f;font-weight:700;box-shadow:0 0 16px rgba(96,220,208,.26)}
.gdBtn:active{transform:translateY(1px)}
.gdBtn.ghost{flex:0 0 auto;padding:10px 17px;font-weight:400;color:#a9c8cb;
background:rgba(255,255,255,.045);border-color:rgba(255,255,255,.16);box-shadow:none}
.gdBtn.ghost:active{background:rgba(96,220,208,.14);color:#7fe6da}
</style>
</head>
<body>
<div id="app">
  <header>
    <div class="brand" id="btnBrand" role="button" tabindex="0" onclick="showView('home')" aria-label="返回首页">PPTAROT<span style="letter-spacing:0">🔮</span></div>
    <button class="pback" id="btnBack" aria-label="返回上一页"><i>‹</i>返回</button>
    <div class="hbtns">
      <button class="pp" id="btnPP">合作咨询</button>
      <button class="pp mbtn" id="btnMenu" aria-label="菜单">☰</button>
    </div>
    <div class="mmask" id="mMask"></div>
    <div class="mpanel" id="mPanel">
      <div class="mitem" id="miPoster">分享海报</div>
      <div class="mitem" onclick="closeMenu();location.href='/admin'">管理后台</div>
    </div>
  </header>

  <div class="pstMask" id="pstMask"></div>
  <div class="pstPanel" id="pstPanel">
    <div class="pstImgWrap" id="pstImgWrap">
      <img id="pstImg" alt="PPTAROT 分享海报">
      <div class="pstHold" id="pstHold">
        <div class="pHalo"></div>
        <div class="pTip" id="pstTip"><b>正在绘制</b> 你的专属海报</div>
        <div class="pstBarWrap"><div class="pstBar" id="pstBar"></div></div>
        <div class="pPct" id="pstPct">0%</div>
      </div>
    </div>
    <div class="pstBtns">
      <a class="pstBtn dis" id="pstSave" href="/api/poster" download="PPTAROT-分享海报.jpg">保存海报</a>
      <button class="pstBtn ghost" id="pstClose" type="button">关闭</button>
    </div>
  </div>

  <main id="view-home">
    <div class="hboard">
      <!-- 顶部 banner 海报 -->
      <a class="bnrTop" id="bnrLink">
        <img class="bnrBg" id="bnrBg" alt="" aria-hidden="true" src="/assets/banner_base.png?v=9">
        <img id="bnrImg" alt="PP TAROT" src="/assets/banner_base.png?v=9">
        <div class="bnrFly" id="bnrFly">
          <div class="wl"><img src="/assets/fly_l.png?v=8" alt=""></div>
          <div class="wr"><img src="/assets/fly_r.png?v=8" alt=""></div>
        </div>
        <div class="ph" id="bnrPh" style="display:none">
          <b>PP TAROT</b>
          <span>它只把你心里那句话说出来</span>
        </div>
      </a>

      <!-- 六个功能入口：H5 每行两个 / 宽屏一行六个，名称居中 -->
      <div class="hgrid">
        <a class="hcard gold" id="btnHomeFortune" role="button" tabindex="0">
          <div class="hi">✦</div>
          <b>今日运势</b>
        </a>
        <a class="hcard" id="btnHomeDaily" role="button" tabindex="0">
          <div class="hi">🌙</div>
          <b>每日塔罗</b>
        </a>
        <a class="hcard" id="btnHomeAstro" role="button" tabindex="0">
          <div class="hi">🪐</div>
          <b>星盘</b>
        </a>
        <a class="hcard" id="btnHomeDraw" role="button" tabindex="0">
          <div class="hi">🔮</div>
          <b>塔罗牌</b>
        </a>
        <a class="hcard anscard" id="btnHomeAnswer" role="button" tabindex="0">
          <div class="hi">🦋</div>
          <b>答案之书</b>
        </a>
        <a class="hcard dicecard" id="btnHomeDice" role="button" tabindex="0">
          <div class="hi">🎲</div>
          <b>星骰</b>
        </a>
      </div>
    </div>
  </main>

  <!-- 第二层：点「塔罗牌」进来的方向选择页（塔罗牌 + 蝴蝶） -->
  <main id="view-dir" style="display:none">
    <div class="dirBg" aria-hidden="true">
      <div class="glow"></div>
      <div class="ring r3"></div>
      <div class="ring r2"></div>
      <div class="ring r1"></div>
      <span class="rn" style="left:9%;top:17%">XII</span>
      <span class="rn" style="right:11%;top:23%">VII</span>
      <span class="rn" style="left:14%;bottom:19%">IV</span>
      <span class="rn" style="right:9%;bottom:14%">IX</span>
      <span class="sg" style="left:47%;top:8%;font-size:9px;opacity:.7">✦</span>
      <span class="sg" style="left:31%;bottom:8%;font-size:9px;opacity:.7">✧</span>
    </div>
    <div class="dirWrap">
      <div class="dirTop">
        <b>问 什 么</b>
      </div>
      <div class="cats" id="homeCats"></div>
    </div>
  </main>

  <main id="view-draw" style="display:none">
    <div id="shfLayer"></div>
    <div class="dcatTip" id="drawCatTip" style="display:none"></div>
    <section id="stage">
      <div class="sDeco" aria-hidden="true">
        <svg class="dMoon" viewBox="0 0 100 100">
          <defs><mask id="moonMask"><rect width="100" height="100" fill="#fff"/><circle cx="68" cy="46" r="38" fill="#000"/></mask></defs>
          <circle cx="46" cy="50" r="38" fill="#f0d79c" mask="url(#moonMask)"/>
        </svg>
        <svg class="dPlanet" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="24" fill="#a89cd8"/>
          <ellipse cx="50" cy="50" rx="46" ry="12" fill="none" stroke="#cfc6ea" stroke-width="2.2" transform="rotate(-20 50 50)"/>
        </svg>
        <svg class="dFly" viewBox="0 0 120 100">
          <g fill="none" stroke="#f0d79c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M60 50C52 26 22 16 16 34c-6 18 20 30 42 22"/>
            <path d="M60 54C50 68 26 80 22 68c-4-12 18-18 36-12"/>
            <path d="M60 50c8-24 38-34 44-16 6 18-20 30-42 22"/>
            <path d="M60 54c10 14 34 26 38 14 4-12-18-18-36-12"/>
            <path d="M60 44v18"/>
            <path d="M60 46C56 38 50 33 44 31"/>
            <path d="M60 46c4-8 10-13 16-15"/>
          </g>
        </svg>
        <i class="dStar" style="left:32%;top:18%"></i>
        <i class="dStar" style="left:12%;top:52%;animation-delay:1.1s"></i>
        <i class="dStar" style="left:74%;top:62%;animation-delay:2.2s"></i>
        <i class="dStar" style="left:88%;top:34%;animation-delay:.6s"></i>
      </div>
      <div class="hint" id="hint"></div>
    </section>
    <div class="bar">
      <span class="cnt" id="cnt">已选 0 张 · 共 78 张</span>
      <button id="btnShuffle">洗牌</button>
      <button id="btnClear">清空桌面</button>
    </div>
    <div id="deck"></div>
  </main>

  <main id="view-fortune" style="display:none">
    <div id="fBody"></div>
  </main>

  <main id="view-astro" style="display:none">
    <!-- 档案列表：存过的出生时间 -->
    <div id="aArchWrap">
      <div class="aTip">存过的出生时间，点一条直接看盘</div>
      <div class="archBox" id="aArchList"></div>
      <button class="aAdd" id="btnArchAdd" type="button">＋ 添一条出生时间</button>
    </div>

    <!-- 出生时间表单 -->
    <div class="aCard" id="aForm" style="display:none">
      <div class="aFormTop"><b id="aFormTitle">添加出生时间</b><span id="aFormCancel">取消</span></div>
      <div class="aField"><label>称呼（自己认得出就行）</label>
        <input id="aName" type="text" placeholder="比如：我自己 / 小A" maxlength="16">
      </div>
      <div class="aField"><label>出生日期</label>
        <button class="aPick" id="aDateBtn" type="button" aria-haspopup="dialog"><span id="aDateTxt" class="ph">点这里选年月日</span><i>›</i></button>
      </div>
      <div class="aField"><label>出生时间</label>
        <button class="aPick" id="aTimeBtn" type="button" aria-haspopup="dialog"><span id="aTimeTxt" class="ph">点这里选时分</span><i>›</i></button>
      </div>
      <label class="aChk"><input type="checkbox" id="aNoTime"> 不记得出生时间，按中午 12:00 算</label>
      <div class="aField"><label>出生城市</label>
        <button class="aPick" id="aCityBtn" type="button" aria-haspopup="dialog"><span id="aCityTxt" class="ph">点这里选省 / 市 / 区</span><i>›</i></button>
      </div>
      <button class="cta" id="btnAstroGo">存下来并看今天 →</button>
      <div class="aErr" id="aErr"></div>
    </div>

    <div id="aResult" style="display:none"></div>

    <div class="chartMask" id="chartMask" onclick="if(event.target===this)apCloseChart()">
      <div class="chartSheet">
        <div class="csTop"><b>本命盘</b><span onclick="apCloseChart()">×</span></div>
        <div id="chartBody"></div>
      </div>
    </div>

    <div class="chartMask" id="archPick" onclick="if(event.target===this)apClosePick()">
      <div class="chartSheet archPickSheet">
        <div class="csTop"><b>切换档案</b><span onclick="apClosePick()">×</span></div>
        <div class="archBox" id="apPickList"></div>
        <button class="apPickMore" onclick="apClosePick();showArchList();loadArch()">管理全部档案 ›</button>
      </div>
    </div>

    <div class="chartMask" id="plMask" onclick="if(event.target===this)apCloseHouse()">
      <div class="chartSheet plSheet">
        <div class="csTop"><b id="plTitle">星体落宫</b><span onclick="apCloseHouse()">×</span></div>
        <div id="plBody"></div>
      </div>
    </div>
  </main>

  <main id="view-answer" style="display:none">
    <div class="ansWrap">
      <div class="ansTop">
        <b>答案之书</b>
      </div>
      <div class="ansStage" id="ansStage">
        <div class="ansOrbit o3"></div>
        <div class="ansOrbit o1"></div>
        <div class="ansOrbit o2"></div>
        <div class="ansGlow"></div>
        <div class="ansDust" id="ansDust"></div>
        <div class="ansFly" id="ansFly">
          <span class="ansWing up l"></span>
          <span class="ansWing up r"></span>
          <span class="ansWing dn l"></span>
          <span class="ansWing dn r"></span>
          <span class="ansBody"></span>
          <span class="ansAnt"></span>
        </div>
        <div class="ansHint" id="ansHint">蝴蝶还停着，答案没起飞</div>
      </div>
      <div class="ansResult" id="ansResult">
        <div class="ansText" id="ansText"></div>
        <div class="ansEn" id="ansEn"></div>
        <div class="ansNote" id="ansNote"></div>
      </div>
      <button class="ansBtn" id="btnAnsGo">让蝴蝶飞一趟</button>
    </div>
  </main>

  <main id="view-dice" style="display:none">
    <div class="dcWrap">
      <div class="dcTop">
        <b>星 骰</b>
        <span>行星定推力，星座定方式，宫位定它落在哪</span>
      </div>
      <div class="dcStage">
        <div class="dcRing r1"></div>
        <div class="dcRing r2"></div>
        <div class="dcGlow"></div>
        <div class="ansDust" id="dcDust"></div>
        <div class="dcDice planet">
          <div class="dcCube" id="dcCube0"><span style="font-size:25px">☉</span></div>
          <div class="dcLab">行星<em>什么力量在推你</em></div>
        </div>
        <div class="dcDice sign">
          <div class="dcCube" id="dcCube1"><span style="font-size:30px">♈</span></div>
          <div class="dcLab">星座<em>它会怎么发生</em></div>
        </div>
        <div class="dcDice house">
          <div class="dcCube" id="dcCube2"><span style="font-size:27px">1</span></div>
          <div class="dcLab">宫位<em>落在哪个领域</em></div>
        </div>
      </div>
      <div class="dcAsk">
        <input id="dcQInput" type="text" maxlength="40" placeholder="把问题压成一句话，也可以不写">
        <div class="dcChips">
          <span class="dcChip" data-q="他还会主动吗">他还会主动吗</span>
          <span class="dcChip" data-q="这件事还要不要继续">这件事还要不要继续</span>
          <span class="dcChip" data-q="我最近到底怎么了">我最近到底怎么了</span>
        </div>
      </div>
      <button class="dcGo" id="btnDiceGo">掷出我的星骰</button>
      <div class="dcRes" id="dcRes">
        <div class="dcQ" id="dcQTxt"></div>
        <div class="dcTri">
          <div class="dcCell"><b>行星 · 推力</b><p id="dcTxt0"></p></div>
          <div class="dcCell sign"><b>星座 · 方式</b><p id="dcTxt1"></p></div>
          <div class="dcCell house"><b>宫位 · 领域</b><p id="dcTxt2"></p></div>
        </div>
        <div class="dcLine" id="dcLine"></div>
      </div>
    </div>
  </main>

  <main id="view-daily" style="display:none">
    <div class="dlyTop">
      <b>每日塔罗</b>
      <span id="dlyDate"></span>
    </div>
    <div class="dlyStage">
      <div class="dlyHalo"></div>
      <div class="dlyRing r1"></div>
      <div class="dlyRing r2"></div>
      <div class="dlyCardWrap" id="dlyWrap">
        <div class="dlyBack" id="dlyBack"><i>☾</i><em>DAILY TAROT</em></div>
        <div class="dlyFace" id="dlyFace"><img id="dlyImg" alt=""></div>
      </div>
    </div>
    <div class="dlyAsk" id="dlyAsk">
      <b>今天这张牌，等你翻开</b>
    </div>
    <button class="cta dlyBtn" id="btnDlyGo">立即开启</button>
    <div class="dlyRes" id="dlyRes">
      <div class="dlyName" id="dlyName"></div>
      <div class="dlyPos"><em id="dlyPos"></em></div>
      <div class="dlyKw" id="dlyKw"></div>
      <div class="dlySec"><h4>今天的状态</h4><p id="dlyP1"></p></div>
      <div class="dlySec"><h4>它在提醒你</h4><p id="dlyP2"></p></div>
      <div class="dlySec"><h4>可以这么做</h4><p id="dlyP3"></p></div>
    </div>
  </main>

</div>

<div class="pkMask" id="pkMask">
  <div class="pkSheet">
    <div class="pkBar">
      <span class="pkCancel" id="pkCancel">取消</span>
      <b id="pkTitle"></b>
      <span class="pkOk" id="pkOk">确定</span>
    </div>
    <div class="pkWrap" id="pkWrap">
      <div class="pkSel"></div>
    </div>
  </div>
</div>

<div class="mask" id="ppMask">
  <div class="ppcard">
    <button class="close" id="ppClose">×</button>
    <img id="ppImg" src="/assets/contact_card.gif" alt="联系方式">
    <div class="wx">
      微信
      <b id="wxText"></b>
      <button class="cbtn" id="btnCopy">复制微信号</button>
      <div class="copyok" id="copyok"></div>
    </div>
  </div>
</div>

<div class="mask" id="meanMask">
  <div class="meanbox">
    <button class="close" id="mClose" style="background:transparent;color:#9c93bd">×</button>
    <h3 id="mName"></h3>
    <div class="pos" id="mPos"></div>
    <div class="kw" id="mKw"></div>
    <div class="foot">牌只是镜子的一面，路还得你自己走。想细聊，点右上角「合作咨询」。</div>
  </div>
</div>

<div class="mask" id="cfMask">
  <div class="cfbox">
    <h3 id="cfTitle">洗牌</h3>
    <div class="cfmsg" id="cfMsg"></div>
    <div class="cfbtns">
      <button class="cbtnCancel" id="cfCancel">取消</button>
      <button class="cbtnOk" id="cfOk">洗牌</button>
    </div>
  </div>
</div>

<div class="gdWrap" id="gdWrap" aria-hidden="true">
  <div class="gdBlock" id="gdBlock"></div>
  <div class="gdSpot plain" id="gdSpot">
    <div class="gdBack" aria-hidden="true">
      <svg viewBox="0 0 150 230" preserveAspectRatio="xMidYMid meet">
        <defs>
          <radialGradient id="gdHalo" cx="50%" cy="48%" r="50%">
            <stop offset="0" stop-color="#57c9c0" stop-opacity=".34"/>
            <stop offset="60%" stop-color="#2d7f86" stop-opacity=".12"/>
            <stop offset="100%" stop-color="#0b1020" stop-opacity="0"/>
          </radialGradient>
          <mask id="gdMoonMask">
            <rect x="0" y="0" width="150" height="230" fill="#000"/>
            <circle cx="75" cy="113" r="25" fill="#fff"/>
            <circle cx="86" cy="105" r="23" fill="#000"/>
          </mask>
          <filter id="gdSoft" x="-70%" y="-70%" width="240%" height="240%">
            <feGaussianBlur stdDeviation="2.4" result="b"/>
            <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
        </defs>
        <rect x="0" y="0" width="150" height="230" fill="url(#gdHalo)"/>
        <rect x="7" y="7" width="136" height="216" rx="13" fill="none" stroke="rgba(240,215,156,.44)" stroke-width="1.2"/>
        <rect x="12.5" y="12.5" width="125" height="205" rx="10" fill="none" stroke="rgba(127,230,218,.28)" stroke-width=".9"/>
        <circle cx="75" cy="113" r="46" fill="none" stroke="rgba(127,230,218,.16)" stroke-width=".8"/>
        <circle cx="75" cy="113" r="25" fill="#7fe6da" mask="url(#gdMoonMask)" filter="url(#gdSoft)"/>
        <g fill="#bfeee8" filter="url(#gdSoft)">
          <path d="M0-7C1-2.3 2.3-1 7 0C2.3 1 1 2.3 0 7C-1 2.3-2.3 1-7 0C-2.3-1-1-2.3 0-7Z" transform="translate(112,86) scale(1)"/>
          <path d="M0-7C1-2.3 2.3-1 7 0C2.3 1 1 2.3 0 7C-1 2.3-2.3 1-7 0C-2.3-1-1-2.3 0-7Z" transform="translate(42,152) scale(.72)"/>
          <path d="M0-7C1-2.3 2.3-1 7 0C2.3 1 1 2.3 0 7C-1 2.3-2.3 1-7 0C-2.3-1-1-2.3 0-7Z" transform="translate(104,160) scale(.55)"/>
          <path d="M0-7C1-2.3 2.3-1 7 0C2.3 1 1 2.3 0 7C-1 2.3-2.3 1-7 0C-2.3-1-1-2.3 0-7Z" transform="translate(54,70) scale(.5)"/>
          <path d="M0-7C1-2.3 2.3-1 7 0C2.3 1 1 2.3 0 7C-1 2.3-2.3 1-7 0C-2.3-1-1-2.3 0-7Z" transform="translate(75,184) scale(.46)"/>
        </g>
        <g fill="rgba(127,230,218,.75)">
          <circle cx="36" cy="104" r="1.1"/><circle cx="116" cy="130" r="1.1"/>
          <circle cx="96" cy="62" r=".9"/><circle cx="38" cy="188" r=".9"/>
          <circle cx="120" cy="198" r="1"/><circle cx="66" cy="44" r=".8"/>
        </g>
      </svg>
    </div>
  </div>
  <div class="gdTip" id="gdTip" role="dialog" aria-label="首次抽牌引导">
    <svg class="gdFly" viewBox="0 0 120 100" aria-hidden="true">
      <g fill="none" stroke="#7fe6da" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M60 50C52 26 22 16 16 34c-6 18 20 30 42 22"/>
        <path d="M60 54C50 68 26 80 22 68c-4-12 18-18 36-12"/>
        <path d="M60 50c8-24 38-34 44-16 6 18-20 30-42 22"/>
        <path d="M60 54c10 14 34 26 38 14 4-12-18-18-36-12"/>
        <path d="M60 44v18"/>
      </g>
    </svg>
    <span class="gdBadge" id="gdBadge">1 / 4</span>
    <b class="gdTitle" id="gdTitle"></b>
    <p class="gdText" id="gdText"></p>
    <div class="gdDots" id="gdDots"><i class="on"></i><i></i><i></i><i></i></div>
    <div class="gdBtns">
      <div class="gdBtn ghost" id="gdSkip" role="button" tabindex="0">跳过</div>
      <div class="gdBtn" id="gdNext" role="button" tabindex="0">下一步</div>
    </div>
  </div>
</div>

<script>
/* ===== 全站按钮防抖 + 加载特效 ===== */
(function(){
  var LOCK = 520;                                            /* 同一控件最短锁定时长 */
  var SEL  = 'button,a,[onclick],[role="button"],.hcard,.mitem,.cat,.bnrTop,.archItem,.chip,.cta';
  var lastEl = null;
  function pick(t){ try { return t && t.closest ? t.closest(SEL) : null; } catch(e){ return null; } }
  function lock(el){
    if (!el) return false;
    if (el.__busy) return false;
    el.__busy = true; el.__t0 = Date.now();
    el.classList.add('isBusy'); el.setAttribute('aria-busy','true');
    return true;
  }
  function unlock(el){
    if (!el || !el.__busy) return;
    el.__busy = false; el.__t0 = 0;
    el.classList.remove('isBusy'); el.removeAttribute('aria-busy');
  }
  function release(el){
    if (!el || !el.__busy) return;
    var left = LOCK - (Date.now() - (el.__t0 || 0));
    if (left > 0) setTimeout(function(){ unlock(el); }, left);
    else unlock(el);
  }
  document.addEventListener('click', function(e){
    var el = pick(e.target);
    if (!el) return;
    if (el.__busy){                                          /* 锁定中：吞掉后续点击 */
      e.preventDefault(); e.stopPropagation();
      if (e.stopImmediatePropagation) e.stopImmediatePropagation();
      return;
    }
    lock(el); lastEl = el;
    release(el);                                             /* 同步操作：保留最短加载态 */
  }, true);
  if (window.fetch && !window.__fetchWrapped){               /* 异步请求期间延长加载态 */
    window.__fetchWrapped = true;
    var _fetch = window.fetch;
    window.fetch = function(){
      var el = lastEl;
      if (el) { if (!el.__busy) lock(el); }
      var p = _fetch.apply(this, arguments);
      var done = function(){ release(el); };
      try { p.then(done, done); } catch(err){ done(); }
      return p;
    };
  }
})();
function pstUrl(){
  /* 每次打开都带新的防缓存参数，服务端在 B/C 两版中随机返回 */
  return '/api/poster?_r='+Date.now()+Math.random().toString(36).slice(2,8)+'&t='+Date.now();
}
var pstTick=null, pstCapT=null, pstWatchT=null, pstDoneT=null, pstP=0;
function pstPaint(v){
  pstP=v;
  var b=document.getElementById('pstBar'), t=document.getElementById('pstPct');
  if(b) b.style.width=(v>100?100:v)+'%';
  if(t) t.textContent=Math.round(v)+'%';
}
function pstClear(){
  if(pstTick){clearInterval(pstTick);pstTick=null;}
  if(pstCapT){clearTimeout(pstCapT);pstCapT=null;}
  if(pstWatchT){clearTimeout(pstWatchT);pstWatchT=null;}
  if(pstDoneT){clearTimeout(pstDoneT);pstDoneT=null;}
}
function pstMode(mode,why){
  var w=document.getElementById('pstImgWrap'), tip=document.getElementById('pstTip');
  if(w){ w.classList.toggle('ready',mode==='ready'); w.classList.toggle('fail',mode==='fail'); }
  if(tip){
    if(mode==='fail') tip.innerHTML = (why==='error') ? '生成失败，<b>点击重试</b>' : '生成超时，<b>点击重试</b>';
    else tip.innerHTML = '<b>正在绘制</b> 你的专属海报';
  }
}
function pstRun(){
  /* 接口是一次性出图，拿不到真实进度：前段快、后段衰减逼近上限 */
  var cap=86;
  pstClear();
  pstCapT=setTimeout(function(){ cap=96; }, 2300);
  pstTick=setInterval(function(){
    if(pstP>=cap) return;
    pstPaint(pstP+(cap-pstP)*0.10+0.6);
  },150);
}
function pstLoad(u){
  var w=document.getElementById('pstImgWrap'), im=document.getElementById('pstImg'), sv=document.getElementById('pstSave');
  if(!im) return;
  pstClear();
  pstMode('loading'); pstPaint(8);
  if(sv) sv.classList.add('dis');
  im.onload=function(){
    pstClear();
    pstPaint(100);
    if(sv) sv.classList.remove('dis');
    pstDoneT=setTimeout(function(){ pstMode('ready'); }, 260);
  };
  im.onerror=function(){
    pstClear(); pstMode('fail','error');
  };
  pstWatchT=setTimeout(function(){
    if(w && w.classList.contains('ready')) return;
    pstClear(); pstMode('fail','timeout');
  },18000);
  im.src=u;
  pstRun();
}
function openPoster(){
  var m=document.getElementById('pstMask'), p=document.getElementById('pstPanel');
  var im=document.getElementById('pstImg'), sv=document.getElementById('pstSave');
  if(!m||!p||!im) return;
  var u=pstUrl();
  if(sv) sv.href=u;
  m.classList.add('show'); p.classList.add('show');
  document.body.style.overflow='hidden';
  pstLoad(u);
}
function closePoster(){
  var m=document.getElementById('pstMask'), p=document.getElementById('pstPanel');
  if(m) m.classList.remove('show');
  if(p) p.classList.remove('show');
  document.body.style.overflow='';
  pstClear();
}
(function(){
  /* 超时后点占位区重试 */
  var hold=document.getElementById('pstHold');
  if(hold) hold.addEventListener('click', function(){
    var w=document.getElementById('pstImgWrap');
    if(!w || !w.classList.contains('fail')) return;
    var u=pstUrl(), sv=document.getElementById('pstSave');
    if(sv) sv.href=u;
    pstLoad(u);
  });
})();
(function(){
  var item=document.getElementById('miPoster');
  if(item) item.addEventListener('click', function(){ closeMenu(); openPoster(); });
  var mk=document.getElementById('pstMask');
  if(mk) mk.addEventListener('click', closePoster);
  var cl=document.getElementById('pstClose');
  if(cl) cl.addEventListener('click', closePoster);
  var sv=document.getElementById('pstSave');
  if(sv) sv.addEventListener('click', function(e){
    if(!(window.fetch && window.URL && URL.createObjectURL)) return;
    e.preventDefault();
    fetch(pstUrl()).then(function(r){ return r.blob(); }).then(function(b){
      var u=URL.createObjectURL(b), a=document.createElement('a');
      a.href=u; a.download='PPTAROT-分享海报.jpg';
      document.body.appendChild(a); a.click();
      setTimeout(function(){ URL.revokeObjectURL(u); a.remove(); }, 900);
    }).catch(function(){ window.open('/api/poster','_blank'); });
  });
})();
function closeMenu(){
  var p=document.getElementById('mPanel'), m=document.getElementById('mMask');
  if(p) p.classList.remove('show');
  if(m) m.classList.remove('show');
}
(function(){
  var b=document.getElementById('btnMenu');
  if(b) b.addEventListener('click', function(ev){
    ev.stopPropagation();
    var p=document.getElementById('mPanel'), mk=document.getElementById('mMask');
    var on = !p.classList.contains('show');
    p.classList.toggle('show', on); mk.classList.toggle('show', on);
  });
})();

var CARDS = /*__FRONT_CARDS__*/[];
var WECHAT = "__WECHAT__";

var deckEl = document.getElementById("deck");
var stage = document.getElementById("stage");
var hint = document.getElementById("hint");
var cntEl = document.getElementById("cnt");
var posMap = {};
var onTable = 0;
var zTop = 10;
var Z_MIN = 10, Z_MAX = 96;
function nextZ(){
  zTop = (zTop >= Z_MAX) ? Z_MIN : zTop + 1;
  return zTop;
}
function resetZ(){ zTop = Z_MIN; }
var drag = null;

function rnd(n){
  if (window.crypto && window.crypto.getRandomValues && n > 1){
    var a = new Uint32Array(1);
    var lim = Math.floor(4294967296 / n) * n;
    var guard = 0;
    do { window.crypto.getRandomValues(a); guard++; } while (a[0] >= lim && guard < 100);
    return a[0] % n;
  }
  return Math.floor(Math.random() * n);
}
function shuffle(a){
  for (var i = a.length - 1; i > 0; i--){
    var j = rnd(i + 1);
    var t = a[i]; a[i] = a[j]; a[j] = t;
  }
  return a;
}
function updCnt(){
  cntEl.textContent = "已选 " + onTable + " 张 · 共 " + CARDS.length + " 张";
}
function resetDeck(){
  var order = [];
  for (var i = 0; i < CARDS.length; i++) order.push(i);
  shuffle(order);
  posMap = {};
  for (var k = 0; k < CARDS.length; k++) posMap[k] = rnd(2) ? "逆" : "正";
  deckEl.innerHTML = "";
  var df = document.createDocumentFragment();
  for (var m = 0; m < order.length; m++){
    var d = document.createElement("div");
    d.className = "dcard";
    d.setAttribute("data-ci", order[m]);
    d.innerHTML = '<b class="dno">' + (m + 1) + '</b><i>PP</i>';
    df.appendChild(d);
  }
  deckEl.appendChild(df);
  deckEl.scrollLeft = 0;
}
function markTaken(ci){
  var ds = deckEl.querySelectorAll('.dcard');
  for (var i = 0; i < ds.length; i++){
    if (ds[i].getAttribute('data-ci') === String(ci)) ds[i].classList.add('taken');
  }
}
function releaseSlot(ci){
  var ds = deckEl.querySelectorAll('.dcard');
  for (var i = 0; i < ds.length; i++){
    if (ds[i].getAttribute('data-ci') === String(ci)) ds[i].classList.remove('taken');
  }
}
function releaseAll(){
  var ds = deckEl.querySelectorAll('.dcard.taken');
  for (var i = 0; i < ds.length; i++) ds[i].classList.remove('taken');
}
function addCard(ci, cx, cy){
  var t = document.createElement("div");
  t.className = "tcard";
  t.setAttribute("data-ci", ci);
  var pos = posMap[ci] || "正";
  t.innerHTML = '<div class="inner"><div class="back"><i>PPTAROT</i></div>' +
    '<div class="face' + (pos === "逆" ? " rev" : "") + '"><img src="' + CARDS[ci].u +
    '" alt="" draggable="false"></div></div><button class="del">×</button>';
  stage.appendChild(t);
  var w = t.offsetWidth || 64, h = t.offsetHeight || 110;
  var r = stage.getBoundingClientRect();
  var left, top;
  if (typeof cx === "number" && typeof cy === "number"){
    left = cx - r.left - w / 2;
    top = cy - r.top - h / 2;
  } else {
    left = r.width / 2 - w / 2 + (rnd(90) - 45);
    top = r.height / 2 - h / 2 + (rnd(90) - 45);
  }
  left = Math.max(-w * 0.12, Math.min(r.width - w * 0.88, left));
  top = Math.max(-h * 0.12, Math.min(r.height - h * 0.88, top));
  t.style.left = left + "px";
  t.style.top = top + "px";
  t.style.zIndex = String(nextZ());
  onTable++;
  markTaken(ci);
  hint.style.display = "none";
  updCnt();
  return t;
}
function clearTable(){
  var ts = stage.querySelectorAll(".tcard");
  for (var i = 0; i < ts.length; i++) ts[i].parentNode.removeChild(ts[i]);
  onTable = 0;
  resetZ();
  releaseAll();
  hint.style.display = "";
  updCnt();
}
function showMeaning(ci){
  var c = CARDS[ci];
  var pos = posMap[ci] || "正";
  document.getElementById("mName").textContent = c.n;
  document.getElementById("mPos").textContent = pos === "正" ? "正 位" : "逆 位";
  document.getElementById("mKw").textContent = pos === "正" ? c.k : c.kr;
  document.getElementById("meanMask").classList.add("on");
}

document.addEventListener("pointerdown", function(e){
  var del = e.target.classList && e.target.classList.contains("del");
  if (del) return;
  var t = e.target.closest ? e.target.closest(".tcard") : null;
  if (t && t.parentNode === stage){
    var r = t.getBoundingClientRect();
    drag = { el: t, dx: e.clientX - r.left, dy: e.clientY - r.top,
             moved: false, sx: e.clientX, sy: e.clientY };
    t.style.zIndex = String(nextZ());
    e.preventDefault();
    return;
  }
}, { passive: false });

document.addEventListener("pointermove", function(e){
  if (!drag) return;
  var mx = Math.abs(e.clientX - drag.sx) + Math.abs(e.clientY - drag.sy);
  if (!drag.moved && mx > 6) drag.moved = true;
  if (!drag.moved) return;
  var r = stage.getBoundingClientRect();
  var w = drag.el.offsetWidth, h = drag.el.offsetHeight;
  var left = e.clientX - r.left - drag.dx;
  var top = e.clientY - r.top - drag.dy;
  left = Math.max(-w * 0.35, Math.min(r.width - w * 0.65, left));
  top = Math.max(-h * 0.35, Math.min(r.height - h * 0.65, top));
  drag.el.style.left = left + "px";
  drag.el.style.top = top + "px";
  e.preventDefault();
}, { passive: false });

document.addEventListener("pointerup", function(e){
  if (!drag) return;
  var el = drag.el, moved = drag.moved;
  if (moved){
    var r = stage.getBoundingClientRect();
    var w = el.offsetWidth, h = el.offsetHeight;
    var L = parseFloat(el.style.left) || 0;
    var T = parseFloat(el.style.top) || 0;
    el.style.left = Math.max(-w * 0.15, Math.min(r.width - w * 0.85, L)) + "px";
    el.style.top = Math.max(-h * 0.15, Math.min(r.height - h * 0.85, T)) + "px";
  } else {
    if (!el.classList.contains("flip")){
      el.classList.add("flip");
      try {
        var _ci = parseInt(el.getAttribute("data-ci"), 10);
        var _c = CARDS[_ci], _pos = posMap[_ci] === "逆" ? "逆位" : "正位";
        if (_c && typeof trackEvent === "function"){
          trackEvent("draw", {
            cat: curCat || "",
            result: _c.n + " · " + _pos,
            detail: { 牌名: _c.n, 位置: _pos, 关键词: posMap[_ci] === "逆" ? _c.kr : _c.k,
                      分类: curCat ? catName(curCat) : "未选" }
          });
        }
      } catch(e){}
    }
    else showMeaning(parseInt(el.getAttribute("data-ci"), 10));
  }
  drag = null;
});

/* ===== 拖拽抽牌：按住牌堆里的牌拖到桌面才落牌 ===== */
var pick = null, lastDraw = 0, ghostEl = null;
function ghostShow(){
  if (ghostEl) return;
  ghostEl = document.createElement("div");
  ghostEl.className = "pickGhost";
  ghostEl.innerHTML = "<i>PP</i>";
  document.body.appendChild(ghostEl);
}
function ghostMove(x, y){
  if (!ghostEl) return;
  ghostEl.style.left = x + "px";
  ghostEl.style.top = y + "px";
}
function ghostKill(){
  if (ghostEl && ghostEl.parentNode) ghostEl.parentNode.removeChild(ghostEl);
  ghostEl = null;
}
document.addEventListener("pointerdown", function(e){
  if (deckAnim) return;
  var d = e.target.closest ? e.target.closest(".dcard") : null;
  if (!d) return;
  if (Date.now() - lastDraw < 300) return;
  if (d.classList.contains("taken")) return;
  var ci = parseInt(d.getAttribute("data-ci"), 10);
  if (isNaN(ci)) return;
  pick = { ci: ci, sx: e.clientX, sy: e.clientY, on: false };
}, { passive: true });

document.addEventListener("pointermove", function(e){
  if (!pick) return;
  var mx = Math.abs(e.clientX - pick.sx), my = Math.abs(e.clientY - pick.sy);
  if (!pick.on){
    if (mx < 8 && my < 8) return;
    /* 横向或斜向滑动优先交给牌堆滚动，只有明显纵向才判定为拖牌 */
    if (mx >= my * 0.9){ pick = null; ghostKill(); return; }
    pick.on = true;
    ghostShow();
  }
  ghostMove(e.clientX, e.clientY);
  e.preventDefault();
}, { passive: false });

/* 浏览器接管横向滚动会触发 pointercancel，清掉拖牌状态避免残留 */
document.addEventListener("pointercancel", function(){
  pick = null;
  ghostKill();
}, { passive: true });

document.addEventListener("pointerup", function(e){
  if (!pick) return;
  var ci = pick.ci, on = pick.on;
  pick = null;
  ghostKill();
  if (!on) return;
  var r = stage.getBoundingClientRect();
  if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) return;
  lastDraw = Date.now();
  addCard(ci, e.clientX, e.clientY);
}, { passive: true });

document.addEventListener("pointercancel", function(){
  pick = null;
  ghostKill();
}, { passive: true });

stage.addEventListener("click", function(e){
  if (e.target.classList && e.target.classList.contains("del")){
    var t = e.target.closest(".tcard");
    if (t){
      var ci = parseInt(t.getAttribute("data-ci"), 10);
      t.parentNode.removeChild(t);
      if (!isNaN(ci)) releaseSlot(ci);
      onTable = Math.max(0, onTable - 1);
      if (!onTable) hint.style.display = "";
      updCnt();
    }
  }
});

var CF_CB = null;
function askConfirm(title, msg, okText, onOk){
  document.getElementById("cfTitle").textContent = title;
  document.getElementById("cfMsg").textContent = msg;
  document.getElementById("cfOk").textContent = okText;
  CF_CB = onOk || null;
  document.getElementById("cfMask").classList.add("on");
}
function closeConfirm(){
  document.getElementById("cfMask").classList.remove("on");
  CF_CB = null;
}
document.getElementById("cfCancel").onclick = function(){ closeConfirm(); };
document.getElementById("cfOk").onclick = function(){
  var cb = CF_CB;
  closeConfirm();
  if (cb) cb();
};
document.getElementById("cfMask").addEventListener("click", function(e){
  if (e.target === this) closeConfirm();
});

var deckAnim = false;
function playDealAnim(done){
  var vd = document.getElementById("view-draw");
  if (deckAnim || !vd || vd.style.display === "none") return;
  var layer = document.getElementById("shfLayer");
  var stEl = document.getElementById("stage");
  if (!layer || !stEl) return;
  deckAnim = true;
  var finished = false;
  function finish(){
    if (finished) return;
    finished = true;
    try { layer.innerHTML = ""; } catch(e){}
    if (done) { try { done(); } catch(e){} }
    try { deckEl.classList.remove("deckHide"); } catch(e){}
    try { updCnt(); } catch(e){}
    deckAnim = false;
  }
  try {
    cntEl.textContent = "洗牌中…";
    var vdR = vd.getBoundingClientRect();
    var stR = stEl.getBoundingClientRect();
    var dkR = deckEl.getBoundingClientRect();
    var CW = 46, CH = 79, N = 46;
    var cx = Math.round(stR.left - vdR.left + stR.width / 2 - CW / 2);
    var cy = Math.round(stR.top - vdR.top + stR.height / 2 - CH / 2);
    var tx = Math.round(dkR.left - vdR.left + dkR.width / 2 - CW / 2);
    var ty = Math.round(dkR.top - vdR.top + dkR.height / 2 - CH / 2);
    var dx = tx - cx, dy = ty - cy;
    /* 飞散半径按桌面实际尺寸取满，四周留安全边 */
    var maxRx = Math.max(60, stR.width / 2 - CW / 2 - 6);
    var maxRy = Math.max(44, stR.height / 2 - CH / 2 - 6);
    var S_DUR = 900, C_DUR = 520, STAG = 8;
    layer.innerHTML = "";
    deckEl.classList.add("deckHide");
    var list = [], i;
    for (i = 0; i < N; i++){
      var el = document.createElement("div");
      el.className = "sc";
      el.textContent = "PP";
      el.style.left = cx + "px";
      el.style.top = cy + "px";
      el.style.zIndex = String(i + 1);
      el.style.opacity = "1";
      layer.appendChild(el);
      list.push(el);
    }
    if (!list[0] || !list[0].animate){ finish(); return; }
    for (i = 0; i < N; i++){
      (function(card, idx){
        var ang = (idx / N) * Math.PI * 2 + (Math.random() - 0.5) * 0.5;
        var px = Math.cos(ang), py = Math.sin(ang);
        var k = 1 / Math.max(Math.abs(px), Math.abs(py));
        var rad = 0.84 + Math.random() * 0.16;
        var ox = Math.round(px * k * maxRx * rad);
        var oy = Math.round(py * k * maxRy * rad);
        var rot = Math.round((Math.random() * 2 - 1) * 68);
        var jx = Math.round((Math.random() * 2 - 1) * 30);
        var jy = Math.round((Math.random() * 2 - 1) * 22);
        var dep = 0.90 + Math.random() * 0.20;   /* 远近层次，视觉更密 */
        card.animate([
          {transform:"translate(0px,0px) rotate(0deg) scale(.86)", opacity:0},
          {transform:"translate(" + Math.round(ox * .42) + "px," + Math.round(oy * .42) + "px) rotate(" + Math.round(rot * .5) + "deg) scale(" + (1.06 * dep).toFixed(2) + ")", opacity:1, offset:.16},
          {transform:"translate(" + ox + "px," + oy + "px) rotate(" + rot + "deg) scale(" + (1.0 * dep).toFixed(2) + ")", opacity:1, offset:.40},
          {transform:"translate(" + (ox + jx) + "px," + (oy + jy) + "px) rotate(" + Math.round(rot * 1.24) + "deg) scale(" + (0.97 * dep).toFixed(2) + ")", opacity:1, offset:.64},
          {transform:"translate(" + Math.round(dx * .62) + "px," + Math.round(dy * .62 - 10) + "px) rotate(" + Math.round(rot * .45) + "deg) scale(.94)", opacity:.92, offset:.86},
          {transform:"translate(" + dx + "px," + dy + "px) rotate(0deg) scale(.86)", opacity:.22, offset:1}
        ], {duration:S_DUR + C_DUR, delay:idx * STAG, easing:"cubic-bezier(.22,.68,.28,1)", fill:"both"});
      })(list[i], i);
    }
    var T_TOTAL = S_DUR + C_DUR + (N - 1) * STAG + 60;
    setTimeout(finish, T_TOTAL);
    setTimeout(finish, T_TOTAL + 900);
  } catch(err){
    finish();
  }
}
function playShuffleAnim(done){ playDealAnim(done); }

document.getElementById("btnShuffle").onclick = function(){
  if (deckAnim) return;
  var n = onTable || 0;
  var msg = n > 0
    ? "桌面上已有 " + n + " 张牌，洗牌会把它们收走，牌堆重新打乱。确定洗牌吗？"
    : "牌堆会重新打乱，顺序不可还原。确定洗牌吗？";
  askConfirm("洗牌", msg, "洗牌", function(){
    /* 洗牌动画开始前先把桌面上的旧牌全部撤下，避免动画与旧牌同屏 */
    clearTable();
    playShuffleAnim(function(){
      resetDeck();
    });
  });
};
document.getElementById("btnClear").onclick = function(){ clearTable(); };

document.getElementById("btnPP").onclick = function(){
  document.getElementById("ppMask").classList.add("on");
};
document.getElementById("ppClose").onclick = function(){
  document.getElementById("ppMask").classList.remove("on");
};
document.getElementById("mClose").onclick = function(){
  document.getElementById("meanMask").classList.remove("on");
};
document.getElementById("ppMask").addEventListener("click", function(e){
  if (e.target === this) this.classList.remove("on");
});
document.getElementById("mMask").addEventListener("click", function(){
  closeMenu();
});
document.addEventListener("pointerdown", function(e){
  var p = document.getElementById("mPanel");
  var b = document.getElementById("btnMenu");
  if (!p || !p.classList.contains("show")) return;
  if (p.contains(e.target)) return;
  if (b && (b === e.target || b.contains(e.target))) return;
  closeMenu();
}, true);
document.getElementById("meanMask").addEventListener("click", function(e){
  if (e.target === this) this.classList.remove("on");
});
document.getElementById("wxText").textContent = WECHAT;
document.getElementById("btnCopy").onclick = function(){
  var ok = document.getElementById("copyok");
  function done(){ ok.textContent = "已复制，去微信搜一下就能加我"; }
  function fallback(){
    var ta = document.createElement("textarea");
    ta.value = WECHAT;
    ta.style.position = "fixed";
    ta.style.left = "-999px";
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand("copy") ? done() : (ok.textContent = "长按上方微信号手动复制");
    } catch (err) {
      ok.textContent = "长按上方微信号手动复制";
    }
    document.body.removeChild(ta);
  }
  ok.textContent = "";
  if (navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(WECHAT).then(done, fallback);
  } else fallback();
};

/* ==================== 答案之书 ==================== */
var ANS = [
 {t:'别太赶了。', e:'', n:''},
 {t:'别想了。', e:'', n:''},
 {t:'不。', e:'', n:''},
 {t:'不然呢？', e:'', n:''},
 {t:'不要抱期望。', e:'', n:''},
 {t:'要求不要太高。', e:'', n:''},
 {t:'这是必然的，不要抗拒。', e:'', n:''},
 {t:'不要浪费精力。', e:'', n:''},
 {t:'不要浪费你的时间了。', e:'', n:''},
 {t:'不要做得过火了。', e:'', n:''},
 {t:'不用担心。', e:'', n:''},
 {t:'车到山前必有路。', e:'', n:''},
 {t:'答案就在你身边。', e:'', n:''},
 {t:'大胆一点。', e:'', n:''},
 {t:'大方一点。', e:'', n:''},
 {t:'等等。', e:'', n:''},
 {t:'放轻松点，慢慢来。', e:'', n:''},
 {t:'管它呢。', e:'', n:''},
 {t:'毫无疑问。', e:'', n:''},
 {t:'好运将会降临。', e:'', n:''},
 {t:'忽略了一件显而易见的事。', e:'', n:''},
 {t:'换个角度想想。', e:'', n:''},
 {t:'会付出代价。', e:'', n:''},
 {t:'会感到庆幸。', e:'', n:''},
 {t:'会很不顺利。', e:'', n:''},
 {t:'会很顺利。', e:'', n:''},
 {t:'会后悔的。', e:'', n:''},
 {t:'会失去自我。', e:'', n:''},
 {t:'会特别顺利。', e:'', n:''},
 {t:'继续前进。', e:'', n:''},
 {t:'结果可能让人惊讶。', e:'', n:''},
 {t:'绝对不。', e:'', n:''},
 {t:'肯定的。', e:'', n:''},
 {t:'没错。', e:'', n:''},
 {t:'木已成舟。', e:'', n:''},
 {t:'你必须解决一些相关的问题。', e:'', n:''},
 {t:'不会后悔的。', e:'', n:''},
 {t:'不会失望的。', e:'', n:''},
 {t:'得真正地努力一下。', e:'', n:''},
 {t:'还有别的选择。', e:'', n:''},
 {t:'你将取得成功。', e:'', n:''},
 {t:'你说了算。', e:'', n:''},
 {t:'你心里已经有答案了。', e:'', n:''},
 {t:'需要合作。', e:'', n:''},
 {t:'需要冒险。', e:'', n:''},
 {t:'要主动。', e:'', n:''},
 {t:'你在开玩笑吗？', e:'', n:''},
 {t:'你做什么都没用。', e:'', n:''},
 {t:'奇迹即将降临。', e:'', n:''},
 {t:'千万别信。', e:'', n:''},
 {t:'千万不能失败。', e:'', n:''},
 {t:'全力以赴。', e:'', n:''},
 {t:'认清现实吧。', e:'', n:''},
 {t:'三思而后行。', e:'', n:''},
 {t:'尚待时日。', e:'', n:''},
 {t:'省点力气吧。', e:'', n:''},
 {t:'时机未到。', e:'', n:''},
 {t:'听听别人怎么说。', e:'', n:''},
 {t:'听听专家的意见。', e:'', n:''},
 {t:'万一错过，就没这个机会了。', e:'', n:''},
 {t:'为什么不呢？', e:'', n:''},
 {t:'问问你的亲人。', e:'', n:''},
 {t:'问问自己，为什么要这么干。', e:'', n:''},
 {t:'先做点别的。', e:'', n:''},
 {t:'现在还说不清。', e:'', n:''},
 {t:'现在你可以。', e:'', n:''},
 {t:'相信你的直觉。', e:'', n:''},
 {t:'相信你最初的想法。', e:'', n:''},
 {t:'想得美。', e:'', n:''},
 {t:'想想有没有机会。', e:'', n:''},
 {t:'休息一下就好了。', e:'', n:''},
 {t:'学会妥协。', e:'', n:''},
 {t:'眼光长远一点。', e:'', n:''},
 {t:'要变通。', e:'', n:''},
 {t:'要有点耐心。', e:'', n:''},
 {t:'要知足。', e:'', n:''},
 {t:'要抓住问题的关键。', e:'', n:''},
 {t:'一定会有好结果的。', e:'', n:''},
 {t:'一笑了之。', e:'', n:''},
 {t:'以后再说。', e:'', n:''},
 {t:'用尽一切办法去努力。', e:'', n:''},
 {t:'有。', e:'', n:''},
 {t:'有可能。', e:'', n:''},
 {t:'仔细想想再说。', e:'', n:''},
 {t:'再等等看。', e:'', n:''},
 {t:'障碍重重。', e:'', n:''},
 {t:'这辈子都不可能。', e:'', n:''},
 {t:'这不可取。', e:'', n:''},
 {t:'这不切实际。', e:'', n:''},
 {t:'这不值得努力。', e:'', n:''},
 {t:'这会影响你的形象。', e:'', n:''},
 {t:'这件事会很麻烦。', e:'', n:''},
 {t:'这件事你说了不算。', e:'', n:''},
 {t:'这没什么意义。', e:'', n:''},
 {t:'这取决于你的行动。', e:'', n:''},
 {t:'这是肯定的。', e:'', n:''},
 {t:'没法保证。', e:'', n:''},
 {t:'无法预测。', e:'', n:''},
 {t:'这是在浪费金钱。', e:'', n:''},
 {t:'没什么好结果。', e:'', n:''},
 {t:'值得奋斗。', e:'', n:''},
 {t:'这种事情不要告诉别人。', e:'', n:''},
 {t:'只有一次机会。', e:'', n:''},
 {t:'众所周知。', e:'', n:''},
 {t:'重新想想。', e:'', n:''},
 {t:'注意细节。', e:'', n:''},
 {t:'做最坏的打算。', e:'', n:''},
 {t:'不要纠结了。', e:'', n:''},
 {t:'毫无道理。', e:'', n:''},
 {t:'结果会让你惊喜。', e:'', n:''},
 {t:'这不是你想要的。', e:'', n:''},
 {t:'寻找机会就行。', e:'', n:''},
 {t:'不要自作多情。', e:'', n:''},
 {t:'最后一次机会。', e:'', n:''},
 {t:'顺其自然。', e:'', n:''},
 {t:'学会释然。', e:'', n:''},
 {t:'别瞎折腾了。', e:'', n:''},
 {t:'再过几年。', e:'', n:''},
 {t:'不要忽视自己的力量。', e:'', n:''},
 {t:'尽在掌握之中。', e:'', n:''},
 {t:'地点不合适。', e:'', n:''},
 {t:'不作死就不会死。', e:'', n:''},
 {t:'当局者迷。', e:'', n:''},
 {t:'另择吉日。', e:'', n:''},
 {t:'时间会证明一切。', e:'', n:''},
 {t:'并非永恒。', e:'', n:''},
 {t:'倾听你内心的声音。', e:'', n:''},
 {t:'如你所愿。', e:'', n:''},
 {t:'遇上方知有。', e:'', n:''},
 {t:'不值得。', e:'', n:''},
 {t:'见好就收。', e:'', n:''},
 {t:'你猜。', e:'', n:''},
 {t:'时机尚不成熟。', e:'', n:''},
 {t:'这难以置信。', e:'', n:''},
 {t:'与你无关。', e:'', n:''},
 {t:'放手。', e:'', n:''},
 {t:'拭目以待。', e:'', n:''}
];
var ansBusy = false, ansLast = -1;
function ansDust(id){
  var box = document.getElementById(id || "ansDust");
  if (!box || box.getAttribute("data-done")) return;
  var h = "";
  for (var i = 0; i < 16; i++){
    var x = (i * 6.4 + 3) % 96;
    var bt = (i % 5) * 14;
    var dur = (4.4 + (i % 6) * 0.9).toFixed(1);
    var del = ((i % 8) * 0.55).toFixed(2);
    h += '<i style="left:' + x.toFixed(1) + '%;bottom:' + bt + 'px;animation-duration:' + dur
      + 's;animation-delay:' + del + 's"></i>';
  }
  box.innerHTML = h;
  box.setAttribute("data-done", "1");
}
/* ==================== 星骰 ==================== */
var DC_P = [
 {s:'☉',fs:25,k:'想被看见',t:'你想的不是躲开，是被承认。这事的动力，是你要在别人眼里有个位置。'},
 {s:'☽',fs:25,k:'情绪先动',t:'你心里其实早有答案，只是不敢承认。情绪已经替你做选择了。'},
 {s:'☿',fs:25,k:'话没说透',t:'卡在沟通，不在人心。你想说的和说出口的，差了一截。'},
 {s:'♀',fs:25,k:'想被喜欢',t:'你要的是舒服和被选中。别把"想被选"错当成"想要"。'},
 {s:'♂',fs:25,k:'憋着一口气',t:'你不是犹豫，是不想再忍。这股火是真的，别压。'},
 {s:'♃',fs:25,k:'想往外走',t:'你嫌现在的盘子太小。想扩是真念头，不是空想。'},
 {s:'♄',fs:25,k:'怕承担结果',t:'你拖着不动，不是懒，是怕错了要认账。'},
 {s:'♅',fs:25,k:'想掀桌',t:'你受够一成不变，哪怕代价是重来一遍。'},
 {s:'♆',fs:25,k:'自己编故事',t:'你看到的多半是你希望的样子，不是它实际的样子。'},
 {s:'♇',fs:25,k:'不得不变',t:'已经压到底了。你等的不是答案，是一个能翻脸的契机。'}
];
var DC_S = [
 {s:'♈',fs:30,k:'来得快',t:'来得快，说干就干，别指望它有耐心。'},
 {s:'♉',fs:30,k:'慢慢磨',t:'慢，但一动就不回头。催不来。'},
 {s:'♊',fs:30,k:'先打听',t:'先聊、先试、先打听，边问边看，别急着定性。'},
 {s:'♋',fs:30,k:'绕回旧事',t:'会绕回旧人旧事，情绪一牵就软。'},
 {s:'♌',fs:30,k:'摊到台面',t:'会摊到台面上，谁看见很重要。'},
 {s:'♍',fs:30,k:'抠细节',t:'抠细节。你会反复核对，直到某一处对不上。'},
 {s:'♎',fs:30,k:'二选一',t:'卡在二选一。你怕得罪人，所以一直不定。'},
 {s:'♏',fs:30,k:'暗着来',t:'不摊开，暗着来。表面没事，底下翻得厉害。'},
 {s:'♐',fs:30,k:'往外跑',t:'往外跑。换个地方、换个人，气就顺了。'},
 {s:'♑',fs:30,k:'算成本',t:'讲条件、算成本。没实际好处，你不会动。'},
 {s:'♒',fs:30,k:'反着来',t:'反着来。别人劝你往东，你偏想往西。'},
 {s:'♓',fs:30,k:'心太软',t:'容易心软，也容易自己骗自己。'}
];
var DC_H = [
 {s:'1',fs:27,k:'你自己',t:'你自己。状态、外表、别人第一眼看你的样子。'},
 {s:'2',fs:27,k:'钱和底气',t:'钱和底气。手里有多少，敢不敢花。'},
 {s:'3',fs:27,k:'说话和消息',t:'说话和消息。等一个回信、一次摊牌，都在这。'},
 {s:'4',fs:27,k:'家里',t:'家里。根上的安全感，绕不开家里人。'},
 {s:'5',fs:27,k:'恋爱与创作',t:'恋爱、玩、创作。喜欢就是喜欢，藏不住。'},
 {s:'6',fs:27,k:'日常与活儿',t:'日常和活儿。琐碎的事在磨你。'},
 {s:'7',fs:27,k:'一对一',t:'一对一。对象、合伙人，还有那个让你来问的人。'},
 {s:'8',fs:27,k:'搅在一起的账',t:'搅在一起的钱和亲密关系，那些说不清的账。'},
 {s:'9',fs:27,k:'远方',t:'远方、考试、下一步去哪。你想走得更远。'},
 {s:'10',fs:22,k:'事业名声',t:'事业和名声。你要被谁认下来。'},
 {s:'11',fs:22,k:'朋友与圈子',t:'朋友和圈子。机会藏在人群里。'},
 {s:'12',fs:22,k:'心结旧账',t:'看不见的那部分。心结、旧账、自己跟自己较劲。'}
];
var dcBusy = false, dcLast = [-1, -1, -1];
function dcDust(){ ansDust("dcDust"); }
function dcRand(len, last){
  var p = Math.floor(Math.random() * len);
  if (len > 1 && p === last) p = (p + 1) % len;
  return p;
}
function dcSpin(i, pool, delay, onDone){
  var cube = document.getElementById("dcCube" + i);
  var face = cube.querySelector("span") || cube;
  var pick = dcRand(pool.length, dcLast[i]);
  dcLast[i] = pick;
  cube.classList.add("roll");
  var timer = setInterval(function(){
    face.textContent = pool[Math.floor(Math.random() * pool.length)].s;
  }, 70);
  setTimeout(function(){
    clearInterval(timer);
    cube.classList.remove("roll");
    var it = pool[pick];
    face.textContent = it.s;
    face.style.fontSize = it.fs + "px";
    cube.classList.add("lit");
    setTimeout(function(){ cube.classList.remove("lit"); }, 700);
    onDone(pick);
  }, delay);
}
function diceGo(){
  if (dcBusy) return;
  dcBusy = true;
  var b = document.getElementById("btnDiceGo");
  b.disabled = true;
  b.textContent = "星骰在转…";
  document.getElementById("dcRes").classList.remove("on");
  var picks = [0, 0, 0];
  dcSpin(0, DC_P, 850, function(i){ picks[0] = i; });
  dcSpin(1, DC_S, 1250, function(i){ picks[1] = i; });
  dcSpin(2, DC_H, 1650, function(i){ picks[2] = i; setTimeout(function(){ dcShow(picks); }, 140); });
}
function dcShow(picks){
  var p = DC_P[picks[0]], s = DC_S[picks[1]], h = DC_H[picks[2]];
  var q = (document.getElementById("dcQInput").value || "").trim();
  document.getElementById("dcQTxt").textContent = q ? ("你问的是：「" + q + "」") : "你没写问题，那就当是你心里那句";
  document.getElementById("dcTxt0").textContent = p.t;
  document.getElementById("dcTxt1").textContent = s.t;
  document.getElementById("dcTxt2").textContent = h.t;
  document.getElementById("dcLine").textContent = "推你的是「" + p.k + "」，它会在「" + s.k + "」这层落地，位置在「" + h.k + "」。你缺的从来不是答案，是承认它。";
  var res = document.getElementById("dcRes");
  res.classList.add("on");
  try {
    if (typeof trackEvent === "function"){
      trackEvent("dice", {
        q: q,
        result: p.t + " ｜ " + s.t + " ｜ " + h.t,
        detail: { 动力骰: p.t, 落地面: s.t, 位置: h.t,
                  解读: "推你的是「" + p.k + "」，它会在「" + s.k + "」这层落地，位置在「" + h.k + "」" }
      });
    }
  } catch(e){}
  var b = document.getElementById("btnDiceGo");
  b.disabled = false;
  b.textContent = "再掷一次";
  dcBusy = false;
  setTimeout(function(){ try { res.scrollIntoView({behavior:"smooth", block:"nearest"}); } catch(e){} }, 80);
}
function openDice(){
  showView("dice");
  dcDust();
}
function openAnswer(){
  showView("answer");
  ansDust();
}
/* 答案展示不带句号：去掉结尾的中英文句号 */
function ansClean(s){
  return String(s || "").replace(/\s+$/, "").replace(/[。．.]+$/, "").trim();
}
function ansGo(){
  if (ansBusy) return;
  ansBusy = true;
  var b = document.getElementById("btnAnsGo");
  var fly = document.getElementById("ansFly");
  var hint = document.getElementById("ansHint");
  b.disabled = true;
  b.textContent = "蝴蝶飞走了…";
  if (hint) hint.textContent = "别动，听翅膀的声音";
  if (fly) fly.style.transform = "scale(.8)";
  var pick = Math.floor(Math.random() * ANS.length);
  if (ANS.length > 1 && pick === ansLast) pick = (pick + 1) % ANS.length;
  ansLast = pick;
  var it = ANS[pick];
  setTimeout(function(){
    document.getElementById("ansText").textContent = ansClean(it.t);
    var enEl = document.getElementById("ansEn");
    enEl.textContent = it.e || "";
    enEl.style.display = it.e ? "" : "none";
    var noteEl = document.getElementById("ansNote");
    noteEl.textContent = it.n || "";
    noteEl.style.display = it.n ? "" : "none";
    document.getElementById("ansStage").style.display = "none";
    document.getElementById("view-answer").classList.add("hasAns");
    document.getElementById("ansResult").style.display = "flex";
    b.disabled = false;
    b.textContent = "再问一次";
    if (fly) fly.style.transform = "";
    ansBusy = false;
    try {
      if (typeof trackEvent === "function"){
        trackEvent("answer", {
          result: ansClean(it.t),
          detail: { 答案: ansClean(it.t), 英文: it.e || "", 分类: it.n || "" }
        });
      }
    } catch(e){}
  }, 1500);
}
function ansAgain(){
  document.getElementById("view-answer").classList.remove("hasAns");
  document.getElementById("ansResult").style.display = "none";
  document.getElementById("ansStage").style.display = "flex";
  var hint = document.getElementById("ansHint");
  if (hint) hint.textContent = "蝴蝶还停着，答案没起飞";
  var b = document.getElementById("btnAnsGo");
  b.disabled = false;
  b.textContent = "让蝴蝶飞一趟";
  ansDust();
}

/* ==================== 首次抽牌引导 ==================== */
var GD_KEY = "ppt_guide_draw_v1";
var GD_STEPS = [
  { t:"按住牌堆任意一张牌，往上拖到桌面", sel:"#deck", r:16,
    d:"牌堆可左右滑动，查看更多", back:false },
  { t:"抽牌时先深呼吸三次，把心里的问题想清楚", sel:null,
    d:"", back:false },
  { t:"点一下牌面翻牌", sel:"#stage", r:20, box:{w:150,h:230},
    d:"", back:true },
  { t:"详细解牌 · 想问更多", sel:"#btnPP", r:999,
    d:"点击右上角【合作咨询】", back:false }
];
var gdIdx = 0, gdOpenFlag = false, gdBound = false;
function gdEl(id){ return document.getElementById(id); }
function gdPlace(){
  var step = GD_STEPS[gdIdx] || GD_STEPS[0];
  var spot = gdEl("gdSpot"), tip = gdEl("gdTip");
  if (!spot || !tip) return;
  var vw = window.innerWidth, vh = window.innerHeight;
  var tr = null;
  if (step.sel){ try { var el = document.querySelector(step.sel); if (el) tr = el.getBoundingClientRect(); } catch(e){ tr = null; } }
  if (tr && (tr.width < 6 || tr.height < 6)) tr = null;
  var sl, st, sw, sh;
  if (!tr){
    /* 无具体锚点：全屏柔光遮罩，小提示卡居中 */
    sl = vw / 2 - 1; st = vh / 2 - 1; sw = 2; sh = 2;
    spot.className = "gdSpot plain";
    spot.style.borderRadius = "50%";
  } else {
    var pad = 8;
    sl = Math.max(4, tr.left - pad);
    st = Math.max(4, tr.top - pad);
    sw = Math.min(vw - sl - 4, tr.width + pad * 2);
    sh = Math.min(vh - st - 4, tr.height + pad * 2);
    if (step.box){
      /* 目标区域过大时只圈中心一块，避免高亮蔓延整屏 */
      sw = Math.min(sw, step.box.w);
      sh = Math.min(sh, step.box.h);
      sl = Math.max(4, tr.left + tr.width / 2 - sw / 2);
      st = Math.max(4, tr.top + tr.height / 2 - sh / 2);
      if (sl + sw > vw - 4) sl = vw - sw - 4;
      if (st + sh > vh - 4) st = vh - sh - 4;
    }
    spot.className = "gdSpot";
    spot.style.borderRadius = (step.r || 16) + "px";
  }
  spot.classList.toggle("showBack", !!step.back);
  spot.style.left = Math.round(sl) + "px";
  spot.style.top = Math.round(st) + "px";
  spot.style.width = Math.round(sw) + "px";
  spot.style.height = Math.round(sh) + "px";

  var tw = tip.offsetWidth || 300, th = tip.offsetHeight || 210;
  var left, top;
  if (tr){
    var below = st + sh + 22, above = st - 22 - th;
    if (below + th <= vh - 12) top = below;
    else if (above >= 12) top = above;
    else top = Math.max(12, Math.min(vh - th - 12, st + sh / 2 - th / 2));
    left = sl + sw / 2 - tw / 2;
  } else {
    left = vw / 2 - tw / 2;
    top = vh / 2 - th / 2;
  }
  left = Math.max(12, Math.min(vw - tw - 12, left));
  top = Math.max(12, Math.min(vh - th - 12, top));
  /* 提示卡若压到高亮区域，移到高亮框外侧 */
  var hit = function(a, b, c, d){
    return !(c + tw + 10 <= a || c >= a + b + 10 || d + th + 10 <= st || d >= st + sh + 10);
  };
  if (hit(sl, sw, left, top)){
    var cands = [st + sh + 18, st - th - 18, vh - th - 14, 14];
    for (var ci = 0; ci < cands.length; ci++){
      var ct = cands[ci];
      if (ct < 8 || ct + th > vh - 8) continue;
      if (!hit(sl, sw, left, ct)){ top = ct; break; }
    }
  }
  tip.style.left = Math.round(left) + "px";
  tip.style.top = Math.round(top) + "px";
}
function gdRender(){
  var step = GD_STEPS[gdIdx] || GD_STEPS[0];
  var badge = gdEl("gdBadge"), title = gdEl("gdTitle"), text = gdEl("gdText");
  var dots = gdEl("gdDots"), next = gdEl("gdNext"), tip = gdEl("gdTip");
  if (badge) badge.textContent = (gdIdx + 1) + " / " + GD_STEPS.length;
  if (title) title.textContent = step.t;
  if (text){ text.textContent = step.d || ""; text.style.display = step.d ? "" : "none"; }
  if (dots){
    var ks = dots.getElementsByTagName("i");
    for (var i = 0; i < ks.length; i++) ks[i].className = (i === gdIdx) ? "on" : "";
  }
  if (next) next.textContent = (gdIdx === GD_STEPS.length - 1) ? "开始抽牌" : "下一步";
  gdPlace();
  if (tip){
    tip.classList.add("in");
    /* 目标可能在动画/滚动后才稳定，稍后再校正一次 */
    setTimeout(function(){ try { gdPlace(); } catch(e){} }, 320);
  }
}
function gdClose(mark){
  if (!gdOpenFlag) return;
  gdOpenFlag = false;
  var wrap = gdEl("gdWrap"), tip = gdEl("gdTip");
  if (tip) tip.classList.remove("in");
  if (wrap){ wrap.classList.remove("on"); wrap.setAttribute("aria-hidden", "true"); }
  if (mark){
    try { localStorage.setItem(GD_KEY, "1"); } catch(e){}
  }
}
function gdNextStep(){
  if (!gdOpenFlag) return;
  if (gdIdx >= GD_STEPS.length - 1){ gdClose(true); return; }
  gdIdx++;
  var tip = gdEl("gdTip");
  if (tip) tip.classList.remove("in");
  setTimeout(function(){ try { gdRender(); } catch(e){} }, 130);
}
function gdBind(){
  if (gdBound) return;
  gdBound = true;
  var next = gdEl("gdNext"), skip = gdEl("gdSkip"), block = gdEl("gdBlock");
  if (next) next.onclick = function(){ gdNextStep(); };
  if (skip) skip.onclick = function(){ gdClose(true); };
  if (block) block.onclick = function(){ /* 遮罩不响应点击穿透，避免误触底层 */ };
  window.addEventListener("resize", function(){ if (gdOpenFlag) { try { gdPlace(); } catch(e){} } });
  window.addEventListener("scroll", function(){ if (gdOpenFlag) { try { gdPlace(); } catch(e){} } }, true);
}
function gdMaybeShow(){
  var vd = gdEl("view-draw");
  if (!vd || vd.style.display === "none") return;
  var seen = "";
  try { seen = localStorage.getItem(GD_KEY) || ""; } catch(e){ seen = ""; }
  if (seen) return;
  var wrap = gdEl("gdWrap");
  if (!wrap || gdOpenFlag) return;
  gdBind();
  gdIdx = 0;
  gdOpenFlag = true;
  wrap.classList.add("on");
  wrap.setAttribute("aria-hidden", "false");
  gdRender();
}

/* ==================== 视图切换 ==================== */
var VIEWELS = { home: document.getElementById("view-home"), dir: document.getElementById("view-dir"), draw: document.getElementById("view-draw"), fortune: document.getElementById("view-fortune"), astro: document.getElementById("view-astro"), answer: document.getElementById("view-answer"), dice: document.getElementById("view-dice"), daily: document.getElementById("view-daily") };
var curView = "home";
/* 导航历史栈：每次切换视图记下上一页，返回按钮逐层回退 */
var VSTACK = [];
function showView(name, noPush){
  if (!VIEWELS[name]) return;
  if (!noPush && curView !== name){
    VSTACK.push(curView);
    if (VSTACK.length > 24) VSTACK.shift();
  }
  if (name === "home") VSTACK.length = 0;   /* 回首页即清空历史 */
  if (name === "astro"){ try { AP_PANE = ""; AP_SUB.length = 0; } catch(e){} }   /* 进星盘页，内部层级重置 */
  else { try { AP_PANE = ""; AP_SUB.length = 0; } catch(e){} }                  /* 离开星盘页，内部层级一并清掉 */
  curView = name;
  for (var k in VIEWELS){
    if (VIEWELS[k]) VIEWELS[k].style.display = (k === name) ? "flex" : "none";
  }
  var bk = document.getElementById("btnBack");
  if (bk) bk.classList.toggle("on", name !== "home");
  window.scrollTo(0, 0);
  if (name === "home"){ try { fitBnrFly(); } catch(e){} }
  if (name === "daily"){ syncDaily(); }
  if (name === "draw"){
    deckAnim = false;
    try { clearTable(); } catch(e){}   /* 洗牌动画前先撤下桌面旧牌 */
    var fireDeal = function(){
      try { playDealAnim(function(){ resetDeck(); }); } catch(e){ deckAnim = false; }
    };
    requestAnimationFrame(function(){ requestAnimationFrame(fireDeal); });
    setTimeout(fireDeal, 120);
    /* 首次进入抽牌台：洗牌动画落定后再弹引导，避免遮挡落牌观感 */
    setTimeout(function(){ try { if (!deckAnim) gdMaybeShow(); } catch(e){} }, 760);
    setTimeout(function(){ try { gdMaybeShow(); } catch(e){} }, 1400);
  }
  if (name === "astro"){
    loadArch();
  }
}
/* ==================== 首页入口 / 分类 ==================== */
var CATS = [
  {k:"love",   n:"爱情", e:"他和这段关系", i:"♥"},
  {k:"career", n:"事业", e:"工作与去处",  i:"▲"},
  {k:"study",  n:"学业", e:"考试与方向",  i:"✎"},
  {k:"money",  n:"财运", e:"钱与机会",    i:"◆"}
];
var curCat = "";
function catName(k){
  for (var i = 0; i < CATS.length; i++){ if (CATS[i].k === k) return CATS[i].n; }
  return "综合";
}
function renderHomeCats(){
  var box = document.getElementById("homeCats");
  if (!box) return;
  var FLY = '<svg class="dtfy" viewBox="0 0 120 100" aria-hidden="true">'
    + '<g fill="none" stroke="#f0d79c" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<g class="wl"><path d="M60 50C52 25 21 15 15 34c-6 19 21 30 43 22"/>'
    + '<path d="M60 55C50 69 26 81 22 68c-4-13 18-18 36-12"/></g>'
    + '<g class="wr"><path d="M60 50c8-25 39-35 45-16 6 19-21 30-43 22"/>'
    + '<path d="M60 55c10 14 34 26 38 13 4-13-18-18-36-12"/></g>'
    + '<path d="M60 43v19"/>'
    + '<path d="M60 46C56 37 50 32 43 30"/><path d="M60 46c4-9 10-14 17-16"/>'
    + '</g></svg>';
  box.innerHTML = CATS.map(function(c){
    return '<div class="dtc" data-k="' + c.k + '">'
      + '<div class="dpp"><span class="d1"></span><i>' + c.i + '</i><span class="d2"></span></div>'
      + '<div class="dtxc"><b>' + c.n + '</b></div>'
      + FLY + '</div>';
  }).join("");
  Array.prototype.forEach.call(box.querySelectorAll(".dtc"), function(el){
    el.addEventListener("click", function(){ goDraw(el.getAttribute("data-k")); });
  });
}
/* 抽牌台顶部不再显示「现在问的是什么」一行（保留节点，避免脚本空引用） */
function renderDrawCats(){
  return;
}
function goDraw(cat){
  curCat = cat || "";
  renderDrawCats();
  showView("draw");
  if (onTable === 0 && hint) hint.style.display = "";
}
document.getElementById("btnBack").addEventListener("click", function(){ goBack(); });
/* 统一返回：先退当前视图内部子层，再按历史栈逐层回上一页，栈空则回首页 */
function goBack(){
  /* 今日运势：切换过档案后返回直接回首页；没切换则回运势正文 */
  if (curView === "fortune" && FT.pick){
    if (FT.switched){
      FT.switched = false;
      FT.pick = false;
      VSTACK.length = 0;
      showView("home");
      return;
    }
    ftPickBack(); return;
  }
  /* 星盘：表单 / 档案列表 / 星盘结果 逐层退 */
  if (curView === "astro"){
    if (AP_SUB.length){ apShowPane(AP_SUB.pop() || "list"); return; }
    if (ARCH_FROM_FT){ ARCH_FROM_FT = false; showView("fortune", true); ftPickBack(); return; }
  }
  /* 按历史栈逐层回上一页 */
  while (VSTACK.length){
    var prev = VSTACK.pop();
    if (!prev || !VIEWELS[prev] || prev === curView) continue;
    showView(prev, true);
    return;
  }
  showView("home");
}
document.getElementById("btnHomeFortune").addEventListener("click", function(){
  openFortune();
});
document.getElementById("btnHomeAstro").addEventListener("click", function(){
  smartAstro();
});
document.getElementById("btnHomeAnswer").addEventListener("click", function(){ openAnswer(); });
document.getElementById("btnHomeDice").addEventListener("click", function(){ openDice(); });
document.getElementById("btnDiceGo").addEventListener("click", function(){ diceGo(); });
(function(){
  var chips = document.querySelectorAll(".dcChip");
  for (var i = 0; i < chips.length; i++){
    chips[i].addEventListener("click", function(){
      var q = this.getAttribute("data-q") || this.textContent;
      document.getElementById("dcQInput").value = q;
    });
  }
  if (location.hash === "#dice") openDice();
  if (location.hash === "#dir") showView("dir");
  if (location.hash === "#draw") goDraw("");
})();
document.getElementById("btnAnsGo").addEventListener("click", function(){
  var rs = document.getElementById("ansResult");
  var st = document.getElementById("ansStage");
  if (rs.style.display === "flex"){
    rs.style.display = "none";
    st.style.display = "flex";
  }
  ansGo();
});
/* 首页点「塔罗牌」→ 进第二层方向选择页 */
document.getElementById("btnHomeDraw").addEventListener("click", function(){
  showView("dir");
});

/* ==================== 今日运势 ==================== */
/* ---- 省市区数据：省[短名, 全名, [lon,lat], 市[]]，市[短名, 全名, 区[], [lon,lat]]，区[名, lon, lat] ---- */
var PCD = [["北京","北京市",[116.405,39.905],[["北京","北京市",[["东城区",116.419,39.918],["西城区",116.367,39.915],["朝阳区",116.486,39.921],["丰台区",116.287,39.864],["石景山区",116.195,39.915],["海淀区",116.31,39.956],["门头沟区",116.105,39.937],["房山区",116.139,39.736],["通州区",116.659,39.902],["顺义区",116.654,40.129],["昌平区",116.236,40.218],["大兴区",116.338,39.729],["怀柔区",116.637,40.324],["平谷区",117.112,40.145],["密云区",116.843,40.377],["延庆区",115.985,40.465]],[116.405285,39.904989]]]],["天津","天津市",[117.19,39.126],[["天津","天津市",[["和平区",117.196,39.118],["河东区",117.227,39.122],["河西区",117.218,39.102],["南开区",117.164,39.12],["河北区",117.202,39.157],["红桥区",117.163,39.175],["东丽区",117.314,39.088],["西青区",117.012,39.139],["津南区",117.383,38.99],["北辰区",117.135,39.226],["武清区",117.058,39.377],["宝坻区",117.308,39.717],["滨海新区",117.654,39.033],["宁河区",117.828,39.329],["静海区",116.925,38.936],["蓟州区",117.407,40.045]],[117.190182,39.125596]]]],["河北","河北省",[114.502,38.045],[["石家庄","石家庄市",[["长安区",114.548,38.048],["桥西区",114.463,38.028],["新华区",114.466,38.067],["井陉矿区",114.058,38.07],["裕华区",114.533,38.028],["藁城区",114.85,38.034],["鹿泉区",114.321,38.094],["栾城区",114.654,37.887],["井陉县",114.144,38.034],["正定县",114.57,38.148],["行唐县",114.553,38.437],["灵寿县",114.379,38.307],["高邑县",114.611,37.606],["深泽县",115.2,38.185],["赞皇县",114.388,37.66],["无极县",114.978,38.176],["平山县",114.184,38.259],["元氏县",114.526,37.763],["赵县",114.775,37.754],["辛集市",115.217,37.929],["晋州市",115.045,38.027],["新乐市",114.686,38.345]],[114.502,38.045]],["唐山","唐山市",[["路南区",118.211,39.615],["路北区",118.175,39.629],["古冶区",118.454,39.716],["开平区",118.264,39.676],["丰南区",118.111,39.563],["丰润区",118.156,39.831],["曹妃甸区",118.447,39.278],["滦南县",118.682,39.506],["乐亭县",118.905,39.428],["迁西县",118.305,40.146],["玉田县",117.754,39.887],["遵化市",117.966,40.189],["迁安市",118.702,40.012],["滦州市",118.7,39.745]],[118.175,39.635]],["秦皇岛","秦皇岛市",[["海港区",119.596,39.943],["山海关区",119.754,39.998],["北戴河区",119.486,39.825],["抚宁区",119.241,39.887],["青龙满族自治县",118.955,40.406],["昌黎县",119.165,39.71],["卢龙县",118.882,39.892]],[119.587,39.943]],["邯郸","邯郸市",[["邯山区",114.485,36.603],["丛台区",114.495,36.611],["复兴区",114.458,36.615],["峰峰矿区",114.21,36.42],["肥乡区",114.805,36.556],["永年区",114.496,36.776],["临漳县",114.611,36.338],["成安县",114.68,36.444],["大名县",115.153,36.283],["涉县",113.673,36.563],["磁县",114.382,36.368],["邱县",115.169,36.813],["鸡泽县",114.879,36.915],["广平县",114.951,36.484],["馆陶县",115.289,36.539],["魏县",114.934,36.354],["曲周县",114.958,36.773],["武安市",114.195,36.696]],[114.491,36.612]],["邢台","邢台市",[["桥东区",114.507,37.064],["桥西区",114.474,37.068],["邢台县",114.561,37.051],["临城县",114.507,37.444],["内丘县",114.512,37.288],["柏乡县",114.693,37.484],["隆尧县",114.776,37.351],["任县",114.684,37.13],["南和县",114.691,37.004],["宁晋县",114.921,37.619],["巨鹿县",115.039,37.218],["新河县",115.248,37.526],["广宗县",115.143,37.076],["平乡县",115.029,37.069],["威县",115.273,36.983],["清河县",115.669,37.06],["临西县",115.499,36.864],["南宫市",115.398,37.36],["沙河市",114.505,36.862]],[114.509,37.068]],["保定","保定市",[["竞秀区",115.471,38.887],["莲池区",115.501,38.865],["满城区",115.324,38.951],["清苑区",115.492,38.771],["徐水区",115.649,39.02],["涞水县",115.712,39.393],["阜平县",114.199,38.847],["定兴县",115.797,39.266],["唐县",114.981,38.749],["高阳县",115.779,38.69],["容城县",115.866,39.053],["涞源县",114.693,39.358],["望都县",115.154,38.707],["安新县",115.932,38.93],["易县",115.501,39.353],["曲阳县",114.704,38.62],["蠡县",115.584,38.496],["顺平县",115.133,38.845],["博野县",115.462,38.458],["雄县",116.107,38.991],["涿州市",115.973,39.486],["定州市",114.991,38.518],["安国市",115.331,38.421],["高碑店市",115.883,39.328]],[115.482,38.868]],["张家口","张家口市",[["桥东区",114.886,40.814],["桥西区",114.882,40.824],["宣化区",115.063,40.609],["下花园区",115.281,40.489],["万全区",114.736,40.765],["崇礼区",115.282,40.971],["张北县",114.716,41.152],["康保县",114.616,41.85],["沽源县",115.685,41.667],["尚义县",113.978,41.08],["蔚县",114.583,39.837],["阳原县",114.167,40.113],["怀安县",114.422,40.671],["怀来县",115.521,40.405],["涿鹿县",115.219,40.379],["赤城县",115.833,40.912]],[114.884,40.812]],["承德","承德市",[["双桥区",117.939,40.976],["双滦区",117.797,40.96],["鹰手营子矿区",117.661,40.547],["承德县",118.172,40.769],["兴隆县",117.507,40.419],["滦平县",117.337,40.937],["隆化县",117.736,41.317],["丰宁满族自治县",116.651,41.21],["宽城满族自治县",118.489,40.608],["围场满族蒙古族自治县",117.764,41.949],["平泉市",118.69,41.006]],[117.939,40.976]],["沧州","沧州市",[["新华区",116.873,38.308],["运河区",116.84,38.307],["沧县",117.007,38.22],["青县",116.838,38.57],["东光县",116.542,37.887],["海兴县",117.497,38.142],["盐山县",117.23,38.056],["肃宁县",115.836,38.427],["南皮县",116.709,38.042],["吴桥县",116.392,37.628],["献县",116.124,38.19],["孟村回族自治县",117.105,38.058],["泊头市",116.57,38.073],["任丘市",116.107,38.707],["黄骅市",117.344,38.369],["河间市",116.089,38.441]],[116.857,38.311]],["廊坊","廊坊市",[["安次区",116.695,39.503],["广阳区",116.714,39.522],["固安县",116.3,39.436],["永清县",116.498,39.32],["香河县",117.007,39.757],["大城县",116.641,38.699],["文安县",116.46,38.867],["大厂回族自治县",116.987,39.889],["霸州市",116.392,39.117],["三河市",117.077,39.983]],[116.704,39.524]],["衡水","衡水市",[["桃城区",115.695,37.732],["冀州区",115.579,37.543],["枣强县",115.726,37.512],["武邑县",115.892,37.804],["武强县",115.97,38.037],["饶阳县",115.727,38.233],["安平县",115.52,38.234],["故城县",115.967,37.351],["景县",116.258,37.687],["阜城县",116.165,37.87],["深州市",115.555,38.003]],[115.666,37.735]]]],["山西","山西省",[112.549,37.857],[["太原","太原市",[["小店区",112.564,37.818],["迎泽区",112.559,37.856],["杏花岭区",112.561,37.879],["尖草坪区",112.487,37.94],["万柏林区",112.522,37.863],["晋源区",112.478,37.716],["清徐县",112.358,37.607],["阳曲县",112.674,38.059],["娄烦县",111.794,38.066],["古交市",112.174,37.909]],[112.549,37.857]],["大同","大同市",[["新荣区",113.141,40.258],["平城区",113.298,40.076],["云冈区",113.15,40.005],["云州区",113.612,40.04],["阳高县",113.75,40.365],["天镇县",114.091,40.421],["广灵县",114.279,39.763],["灵丘县",114.236,39.439],["浑源县",113.698,39.699],["左云县",112.706,40.013]],[113.295,40.09]],["阳泉","阳泉市",[["城区",113.587,37.861],["矿区",113.559,37.87],["郊区",113.587,37.941],["平定县",113.631,37.8],["盂县",113.412,38.086]],[113.583,37.861]],["长治","长治市",[["潞州区",113.114,36.188],["上党区",113.057,36.052],["屯留区",112.893,36.314],["潞城区",113.223,36.332],["襄垣县",113.05,36.533],["平顺县",113.439,36.2],["黎城县",113.387,36.503],["壶关县",113.206,36.111],["长子县",112.885,36.119],["武乡县",112.865,36.834],["沁县",112.701,36.757],["沁源县",112.341,36.501]],[113.114,36.191]],["晋城","晋城市",[["城区",112.853,35.497],["沁水县",112.187,35.689],["阳城县",112.422,35.482],["陵川县",113.279,35.776],["泽州县",112.899,35.617],["高平市",112.931,35.791]],[112.851,35.498]],["朔州","朔州市",[["朔城区",112.429,39.325],["平鲁区",112.295,39.516],["山阴县",112.816,39.527],["应县",113.188,39.559],["右玉县",112.466,39.989],["怀仁市",113.101,39.821]],[112.433,39.331]],["晋中","晋中市",[["榆次区",112.74,37.698],["榆社县",112.974,37.069],["左权县",113.378,37.08],["和顺县",113.573,37.327],["昔阳县",113.706,37.604],["寿阳县",113.178,37.891],["太谷县",112.554,37.425],["祁县",112.331,37.359],["平遥县",112.174,37.195],["灵石县",111.773,36.847],["介休市",111.914,37.028]],[112.736,37.696]],["运城","运城市",[["盐湖区",111.001,35.026],["临猗县",110.775,35.142],["万荣县",110.844,35.417],["闻喜县",111.22,35.354],["稷山县",110.979,35.6],["新绛县",111.225,35.614],["绛县",111.576,35.49],["垣曲县",111.671,35.298],["夏县",111.223,35.14],["平陆县",111.212,34.837],["芮城县",110.691,34.695],["永济市",110.448,34.865],["河津市",110.71,35.597]],[111.004,35.023]],["忻州","忻州市",[["忻府区",112.734,38.418],["定襄县",112.963,38.485],["五台县",113.259,38.726],["代县",112.963,39.065],["繁峙县",113.268,39.188],["宁武县",112.308,39.002],["静乐县",111.94,38.356],["神池县",112.2,39.088],["五寨县",111.841,38.913],["岢岚县",111.57,38.706],["河曲县",111.147,39.382],["保德县",111.086,39.023],["偏关县",111.5,39.442],["原平市",112.713,38.729]],[112.734,38.418]],["临汾","临汾市",[["尧都区",111.523,36.08],["曲沃县",111.476,35.641],["翼城县",111.714,35.739],["襄汾县",111.443,35.876],["洪洞县",111.674,36.256],["古县",111.92,36.269],["安泽县",112.251,36.146],["浮山县",111.85,35.971],["吉县",110.683,36.099],["乡宁县",110.857,35.975],["大宁县",110.751,36.464],["隰县",110.936,36.693],["永和县",110.631,36.761],["蒲县",111.097,36.412],["汾西县",111.563,36.653],["侯马市",111.371,35.62],["霍州市",111.723,36.572]],[111.518,36.084]],["吕梁","吕梁市",[["离石区",111.134,37.524],["文水县",112.033,37.436],["交城县",112.159,37.555],["兴县",111.125,38.464],["临县",110.996,37.961],["柳林县",110.896,37.432],["石楼县",110.837,36.999],["岚县",111.672,38.279],["方山县",111.239,37.893],["中阳县",111.193,37.342],["交口县",111.183,36.983],["孝义市",111.782,37.144],["汾阳市",111.785,37.268]],[111.134,37.524]]]],["内蒙古","内蒙古自治区",[111.671,40.818],[["呼和浩特","呼和浩特市",[["新城区",111.686,40.826],["回民区",111.662,40.815],["玉泉区",111.665,40.799],["赛罕区",111.698,40.808],["土默特左旗",111.134,40.72],["托克托县",111.197,40.277],["和林格尔县",111.824,40.38],["清水河县",111.672,39.912],["武川县",111.457,41.094]],[111.671,40.818]],["包头","包头市",[["东河区",110.027,40.587],["昆都仑区",109.823,40.661],["青山区",109.88,40.669],["石拐区",110.273,40.672],["白云鄂博矿区",109.97,41.769],["九原区",109.968,40.601],["土默特右旗",110.527,40.566],["固阳县",110.063,41.03],["达尔罕茂明安联合旗",110.438,41.703]],[109.84,40.658]],["乌海","乌海市",[["海勃湾区",106.818,39.674],["海南区",106.885,39.442],["乌达区",106.723,39.502]],[106.826,39.674]],["赤峰","赤峰市",[["红山区",118.961,42.27],["元宝山区",119.29,42.041],["松山区",118.939,42.281],["阿鲁科尔沁旗",120.095,43.879],["巴林左旗",119.392,43.981],["巴林右旗",118.678,43.529],["林西县",118.058,43.605],["克什克腾旗",117.542,43.256],["翁牛特旗",119.023,42.937],["喀喇沁旗",118.709,41.928],["宁城县",119.339,41.599],["敖汉旗",119.906,42.287]],[118.957,42.275]],["通辽","通辽市",[["科尔沁区",122.264,43.617],["科尔沁左翼中旗",123.314,44.127],["科尔沁左翼后旗",122.355,42.955],["开鲁县",121.309,43.602],["库伦旗",121.775,42.735],["奈曼旗",120.663,42.847],["扎鲁特旗",120.905,44.555],["霍林郭勒市",119.658,45.532]],[122.263,43.617]],["鄂尔多斯","鄂尔多斯市",[["东胜区",109.989,39.818],["康巴什区",109.79,39.607],["达拉特旗",110.04,40.404],["准格尔旗",111.238,39.865],["鄂托克前旗",107.482,38.183],["鄂托克旗",107.983,39.096],["杭锦旗",108.736,39.832],["乌审旗",108.842,38.597],["伊金霍洛旗",109.787,39.604]],[109.99,39.817]],["呼伦贝尔","呼伦贝尔市",[["海拉尔区",119.765,49.214],["扎赉诺尔区",117.716,49.457],["阿荣旗",123.465,48.131],["莫力达瓦达斡尔族自治旗",124.507,48.478],["鄂伦春自治旗",123.726,50.59],["鄂温克族自治旗",119.754,49.143],["陈巴尔虎旗",119.438,49.328],["新巴尔虎左旗",118.267,48.217],["新巴尔虎右旗",116.826,48.669],["满洲里市",117.456,49.591],["牙克石市",120.729,49.287],["扎兰屯市",122.744,48.007],["额尔古纳市",120.179,50.244],["根河市",121.533,50.78]],[119.758,49.215]],["巴彦淖尔","巴彦淖尔市",[["临河区",107.417,40.757],["五原县",108.271,41.098],["磴口县",107.006,40.33],["乌拉特前旗",108.657,40.725],["乌拉特中旗",108.515,41.573],["乌拉特后旗",107.075,41.084],["杭锦后旗",107.148,40.889]],[107.417,40.757]],["乌兰察布","乌兰察布市",[["集宁区",113.116,41.034],["卓资县",112.578,40.896],["化德县",114.01,41.899],["商都县",113.561,41.56],["兴和县",113.834,40.872],["凉城县",112.501,40.532],["察哈尔右翼前旗",113.212,40.787],["察哈尔右翼中旗",112.634,41.274],["察哈尔右翼后旗",113.191,41.447],["四子王旗",111.701,41.528],["丰镇市",113.163,40.438]],[113.115,41.034]],["兴安盟","兴安盟",[["乌兰浩特市",122.069,46.077],["阿尔山市",119.944,47.177],["科尔沁右翼前旗",121.958,46.076],["科尔沁右翼中旗",121.473,45.06],["扎赉特旗",122.909,46.725],["突泉县",121.565,45.381]],[122.07,46.076]],["锡林郭勒盟","锡林郭勒盟",[["二连浩特市",111.98,43.653],["锡林浩特市",116.092,43.944],["阿巴嘎旗",114.971,44.023],["苏尼特左旗",113.653,43.854],["苏尼特右旗",112.655,42.747],["东乌珠穆沁旗",116.98,45.51],["西乌珠穆沁旗",117.615,44.586],["太仆寺旗",115.287,41.895],["镶黄旗",113.844,42.239],["正镶白旗",115.031,42.287],["正蓝旗",116.003,42.246],["多伦县",116.477,42.198]],[116.091,43.944]],["阿拉善盟","阿拉善盟",[["阿拉善左旗",105.702,38.847],["阿拉善右旗",101.672,39.212],["额济纳旗",101.069,41.959]],[105.706,38.845]]]],["辽宁","辽宁省",[123.429,41.797],[["沈阳","沈阳市",[["和平区",123.407,41.788],["沈河区",123.446,41.796],["大东区",123.47,41.809],["皇姑区",123.406,41.822],["铁西区",123.351,41.788],["苏家屯区",123.342,41.666],["浑南区",123.459,41.742],["沈北新区",123.521,42.052],["于洪区",123.311,41.796],["辽中区",122.731,41.513],["康平县",123.353,42.742],["法库县",123.417,42.507],["新民市",122.829,41.997]],[123.429,41.797]],["大连","大连市",[["中山区",121.644,38.922],["西岗区",121.616,38.914],["沙河口区",121.594,38.913],["甘井子区",121.583,38.975],["旅顺口区",121.267,38.812],["金州区",121.789,39.053],["普兰店区",121.971,39.402],["长海县",122.588,39.272],["瓦房店市",122.003,39.631],["庄河市",122.971,39.698]],[121.619,38.915]],["鞍山","鞍山市",[["铁东区",122.994,41.11],["铁西区",122.972,41.111],["立山区",123.025,41.151],["千山区",122.949,41.069],["台安县",122.43,41.387],["岫岩满族自治县",123.288,40.282],["海城市",122.752,40.853]],[122.996,41.111]],["抚顺","抚顺市",[["新抚区",123.903,41.861],["东洲区",124.047,41.867],["望花区",123.802,41.852],["顺城区",123.917,41.881],["抚顺县",124.098,41.923],["新宾满族自治县",125.038,41.732],["清原满族自治县",124.927,42.101]],[123.921,41.876]],["本溪","本溪市",[["平山区",123.761,41.292],["溪湖区",123.765,41.33],["明山区",123.763,41.302],["南芬区",123.748,41.104],["本溪满族自治县",124.126,41.3],["桓仁满族自治县",125.359,41.269]],[123.771,41.298]],["丹东","丹东市",[["元宝区",124.398,40.136],["振兴区",124.361,40.103],["振安区",124.428,40.159],["宽甸满族自治县",124.785,40.73],["东港市",124.149,39.883],["凤城市",124.071,40.458]],[124.383,40.124]],["锦州","锦州市",[["古塔区",121.13,41.116],["凌河区",121.151,41.115],["太和区",121.107,41.105],["黑山县",122.118,41.692],["义县",121.243,41.537],["凌海市",121.364,41.172],["北镇市",121.796,41.599]],[121.136,41.119]],["营口","营口市",[["站前区",122.253,40.67],["西市区",122.21,40.663],["鲅鱼圈区",122.127,40.264],["老边区",122.383,40.683],["盖州市",122.356,40.405],["大石桥市",122.506,40.634]],[122.235,40.667]],["阜新","阜新市",[["海州区",121.658,42.011],["新邱区",121.791,42.087],["太平区",121.678,42.011],["清河门区",121.42,41.78],["细河区",121.655,42.019],["阜新蒙古族自治县",121.743,42.059],["彰武县",122.537,42.385]],[121.649,42.012]],["辽阳","辽阳市",[["白塔区",123.173,41.267],["文圣区",123.188,41.267],["宏伟区",123.2,41.206],["弓长岭区",123.432,41.158],["太子河区",123.185,41.252],["辽阳县",123.08,41.216],["灯塔市",123.326,41.428]],[123.182,41.269]],["盘锦","盘锦市",[["双台子区",122.056,41.19],["兴隆台区",122.072,41.122],["大洼区",122.072,40.994],["盘山县",121.985,41.241]],[122.07,41.124]],["铁岭","铁岭市",[["银州区",123.845,42.292],["清河区",124.149,42.543],["铁岭县",123.726,42.223],["西丰县",124.723,42.738],["昌图县",124.11,42.784],["调兵山市",123.545,42.451],["开原市",124.046,42.542]],[123.844,42.291]],["朝阳","朝阳市",[["双塔区",120.449,41.579],["龙城区",120.413,41.577],["朝阳县",120.404,41.526],["建平县",119.642,41.403],["喀喇沁左翼蒙古族自治县",119.745,41.125],["北票市",120.767,41.803],["凌源市",119.405,41.243]],[120.451,41.577]],["葫芦岛","葫芦岛市",[["连山区",120.859,40.755],["龙港区",120.839,40.71],["南票区",120.752,41.099],["绥中县",120.342,40.328],["建昌县",119.808,40.813],["兴城市",120.729,40.619]],[120.856,40.756]]]],["吉林","吉林省",[125.325,43.887],[["长春","长春市",[["南关区",125.337,43.89],["宽城区",125.343,43.904],["朝阳区",125.318,43.865],["二道区",125.385,43.871],["绿园区",125.272,43.892],["双阳区",125.659,43.525],["九台区",125.845,44.157],["农安县",125.175,44.431],["榆树市",126.55,44.828],["德惠市",125.703,44.534]],[125.325,43.887]],["吉林","吉林市",[["昌邑区",126.571,43.851],["龙潭区",126.561,43.91],["船营区",126.552,43.844],["丰满区",126.561,43.817],["永吉县",126.502,43.667],["蛟河市",127.343,43.721],["桦甸市",126.745,42.972],["舒兰市",126.948,44.411],["磐石市",126.06,42.942]],[126.553,43.844]],["四平","四平市",[["铁西区",124.361,43.176],["铁东区",124.388,43.167],["梨树县",124.336,43.308],["伊通满族自治县",125.303,43.345],["公主岭市",124.818,43.509],["双辽市",123.505,43.518]],[124.371,43.17]],["辽源","辽源市",[["龙山区",125.145,42.903],["西安区",125.151,42.92],["东丰县",125.53,42.675],["东辽县",124.992,42.928]],[125.145,42.903]],["通化","通化市",[["东昌区",125.937,41.721],["二道江区",126.046,41.778],["通化县",125.753,41.678],["辉南县",126.043,42.683],["柳河县",125.741,42.281],["梅河口市",125.687,42.53],["集安市",126.186,41.126]],[125.937,41.721]],["白山","白山市",[["浑江区",126.428,41.943],["江源区",126.584,42.048],["抚松县",127.274,42.333],["靖宇县",126.808,42.39],["长白朝鲜族自治县",128.203,41.419],["临江市",126.919,41.811]],[126.428,41.943]],["松原","松原市",[["宁江区",124.828,45.176],["前郭尔罗斯蒙古族自治县",124.827,45.116],["长岭县",123.985,44.277],["乾安县",124.024,45.007],["扶余市",126.043,44.986]],[124.824,45.118]],["白城","白城市",[["洮北区",122.842,45.619],["镇赉县",123.202,45.846],["通榆县",123.089,44.809],["洮南市",122.784,45.339],["大安市",124.292,45.508]],[122.841,45.619]],["延边朝鲜族自治州","延边朝鲜族自治州",[["延吉市",129.516,42.907],["图们市",129.847,42.967],["敦化市",128.23,43.367],["珲春市",130.366,42.871],["龙井市",129.426,42.771],["和龙市",129.009,42.547],["汪清县",129.766,43.315],["安图县",128.902,43.111]],[129.513,42.905]]]],["黑龙江","黑龙江省",[126.642,45.757],[["哈尔滨","哈尔滨市",[["道里区",126.613,45.762],["南岗区",126.652,45.756],["道外区",126.649,45.785],["平房区",126.629,45.606],["松北区",126.563,45.815],["香坊区",126.667,45.713],["呼兰区",126.603,45.984],["阿城区",126.973,45.538],["双城区",126.309,45.378],["依兰县",129.566,46.315],["方正县",128.836,45.84],["宾县",127.486,45.759],["巴彦县",127.404,46.082],["木兰县",128.043,45.95],["通河县",128.748,45.978],["延寿县",128.332,45.456],["尚志市",127.969,45.215],["五常市",127.158,44.919]],[126.642,45.757]],["齐齐哈尔","齐齐哈尔市",[["龙沙区",123.957,47.342],["建华区",123.956,47.354],["铁锋区",123.974,47.339],["昂昂溪区",123.813,47.157],["富拉尔基区",123.639,47.207],["碾子山区",122.888,47.514],["梅里斯达斡尔族区",123.755,47.311],["龙江县",123.187,47.336],["依安县",125.308,47.89],["泰来县",123.42,46.392],["甘南县",123.506,47.918],["富裕县",124.469,47.797],["克山县",125.874,48.034],["克东县",126.249,48.037],["拜泉县",126.092,47.607],["讷河市",124.882,48.481]],[123.958,47.342]],["鸡西","鸡西市",[["鸡冠区",130.974,45.3],["恒山区",130.911,45.213],["滴道区",130.847,45.349],["梨树区",130.698,45.092],["城子河区",131.011,45.338],["麻山区",130.481,45.21],["鸡东县",131.149,45.251],["虎林市",132.974,45.768],["密山市",131.874,45.547]],[130.976,45.3]],["鹤岗","鹤岗市",[["向阳区",130.292,47.345],["工农区",130.277,47.332],["南山区",130.276,47.313],["兴安区",130.236,47.253],["东山区",130.317,47.337],["兴山区",130.305,47.36],["萝北县",130.829,47.578],["绥滨县",131.861,47.29]],[130.277,47.332]],["双鸭山","双鸭山市",[["尖山区",131.159,46.643],["岭东区",131.164,46.591],["四方台区",131.333,46.594],["宝山区",131.404,46.573],["集贤县",131.139,46.729],["友谊县",131.811,46.775],["宝清县",132.206,46.329],["饶河县",134.021,46.801]],[131.157,46.643]],["大庆","大庆市",[["萨尔图区",125.115,46.596],["龙凤区",125.146,46.574],["让胡路区",124.868,46.653],["红岗区",124.89,46.403],["大同区",124.819,46.034],["肇州县",125.273,45.709],["肇源县",125.082,45.519],["林甸县",124.878,47.186],["杜尔伯特蒙古族自治县",124.446,46.866]],[125.113,46.591]],["伊春","伊春市",[["伊春区",128.899,47.727],["南岔区",129.282,47.137],["友好区",128.839,47.854],["西林区",129.311,47.479],["翠峦区",128.672,47.726],["新青区",129.53,48.288],["美溪区",129.133,47.636],["金山屯区",129.436,47.413],["五营区",129.245,48.108],["乌马河区",128.803,47.727],["汤旺河区",129.572,48.454],["带岭区",129.021,47.028],["乌伊岭区",129.438,48.591],["红星区",129.389,48.238],["上甘岭区",129.025,47.975],["嘉荫县",130.398,48.891],["铁力市",128.031,46.986]],[128.899,47.725]],["佳木斯","佳木斯市",[["向阳区",130.362,46.81],["前进区",130.378,46.812],["东风区",130.403,46.822],["郊区",130.352,46.807],["桦南县",130.57,46.24],["桦川县",130.724,47.023],["汤原县",129.904,46.73],["同江市",132.51,47.651],["富锦市",132.038,47.251],["抚远市",134.295,48.365]],[130.362,46.81]],["七台河","七台河市",[["新兴区",130.889,45.794],["桃山区",131.016,45.771],["茄子河区",131.072,45.777],["勃利县",130.575,45.752]],[131.016,45.771]],["牡丹江","牡丹江市",[["东安区",129.623,44.582],["阳明区",129.635,44.596],["爱民区",129.601,44.595],["西安区",129.613,44.581],["林口县",130.268,45.287],["绥芬河市",131.165,44.397],["海林市",129.388,44.574],["宁安市",129.47,44.347],["穆棱市",130.527,44.92],["东宁市",131.125,44.064]],[129.619,44.583]],["黑河","黑河市",[["爱辉区",127.498,50.249],["嫩江市",125.23,49.177],["逊克县",128.476,49.583],["孙吴县",127.327,49.424],["北安市",126.509,48.245],["五大连池市",126.198,48.513]],[127.499,50.25]],["绥化","绥化市",[["北林区",126.991,46.635],["望奎县",126.484,46.834],["兰西县",126.289,46.259],["青冈县",126.112,46.687],["庆安县",127.51,46.879],["明水县",125.908,47.184],["绥棱县",127.111,47.247],["安达市",125.33,46.411],["肇东市",125.991,46.069],["海伦市",126.969,47.46]],[126.993,46.637]],["大兴安岭地区","大兴安岭地区",[["漠河市",122.536,52.972],["加格达奇区",124.127,50.425],["呼玛县",126.662,51.727],["塔河县",124.711,52.335]],[124.712,52.335]]]],["上海","上海市",[121.473,31.232],[["上海","上海市",[["黄浦区",121.49,31.223],["徐汇区",121.438,31.18],["长宁区",121.422,31.218],["静安区",121.448,31.229],["普陀区",121.392,31.242],["虹口区",121.492,31.261],["杨浦区",121.523,31.271],["闵行区",121.376,31.112],["宝山区",121.49,31.399],["嘉定区",121.25,31.384],["浦东新区",121.568,31.246],["金山区",121.331,30.725],["松江区",121.224,31.03],["青浦区",121.113,31.151],["奉贤区",121.458,30.912],["崇明区",121.398,31.627]],[121.472644,31.231706]]]],["江苏","江苏省",[118.767,32.042],[["南京","南京市",[["玄武区",118.792,32.051],["秦淮区",118.786,32.034],["建邺区",118.733,32.005],["鼓楼区",118.77,32.067],["浦口区",118.625,32.058],["栖霞区",118.809,32.102],["雨花台区",118.772,31.996],["江宁区",118.851,31.953],["六合区",118.851,32.341],["溧水区",119.029,31.653],["高淳区",118.876,31.327]],[118.767,32.042]],["无锡","无锡市",[["锡山区",120.357,31.586],["惠山区",120.304,31.681],["滨湖区",120.266,31.55],["梁溪区",120.297,31.576],["新吴区",120.353,31.551],["江阴市",120.276,31.911],["宜兴市",119.821,31.364]],[120.302,31.575]],["徐州","徐州市",[["鼓楼区",117.193,34.269],["云龙区",117.195,34.255],["贾汪区",117.45,34.442],["泉山区",117.182,34.262],["铜山区",117.184,34.193],["丰县",116.593,34.697],["沛县",116.937,34.729],["睢宁县",117.951,33.899],["新沂市",118.346,34.369],["邳州市",117.964,34.315]],[117.185,34.262]],["常州","常州市",[["天宁区",119.964,31.78],["钟楼区",119.948,31.781],["新北区",119.975,31.825],["武进区",119.959,31.719],["金坛区",119.573,31.744],["溧阳市",119.488,31.427]],[119.947,31.773]],["苏州","苏州市",[["虎丘区",120.567,31.295],["吴中区",120.625,31.271],["相城区",120.619,31.397],["姑苏区",120.622,31.311],["吴江区",120.642,31.16],["苏州工业园区",120.723,31.324],["常熟市",120.749,31.658],["张家港市",120.543,31.866],["昆山市",120.958,31.382],["太仓市",121.112,31.453]],[120.62,31.299]],["南通","南通市",[["崇川区",120.866,32.015],["港闸区",120.834,32.04],["通州区",121.073,32.084],["如东县",121.186,32.312],["启东市",121.66,31.81],["如皋市",120.566,32.392],["海门市",121.177,31.894],["海安市",120.466,32.54]],[120.865,32.016]],["连云港","连云港市",[["连云区",119.366,34.74],["海州区",119.18,34.602],["赣榆区",119.129,34.839],["东海县",118.766,34.523],["灌云县",119.256,34.298],["灌南县",119.352,34.093]],[119.179,34.6]],["淮安","淮安市",[["淮安区",119.146,33.507],["淮阴区",119.021,33.622],["清江浦区",119.019,33.603],["洪泽区",118.868,33.295],["涟水县",119.266,33.771],["盱眙县",118.494,33.004],["金湖县",119.017,33.018]],[119.021,33.598]],["盐城","盐城市",[["亭湖区",120.136,33.384],["盐都区",120.14,33.341],["大丰区",120.47,33.2],["响水县",119.58,34.2],["滨海县",119.828,33.99],["阜宁县",119.805,33.786],["射阳县",120.257,33.774],["建湖县",119.793,33.473],["东台市",120.314,32.853]],[120.14,33.378]],["扬州","扬州市",[["广陵区",119.442,32.392],["邗江区",119.398,32.378],["江都区",119.567,32.427],["宝应县",119.321,33.237],["仪征市",119.182,32.272],["高邮市",119.444,32.785]],[119.421,32.393]],["镇江","镇江市",[["京口区",119.455,32.206],["润州区",119.415,32.214],["丹徒区",119.434,32.129],["丹阳市",119.582,31.991],["扬中市",119.828,32.237],["句容市",119.167,31.947]],[119.453,32.204]],["泰州","泰州市",[["海陵区",119.92,32.488],["高港区",119.882,32.316],["姜堰区",120.148,32.508],["兴化市",119.84,32.938],["靖江市",120.268,32.018],["泰兴市",120.02,32.169]],[119.915,32.485]],["宿迁","宿迁市",[["宿城区",118.279,33.938],["宿豫区",118.33,33.941],["沭阳县",118.776,34.129],["泗阳县",118.681,33.711],["泗洪县",118.212,33.457]],[118.275,33.963]]]],["浙江","浙江省",[120.154,30.287],[["杭州","杭州市",[["上城区",120.171,30.25],["下城区",120.173,30.276],["江干区",120.203,30.267],["拱墅区",120.15,30.315],["西湖区",120.147,30.273],["滨江区",120.211,30.207],["萧山区",120.271,30.163],["余杭区",120.302,30.421],["富阳区",119.95,30.05],["临安区",119.715,30.231],["桐庐县",119.685,29.797],["淳安县",119.044,29.604],["建德市",119.279,29.472]],[120.154,30.287]],["宁波","宁波市",[["海曙区",121.54,29.874],["江北区",121.559,29.888],["北仑区",121.831,29.909],["镇海区",121.713,29.952],["鄞州区",121.558,29.832],["奉化区",121.411,29.662],["象山县",121.877,29.47],["宁海县",121.433,29.3],["余姚市",121.156,30.045],["慈溪市",121.248,30.177]],[121.55,29.868]],["温州","温州市",[["鹿城区",120.674,28.003],["龙湾区",120.763,27.97],["瓯海区",120.637,28.006],["洞头区",121.156,27.836],["永嘉县",120.691,28.154],["平阳县",120.564,27.669],["苍南县",120.406,27.508],["文成县",120.092,27.789],["泰顺县",119.716,27.557],["瑞安市",120.646,27.779],["乐清市",120.967,28.116],["龙港市",120.553,27.578]],[120.672,28.001]],["嘉兴","嘉兴市",[["南湖区",120.75,30.765],["秀洲区",120.72,30.763],["嘉善县",120.922,30.841],["海盐县",120.942,30.522],["海宁市",120.689,30.526],["平湖市",121.015,30.699],["桐乡市",120.551,30.629]],[120.751,30.763]],["湖州","湖州市",[["吴兴区",120.101,30.867],["南浔区",120.417,30.873],["德清县",119.968,30.535],["长兴县",119.91,31.005],["安吉县",119.688,30.632]],[120.102,30.867]],["绍兴","绍兴市",[["越城区",120.585,29.997],["柯桥区",120.476,30.078],["上虞区",120.874,30.017],["新昌县",120.906,29.501],["诸暨市",120.244,29.714],["嵊州市",120.829,29.587]],[120.582,29.997]],["金华","金华市",[["婺城区",119.653,29.083],["金东区",119.681,29.096],["武义县",119.819,28.897],["浦江县",119.893,29.451],["磐安县",120.445,29.053],["兰溪市",119.461,29.21],["义乌市",120.075,29.307],["东阳市",120.233,29.263],["永康市",120.036,28.895]],[119.65,29.09]],["衢州","衢州市",[["柯城区",118.873,28.945],["衢江区",118.958,28.973],["常山县",118.522,28.9],["开化县",118.414,29.137],["龙游县",119.173,29.031],["江山市",118.628,28.735]],[118.873,28.942]],["舟山","舟山市",[["定海区",122.108,30.016],["普陀区",122.302,29.946],["岱山县",122.201,30.243],["嵊泗县",122.458,30.727]],[122.107,30.016]],["台州","台州市",[["椒江区",121.431,28.676],["黄岩区",121.262,28.645],["路桥区",121.373,28.582],["三门县",121.376,29.119],["天台县",121.031,29.141],["仙居县",120.735,28.849],["温岭市",121.374,28.369],["临海市",121.131,28.845],["玉环市",121.232,28.128]],[121.429,28.661]],["丽水","丽水市",[["莲都区",119.922,28.451],["青田县",120.292,28.135],["缙云县",120.079,28.654],["遂昌县",119.276,28.592],["松阳县",119.485,28.45],["云和县",119.569,28.111],["庆元县",119.067,27.618],["景宁畲族自治县",119.635,27.977],["龙泉市",119.132,28.069]],[119.922,28.452]]]],["安徽","安徽省",[117.283,31.861],[["合肥","合肥市",[["瑶海区",117.315,31.87],["庐阳区",117.284,31.869],["蜀山区",117.262,31.856],["包河区",117.286,31.83],["长丰县",117.165,32.479],["肥东县",117.463,31.884],["肥西县",117.166,31.72],["庐江县",117.29,31.251],["巢湖市",117.874,31.601]],[117.283,31.861]],["芜湖","芜湖市",[["镜湖区",118.376,31.326],["弋江区",118.377,31.313],["鸠江区",118.4,31.363],["三山区",118.234,31.225],["芜湖县",118.572,31.145],["繁昌县",118.201,31.081],["南陵县",118.337,30.92],["无为县",117.911,31.303]],[118.376,31.326]],["蚌埠","蚌埠市",[["龙子湖区",117.382,32.95],["蚌山区",117.356,32.938],["禹会区",117.353,32.932],["淮上区",117.347,32.963],["怀远县",117.2,32.957],["五河县",117.889,33.146],["固镇县",117.316,33.319]],[117.363,32.94]],["淮南","淮南市",[["大通区",117.053,32.632],["田家庵区",117.018,32.644],["谢家集区",116.865,32.598],["八公山区",116.841,32.628],["潘集区",116.817,32.782],["凤台县",116.723,32.705],["寿县",116.785,32.577]],[117.018,32.648]],["马鞍山","马鞍山市",[["花山区",118.511,31.699],["雨山区",118.493,31.686],["博望区",118.844,31.562],["当涂县",118.49,31.556],["含山县",118.106,31.728],["和县",118.363,31.717]],[118.508,31.689]],["淮北","淮北市",[["杜集区",116.834,33.991],["相山区",116.791,33.971],["烈山区",116.809,33.89],["濉溪县",116.767,33.916]],[116.795,33.972]],["铜陵","铜陵市",[["铜官区",117.818,30.932],["义安区",117.792,30.952],["郊区",117.807,30.909],["枞阳县",117.222,30.701]],[117.817,30.93]],["安庆","安庆市",[["迎江区",117.045,30.506],["大观区",117.035,30.506],["宜秀区",117.07,30.541],["怀宁县",116.829,30.735],["太湖县",116.305,30.452],["宿松县",116.12,30.158],["望江县",116.691,30.125],["岳西县",116.36,30.849],["桐城市",116.96,31.051],["潜山市",116.574,30.638]],[117.044,30.509]],["黄山","黄山市",[["屯溪区",118.317,29.709],["黄山区",118.137,30.295],["徽州区",118.34,29.825],["歙县",118.428,29.868],["休宁县",118.189,29.789],["黟县",117.943,29.924],["祁门县",117.717,29.853]],[118.317,29.709]],["滁州","滁州市",[["琅琊区",118.316,32.304],["南谯区",118.297,32.33],["来安县",118.433,32.45],["全椒县",118.269,32.094],["定远县",117.684,32.527],["凤阳县",117.562,32.867],["天长市",119.011,32.681],["明光市",117.998,32.781]],[118.316,32.304]],["阜阳","阜阳市",[["颍州区",115.814,32.891],["颍东区",115.859,32.909],["颍泉区",115.805,32.925],["临泉县",115.262,33.063],["太和县",115.627,33.162],["阜南县",115.591,32.638],["颍上县",116.259,32.637],["界首市",115.362,33.262]],[115.82,32.897]],["宿州","宿州市",[["埇桥区",116.983,33.634],["砀山县",116.351,34.426],["萧县",116.945,34.183],["灵璧县",117.551,33.541],["泗县",117.885,33.478]],[116.984,33.634]],["六安","六安市",[["金安区",116.503,31.754],["裕安区",116.495,31.751],["叶集区",115.914,31.848],["霍邱县",116.279,32.341],["舒城县",116.944,31.463],["金寨县",115.879,31.682],["霍山县",116.333,31.402]],[116.508,31.753]],["亳州","亳州市",[["谯城区",115.781,33.869],["涡阳县",116.212,33.503],["蒙城县",116.56,33.261],["利辛县",116.208,33.144]],[115.783,33.869]],["池州","池州市",[["贵池区",117.488,30.657],["东至县",117.021,30.097],["石台县",117.483,30.21],["青阳县",117.857,30.638]],[117.489,30.656]],["宣城","宣城市",[["宣州区",118.758,30.946],["郎溪县",119.185,31.128],["广德市",119.418,30.893],["泾县",118.412,30.686],["绩溪县",118.595,30.065],["旌德县",118.543,30.288],["宁国市",118.983,30.627]],[118.758,30.946]]]],["福建","福建省",[119.306,26.075],[["福州","福州市",[["鼓楼区",119.299,26.082],["台江区",119.31,26.059],["仓山区",119.321,26.039],["马尾区",119.459,25.992],["晋安区",119.329,26.079],["长乐区",119.511,25.961],["闽侯县",119.145,26.149],["连江县",119.538,26.202],["罗源县",119.553,26.487],["闽清县",118.868,26.224],["永泰县",118.939,25.865],["平潭县",119.791,25.504],["福清市",119.377,25.72]],[119.306,26.075]],["厦门","厦门市",[["思明区",118.088,24.462],["海沧区",118.036,24.493],["湖里区",118.109,24.513],["集美区",118.101,24.573],["同安区",118.15,24.729],["翔安区",118.243,24.637]],[118.11,24.49]],["莆田","莆田市",[["城厢区",119.001,25.434],["涵江区",119.119,25.459],["荔城区",119.02,25.43],["秀屿区",119.093,25.316],["仙游县",118.694,25.357]],[119.008,25.431]],["三明","三明市",[["梅列区",117.637,26.269],["三元区",117.607,26.234],["明溪县",117.202,26.357],["清流县",116.816,26.178],["宁化县",116.66,26.26],["大田县",117.849,25.691],["尤溪县",118.189,26.169],["沙县",117.789,26.397],["将乐县",117.474,26.729],["泰宁县",117.178,26.898],["建宁县",116.846,26.831],["永安市",117.364,25.974]],[117.635,26.265]],["泉州","泉州市",[["鲤城区",118.589,24.908],["丰泽区",118.605,24.896],["洛江区",118.67,24.941],["泉港区",118.912,25.127],["惠安县",118.799,25.029],["安溪县",118.186,25.057],["永春县",118.295,25.321],["德化县",118.243,25.489],["金门县",118.323,24.436],["石狮市",118.628,24.732],["晋江市",118.577,24.807],["南安市",118.387,24.959]],[118.589,24.909]],["漳州","漳州市",[["芗城区",117.656,24.51],["龙文区",117.671,24.516],["云霄县",117.341,23.95],["漳浦县",117.614,24.118],["诏安县",117.176,23.711],["长泰县",117.756,24.621],["东山县",117.428,23.703],["南靖县",117.365,24.516],["平和县",117.314,24.366],["华安县",117.536,25.001],["龙海市",117.817,24.445]],[117.662,24.511]],["南平","南平市",[["延平区",118.179,26.636],["建阳区",118.123,27.332],["顺昌县",117.808,26.793],["浦城县",118.537,27.92],["光泽县",117.338,27.543],["松溪县",118.783,27.526],["政和县",118.859,27.365],["邵武市",117.492,27.338],["武夷山市",118.033,27.752],["建瓯市",118.322,27.035]],[118.178,26.636]],["龙岩","龙岩市",[["新罗区",117.031,25.092],["永定区",116.733,24.72],["长汀县",116.361,25.842],["上杭县",116.425,25.05],["武平县",116.101,25.089],["连城县",116.757,25.709],["漳平市",117.421,25.292]],[117.03,25.092]],["宁德","宁德市",[["蕉城区",119.527,26.659],["霞浦县",120.005,26.882],["古田县",118.743,26.577],["屏南县",118.988,26.911],["寿宁县",119.507,27.458],["周宁县",119.338,27.103],["柘荣县",119.898,27.236],["福安市",119.651,27.084],["福鼎市",120.22,27.319]],[119.527,26.659]]]],["江西","江西省",[115.892,28.676],[["南昌","南昌市",[["东湖区",115.89,28.683],["西湖区",115.911,28.663],["青云谱区",115.907,28.636],["湾里区",115.731,28.715],["青山湖区",115.949,28.689],["新建区",115.821,28.691],["南昌县",115.942,28.544],["安义县",115.553,28.841],["进贤县",116.268,28.366]],[115.892,28.676]],["景德镇","景德镇市",[["昌江区",117.195,29.288],["珠山区",117.215,29.293],["浮梁县",117.218,29.352],["乐平市",117.129,28.967]],[117.215,29.293]],["萍乡","萍乡市",[["安源区",113.855,27.626],["湘东区",113.746,27.639],["莲花县",113.956,27.128],["上栗县",113.801,27.877],["芦溪县",114.041,27.634]],[113.852,27.623]],["九江","九江市",[["濂溪区",115.99,29.676],["浔阳区",115.996,29.725],["柴桑区",115.893,29.61],["武宁县",115.106,29.26],["修水县",114.573,29.033],["永修县",115.809,29.018],["德安县",115.763,29.327],["都昌县",116.205,29.275],["湖口县",116.244,29.726],["彭泽县",116.556,29.899],["瑞昌市",115.669,29.677],["共青城市",115.806,29.248],["庐山市",116.044,29.456]],[115.993,29.712]],["新余","新余市",[["渝水区",114.924,27.819],["分宜县",114.675,27.811]],[114.931,27.811]],["鹰潭","鹰潭市",[["月湖区",117.034,28.239],["余江区",116.823,28.206],["贵溪市",117.212,28.284]],[117.034,28.239]],["赣州","赣州市",[["章贡区",114.939,25.851],["南康区",114.757,25.662],["赣县区",115.018,25.865],["信丰县",114.931,25.38],["大余县",114.362,25.396],["上犹县",114.541,25.794],["崇义县",114.307,25.688],["安远县",115.392,25.135],["龙南县",114.793,24.905],["定南县",115.033,24.774],["全南县",114.532,24.743],["宁都县",116.019,26.472],["于都县",115.411,25.955],["兴国县",115.352,26.33],["会昌县",115.791,25.599],["寻乌县",115.651,24.954],["石城县",116.342,26.327],["瑞金市",116.035,25.875]],[114.94,25.851]],["吉安","吉安市",[["吉州区",114.987,27.112],["青原区",115.016,27.106],["吉安县",114.905,27.04],["吉水县",115.135,27.213],["峡江县",115.319,27.581],["新干县",115.399,27.756],["永丰县",115.436,27.321],["泰和县",114.901,26.79],["遂川县",114.517,26.324],["万安县",114.785,26.462],["安福县",114.614,27.383],["永新县",114.243,26.945],["井冈山市",114.284,26.746]],[114.986,27.112]],["宜春","宜春市",[["袁州区",114.387,27.8],["奉新县",115.39,28.701],["万载县",114.449,28.105],["上高县",114.933,28.235],["宜丰县",114.787,28.388],["靖安县",115.362,28.861],["铜鼓县",114.37,28.521],["丰城市",115.786,28.192],["樟树市",115.543,28.056],["高安市",115.382,28.421]],[114.391,27.804]],["抚州","抚州市",[["临川区",116.361,27.982],["东乡区",116.605,28.233],["南城县",116.639,27.555],["黎川县",116.915,27.293],["南丰县",116.533,27.21],["崇仁县",116.059,27.761],["乐安县",115.838,27.42],["宜黄县",116.223,27.547],["金溪县",116.779,27.907],["资溪县",117.066,27.707],["广昌县",116.327,26.838]],[116.358,27.984]],["上饶","上饶市",[["信州区",117.971,28.445],["广丰区",118.19,28.44],["广信区",117.906,28.454],["玉山县",118.244,28.673],["铅山县",117.712,28.311],["横峰县",117.608,28.415],["弋阳县",117.435,28.402],["余干县",116.691,28.692],["鄱阳县",116.674,28.993],["万年县",117.07,28.693],["婺源县",117.862,29.254],["德兴市",117.579,28.945]],[117.971,28.444]]]],["山东","山东省",[117.001,36.676],[["济南","济南市",[["历下区",117.039,36.664],["市中区",116.999,36.657],["槐荫区",116.948,36.668],["天桥区",116.996,36.693],["历城区",117.064,36.682],["长清区",116.746,36.561],["章丘区",117.541,36.712],["济阳区",117.176,36.977],["莱芜区",117.678,36.214],["钢城区",117.82,36.058],["平阴县",116.455,36.287],["商河县",117.156,37.311]],[117.001,36.676]],["青岛","青岛市",[["市南区",120.396,36.071],["市北区",120.355,36.084],["黄岛区",119.996,35.875],["崂山区",120.467,36.103],["李沧区",120.421,36.16],["城阳区",120.389,36.307],["即墨区",120.447,36.391],["胶州市",120.006,36.286],["平度市",119.959,36.789],["莱西市",120.526,36.865]],[120.355,36.083]],["淄博","淄博市",[["淄川区",117.968,36.647],["张店区",118.054,36.807],["博山区",117.858,36.498],["临淄区",118.306,36.817],["周村区",117.851,36.804],["桓台县",118.102,36.96],["高青县",117.83,37.17],["沂源县",118.166,36.186]],[118.048,36.815]],["枣庄","枣庄市",[["市中区",117.557,34.857],["薛城区",117.265,34.798],["峄城区",117.586,34.768],["台儿庄区",117.735,34.565],["山亭区",117.459,35.096],["滕州市",117.162,35.088]],[117.558,34.856]],["东营","东营市",[["东营区",118.508,37.462],["河口区",118.53,37.886],["垦利区",118.551,37.589],["利津县",118.249,37.493],["广饶县",118.408,37.052]],[118.665,37.435]],["烟台","烟台市",[["芝罘区",121.386,37.541],["福山区",121.265,37.497],["牟平区",121.602,37.388],["莱山区",121.449,37.474],["长岛县",120.738,37.916],["龙口市",120.528,37.648],["莱阳市",120.711,36.977],["莱州市",119.942,37.183],["蓬莱市",120.763,37.811],["招远市",120.403,37.365],["栖霞市",120.834,37.306],["海阳市",121.168,36.781]],[121.391,37.539]],["潍坊","潍坊市",[["潍城区",119.104,36.71],["寒亭区",119.208,36.772],["坊子区",119.166,36.655],["奎文区",119.137,36.709],["临朐县",118.54,36.516],["昌乐县",118.84,36.703],["青州市",118.485,36.698],["诸城市",119.403,35.997],["寿光市",118.736,36.874],["安丘市",119.207,36.427],["高密市",119.757,36.378],["昌邑市",119.395,36.855]],[119.107,36.709]],["济宁","济宁市",[["任城区",116.595,35.415],["兖州区",116.829,35.556],["微山县",117.129,34.81],["鱼台县",116.65,34.998],["金乡县",116.31,35.07],["嘉祥县",116.343,35.398],["汶上县",116.487,35.722],["泗水县",117.274,35.653],["梁山县",116.09,35.802],["曲阜市",116.992,35.593],["邹城市",116.967,35.405]],[116.587,35.415]],["泰安","泰安市",[["泰山区",117.13,36.189],["岱岳区",117.044,36.184],["宁阳县",116.799,35.768],["东平县",116.461,35.93],["新泰市",117.766,35.91],["肥城市",116.764,36.186]],[117.129,36.195]],["威海","威海市",[["环翠区",122.116,37.511],["文登区",122.057,37.196],["荣成市",122.423,37.16],["乳山市",121.536,36.92]],[122.116,37.51]],["日照","日照市",[["东港区",119.458,35.426],["岚山区",119.316,35.12],["五莲县",119.207,35.752],["莒县",118.833,35.588]],[119.461,35.429]],["临沂","临沂市",[["兰山区",118.328,35.062],["罗庄区",118.285,34.997],["河东区",118.398,35.085],["沂南县",118.455,35.547],["郯城县",118.343,34.615],["沂水县",118.635,35.787],["兰陵县",118.05,34.856],["费县",117.969,35.269],["平邑县",117.632,35.512],["莒南县",118.838,35.176],["蒙阴县",117.943,35.712],["临沭县",118.648,34.917]],[118.326,35.065]],["德州","德州市",[["德城区",116.307,37.454],["陵城区",116.575,37.333],["宁津县",116.794,37.65],["庆云县",117.391,37.778],["临邑县",116.867,37.192],["齐河县",116.758,36.795],["平原县",116.434,37.164],["夏津县",116.004,36.951],["武城县",116.079,37.21],["乐陵市",117.217,37.729],["禹城市",116.643,36.934]],[116.307,37.454]],["聊城","聊城市",[["东昌府区",115.98,36.456],["阳谷县",115.784,36.114],["莘县",115.667,36.238],["茌平区",116.253,36.592],["东阿县",116.249,36.336],["冠县",115.445,36.484],["高唐县",116.23,36.86],["临清市",115.713,36.843]],[115.98,36.456]],["滨州","滨州市",[["滨城区",118.02,37.385],["沾化区",118.13,37.698],["惠民县",117.509,37.484],["阳信县",117.581,37.64],["无棣县",117.616,37.741],["博兴县",118.123,37.147],["邹平市",117.737,36.878]],[118.017,37.384]],["菏泽","菏泽市",[["牡丹区",115.471,35.243],["定陶区",115.57,35.073],["曹县",115.549,34.823],["单县",116.083,34.791],["成武县",115.897,34.947],["巨野县",116.089,35.391],["郓城县",115.939,35.595],["鄄城县",115.514,35.56],["东明县",115.098,35.29]],[115.469,35.247]]]],["河南","河南省",[113.665,34.758],[["郑州","郑州市",[["中原区",113.612,34.748],["二七区",113.645,34.731],["管城回族区",113.685,34.746],["金水区",113.686,34.776],["上街区",113.298,34.809],["惠济区",113.618,34.829],["中牟县",114.023,34.722],["巩义市",112.983,34.752],["荥阳市",113.392,34.789],["新密市",113.381,34.538],["新郑市",113.74,34.394],["登封市",113.038,34.46]],[113.665,34.758]],["开封","开封市",[["龙亭区",114.353,34.8],["顺河回族区",114.365,34.8],["鼓楼区",114.349,34.792],["禹王台区",114.35,34.78],["祥符区",114.438,34.756],["杞县",114.77,34.555],["通许县",114.468,34.477],["尉氏县",114.194,34.412],["兰考县",114.821,34.83]],[114.341,34.797]],["洛阳","洛阳市",[["老城区",112.477,34.683],["西工区",112.443,34.668],["瀍河回族区",112.492,34.685],["涧西区",112.399,34.654],["吉利区",112.585,34.899],["洛龙区",112.457,34.619],["孟津县",112.444,34.826],["新安县",112.141,34.729],["栾川县",111.618,33.783],["嵩县",112.088,34.132],["汝阳县",112.474,34.153],["宜阳县",112.18,34.516],["洛宁县",111.655,34.387],["伊川县",112.429,34.423],["偃师市",112.788,34.723]],[112.434,34.663]],["平顶山","平顶山市",[["新华区",113.299,33.738],["卫东区",113.31,33.739],["石龙区",112.89,33.902],["湛河区",113.321,33.726],["宝丰县",113.067,33.866],["叶县",113.358,33.621],["鲁山县",112.907,33.74],["郏县",113.22,33.972],["舞钢市",113.526,33.302],["汝州市",112.845,34.167]],[113.308,33.735]],["安阳","安阳市",[["文峰区",114.353,36.098],["北关区",114.353,36.11],["殷都区",114.3,36.109],["龙安区",114.324,36.096],["安阳县",114.13,36.131],["汤阴县",114.362,35.922],["滑县",114.524,35.575],["内黄县",114.905,35.954],["林州市",113.824,36.063]],[114.352,36.103]],["鹤壁","鹤壁市",[["鹤山区",114.167,35.936],["山城区",114.184,35.896],["淇滨区",114.294,35.748],["浚县",114.55,35.671],["淇县",114.2,35.609]],[114.295,35.748]],["新乡","新乡市",[["红旗区",113.878,35.303],["卫滨区",113.866,35.305],["凤泉区",113.907,35.38],["牧野区",113.897,35.313],["新乡县",113.806,35.19],["获嘉县",113.657,35.262],["原阳县",113.966,35.054],["延津县",114.201,35.15],["封丘县",114.423,35.041],["长垣市",114.674,35.196],["卫辉市",114.066,35.404],["辉县市",113.803,35.461]],[113.884,35.303]],["焦作","焦作市",[["解放区",113.226,35.241],["中站区",113.175,35.236],["马村区",113.322,35.265],["山阳区",113.268,35.215],["修武县",113.447,35.23],["博爱县",113.069,35.17],["武陟县",113.408,35.099],["温县",113.079,34.941],["沁阳市",112.935,35.089],["孟州市",112.787,34.91]],[113.238,35.239]],["濮阳","濮阳市",[["华龙区",115.032,35.76],["清丰县",115.107,35.902],["南乐县",115.204,36.075],["范县",115.504,35.852],["台前县",115.856,35.996],["濮阳县",115.024,35.71]],[115.041,35.768]],["许昌","许昌市",[["魏都区",113.828,34.027],["建安区",113.843,34.005],["鄢陵县",114.189,34.101],["襄城县",113.493,33.856],["禹州市",113.471,34.154],["长葛市",113.769,34.219]],[113.826,34.023]],["漯河","漯河市",[["源汇区",114.018,33.565],["郾城区",114.017,33.589],["召陵区",114.052,33.568],["舞阳县",113.611,33.436],["临颍县",113.939,33.806]],[114.026,33.576]],["三门峡","三门峡市",[["湖滨区",111.195,34.778],["陕州区",111.104,34.72],["渑池县",111.763,34.763],["卢氏县",111.053,34.054],["义马市",111.869,34.747],["灵宝市",110.886,34.521]],[111.194,34.777]],["南阳","南阳市",[["宛城区",112.545,32.995],["卧龙区",112.529,32.99],["南召县",112.436,33.489],["方城县",113.011,33.255],["西峡县",111.486,33.303],["镇平县",112.233,33.037],["内乡县",111.844,33.046],["淅川县",111.489,33.136],["社旗县",112.938,33.056],["唐河县",112.838,32.688],["新野县",112.366,32.524],["桐柏县",113.406,32.367],["邓州市",112.093,32.682]],[112.541,32.999]],["商丘","商丘市",[["梁园区",115.655,34.437],["睢阳区",115.654,34.391],["民权县",115.148,34.648],["睢县",115.07,34.428],["宁陵县",115.32,34.449],["柘城县",115.307,34.075],["虞城县",115.864,34.4],["夏邑县",116.14,34.241],["永城市",116.45,33.931]],[115.65,34.437]],["信阳","信阳市",[["浉河区",114.075,32.123],["平桥区",114.126,32.098],["罗山县",114.533,32.203],["光山县",114.904,32.01],["新县",114.877,31.635],["商城县",115.406,31.8],["固始县",115.667,32.183],["潢川县",115.05,32.134],["淮滨县",115.415,32.453],["息县",114.741,32.345]],[114.075,32.123]],["周口","周口市",[["川汇区",114.652,33.615],["扶沟县",114.392,34.054],["西华县",114.53,33.784],["商水县",114.609,33.544],["沈丘县",115.078,33.396],["郸城县",115.189,33.644],["淮阳区",114.87,33.733],["太康县",114.854,34.065],["鹿邑县",115.486,33.861],["项城市",114.9,33.443]],[114.65,33.62]],["驻马店","驻马店市",[["驿城区",114.029,32.978],["西平县",114.027,33.382],["上蔡县",114.267,33.265],["平舆县",114.637,32.956],["正阳县",114.389,32.602],["确山县",114.027,32.802],["泌阳县",113.326,32.725],["汝南县",114.359,33.005],["遂平县",114.004,33.147],["新蔡县",114.975,32.75]],[114.025,32.98]],["济源","济源市",[],[112.59,35.09]]]],["湖北","湖北省",[114.299,30.584],[["武汉","武汉市",[["江岸区",114.303,30.595],["江汉区",114.283,30.579],["硚口区",114.265,30.571],["汉阳区",114.266,30.549],["武昌区",114.307,30.547],["青山区",114.397,30.634],["洪山区",114.401,30.504],["东西湖区",114.142,30.622],["汉南区",114.081,30.31],["蔡甸区",114.029,30.582],["江夏区",114.314,30.349],["黄陂区",114.374,30.874],["新洲区",114.802,30.842]],[114.299,30.584]],["黄石","黄石市",[["黄石港区",115.09,30.212],["西塞山区",115.093,30.205],["下陆区",114.976,30.178],["铁山区",114.901,30.206],["阳新县",115.213,29.842],["大冶市",114.975,30.099]],[115.077,30.22]],["十堰","十堰市",[["茅箭区",110.786,32.644],["张湾区",110.772,32.653],["郧阳区",110.812,32.838],["郧西县",110.426,32.991],["竹山县",110.23,32.226],["竹溪县",109.717,32.315],["房县",110.742,32.055],["丹江口市",111.514,32.539]],[110.788,32.647]],["宜昌","宜昌市",[["西陵区",111.295,30.702],["伍家岗区",111.307,30.679],["点军区",111.268,30.692],["猇亭区",111.428,30.531],["夷陵区",111.327,30.77],["远安县",111.643,31.06],["兴山县",110.754,31.348],["秭归县",110.977,30.824],["长阳土家族自治县",111.198,30.467],["五峰土家族自治县",110.675,30.199],["宜都市",111.454,30.387],["当阳市",111.793,30.824],["枝江市",111.752,30.425]],[111.291,30.703]],["襄阳","襄阳市",[["襄城区",112.15,32.015],["樊城区",112.14,32.059],["襄州区",112.197,32.086],["南漳县",111.844,31.777],["谷城县",111.64,32.263],["保康县",111.262,31.874],["老河口市",111.676,32.385],["枣阳市",112.765,32.123],["宜城市",112.261,31.709]],[112.144,32.042]],["鄂州","鄂州市",[["梁子湖区",114.682,30.098],["华容区",114.741,30.534],["鄂城区",114.89,30.397]],[114.891,30.397]],["荆门","荆门市",[["东宝区",112.205,31.033],["掇刀区",112.198,30.981],["沙洋县",112.595,30.704],["钟祥市",112.587,31.166],["京山市",113.115,31.022]],[112.204,31.035]],["孝感","孝感市",[["孝南区",113.926,30.926],["孝昌县",113.989,31.252],["大悟县",114.126,31.565],["云梦县",113.751,31.022],["应城市",113.574,30.939],["安陆市",113.69,31.262],["汉川市",113.835,30.652]],[113.927,30.926]],["荆州","荆州市",[["沙市区",112.257,30.316],["荆州区",112.195,30.351],["公安县",112.23,30.059],["监利县",112.904,29.82],["江陵县",112.417,30.034],["石首市",112.409,29.716],["洪湖市",113.47,29.813],["松滋市",111.778,30.176]],[112.238,30.327]],["黄冈","黄冈市",[["黄州区",114.879,30.447],["团风县",114.872,30.636],["红安县",114.615,31.285],["罗田县",115.399,30.782],["英山县",115.678,30.736],["浠水县",115.263,30.455],["蕲春县",115.434,30.235],["黄梅县",115.943,30.075],["麻城市",115.025,31.178],["武穴市",115.562,29.849]],[114.879,30.448]],["咸宁","咸宁市",[["咸安区",114.334,29.825],["嘉鱼县",113.922,29.973],["通城县",113.814,29.246],["崇阳县",114.05,29.541],["通山县",114.493,29.604],["赤壁市",113.884,29.717]],[114.329,29.833]],["随州","随州市",[["曾都区",113.375,31.718],["随县",113.301,31.854],["广水市",113.827,31.618]],[113.374,31.717]],["恩施土家族苗族自治州","恩施土家族苗族自治州",[["恩施市",109.487,30.282],["利川市",108.943,30.294],["建始县",109.724,30.602],["巴东县",110.337,31.041],["宣恩县",109.483,29.989],["咸丰县",109.15,29.679],["来凤县",109.408,29.507],["鹤峰县",110.034,29.887]],[109.487,30.283]],["仙桃","仙桃市",[],[113.454,30.365]],["潜江","潜江市",[],[112.897,30.421]],["天门","天门市",[],[113.166,30.653]],["神农架林区","神农架林区",[],[110.672,31.744]]]],["湖南","湖南省",[112.982,28.194],[["长沙","长沙市",[["芙蓉区",112.988,28.193],["天心区",112.973,28.192],["岳麓区",112.912,28.213],["开福区",112.986,28.201],["雨花区",113.016,28.11],["望城区",112.82,28.347],["长沙县",113.08,28.238],["浏阳市",113.633,28.141],["宁乡市",112.553,28.254]],[112.982,28.194]],["株洲","株洲市",[["荷塘区",113.163,27.833],["芦淞区",113.155,27.827],["石峰区",113.113,27.872],["天元区",113.136,27.827],["渌口区",113.146,27.706],["攸县",113.346,27.0],["茶陵县",113.547,26.79],["炎陵县",113.777,26.489],["醴陵市",113.507,27.658]],[113.152,27.836]],["湘潭","湘潭市",[["雨湖区",112.907,27.861],["岳塘区",112.928,27.829],["湘潭县",112.953,27.779],["湘乡市",112.525,27.735],["韶山市",112.528,27.923]],[112.944,27.83]],["衡阳","衡阳市",[["珠晖区",112.626,26.891],["雁峰区",112.612,26.894],["石鼓区",112.608,26.904],["蒸湘区",112.571,26.891],["南岳区",112.734,27.241],["衡阳县",112.38,26.962],["衡南县",112.677,26.74],["衡山县",112.87,27.235],["衡东县",112.95,27.084],["祁东县",112.111,26.787],["耒阳市",112.847,26.414],["常宁市",112.397,26.407]],[112.608,26.9]],["邵阳","邵阳市",[["双清区",111.48,27.24],["大祥区",111.463,27.234],["北塔区",111.452,27.246],["邵东市",111.743,27.257],["新邵县",111.46,27.311],["邵阳县",111.276,26.99],["隆回县",111.039,27.116],["洞口县",110.579,27.062],["绥宁县",110.155,26.581],["新宁县",110.859,26.439],["城步苗族自治县",110.313,26.364],["武冈市",110.637,26.732]],[111.469,27.238]],["岳阳","岳阳市",[["岳阳楼区",113.121,29.367],["云溪区",113.274,29.473],["君山区",113.004,29.438],["岳阳县",113.116,29.145],["华容县",112.559,29.524],["湘阴县",112.89,28.677],["平江县",113.594,28.702],["汨罗市",113.079,28.803],["临湘市",113.451,29.472]],[113.133,29.37]],["常德","常德市",[["武陵区",111.691,29.04],["鼎城区",111.685,29.014],["安乡县",112.172,29.414],["汉寿县",111.969,28.907],["澧县",111.762,29.643],["临澧县",111.646,29.443],["桃源县",111.485,28.903],["石门县",111.379,29.585],["津市市",111.88,29.631]],[111.691,29.04]],["张家界","张家界市",[["永定区",110.485,29.126],["武陵源区",110.548,29.348],["慈利县",111.133,29.424],["桑植县",110.164,29.4]],[110.48,29.127]],["益阳","益阳市",[["资阳区",112.331,28.593],["赫山区",112.361,28.568],["南县",112.41,29.372],["桃江县",112.14,28.521],["安化县",111.222,28.377],["沅江市",112.361,28.84]],[112.355,28.57]],["郴州","郴州市",[["北湖区",113.032,25.793],["苏仙区",113.039,25.793],["桂阳县",112.734,25.737],["宜章县",112.948,25.394],["永兴县",113.115,26.129],["嘉禾县",112.371,25.587],["临武县",112.565,25.279],["汝城县",113.686,25.554],["桂东县",113.946,26.074],["安仁县",113.272,26.709],["资兴市",113.237,25.974]],[113.032,25.794]],["永州","永州市",[["零陵区",111.626,26.223],["冷水滩区",111.607,26.434],["祁阳县",111.857,26.586],["东安县",111.313,26.397],["双牌县",111.662,25.959],["道县",111.592,25.518],["江永县",111.347,25.268],["宁远县",111.945,25.584],["蓝山县",112.194,25.375],["新田县",112.22,25.907],["江华瑶族自治县",111.577,25.183]],[111.608,26.435]],["怀化","怀化市",[["鹤城区",109.982,27.548],["中方县",109.948,27.437],["沅陵县",110.399,28.456],["辰溪县",110.197,28.005],["溆浦县",110.593,27.904],["会同县",109.721,26.871],["麻阳苗族自治县",109.803,27.866],["新晃侗族自治县",109.174,27.36],["芷江侗族自治县",109.688,27.438],["靖州苗族侗族自治县",109.691,26.574],["通道侗族自治县",109.783,26.158],["洪江市",109.832,27.202]],[109.978,27.55]],["娄底","娄底市",[["娄星区",112.008,27.727],["双峰县",112.198,27.459],["新化县",111.307,27.737],["冷水江市",111.435,27.686],["涟源市",111.671,27.692]],[112.008,27.728]],["湘西土家族苗族自治州","湘西土家族苗族自治州",[["吉首市",109.738,28.315],["泸溪县",110.214,28.215],["凤凰县",109.599,27.948],["花垣县",109.479,28.581],["保靖县",109.651,28.71],["古丈县",109.95,28.617],["永顺县",109.853,28.998],["龙山县",109.441,29.453]],[109.74,28.314]]]],["广东","广东省",[113.281,23.125],[["广州","广州市",[["荔湾区",113.243,23.125],["越秀区",113.281,23.126],["海珠区",113.262,23.103],["天河区",113.335,23.136],["白云区",113.263,23.162],["黄埔区",113.451,23.103],["番禺区",113.365,22.939],["花都区",113.211,23.392],["南沙区",113.537,22.795],["从化区",113.587,23.545],["增城区",113.83,23.29]],[113.281,23.125]],["韶关","韶关市",[["武江区",113.588,24.8],["浈江区",113.599,24.804],["曲江区",113.606,24.68],["始兴县",114.067,24.948],["仁化县",113.749,25.088],["翁源县",114.131,24.354],["乳源瑶族自治县",113.278,24.776],["新丰县",114.207,24.055],["乐昌市",113.352,25.128],["南雄市",114.311,25.115]],[113.592,24.801]],["深圳","深圳市",[["罗湖区",114.124,22.555],["福田区",114.051,22.541],["南山区",113.929,22.531],["宝安区",113.829,22.755],["龙岗区",114.251,22.722],["盐田区",114.235,22.555],["龙华区",114.044,22.692],["坪山区",114.338,22.694],["光明区",113.936,22.749]],[114.086,22.547]],["珠海","珠海市",[["香洲区",113.55,22.271],["斗门区",113.298,22.209],["金湾区",113.345,22.139]],[113.554,22.225]],["汕头","汕头市",[["龙湖区",116.732,23.374],["金平区",116.704,23.367],["濠江区",116.73,23.279],["潮阳区",116.603,23.262],["潮南区",116.424,23.25],["澄海区",116.763,23.468],["南澳县",117.027,23.42]],[116.708,23.371]],["佛山","佛山市",[["禅城区",113.112,23.02],["南海区",113.146,23.032],["顺德区",113.282,22.759],["三水区",112.899,23.165],["高明区",112.882,22.894]],[113.123,23.029]],["江门","江门市",[["蓬江区",113.079,22.597],["江海区",113.121,22.572],["新会区",113.039,22.52],["台山市",112.793,22.251],["开平市",112.692,22.366],["鹤山市",112.962,22.768],["恩平市",112.314,22.183]],[113.095,22.59]],["湛江","湛江市",[["赤坎区",110.362,21.273],["霞山区",110.406,21.194],["坡头区",110.456,21.244],["麻章区",110.329,21.266],["遂溪县",110.255,21.377],["徐闻县",110.176,20.326],["廉江市",110.285,21.611],["雷州市",110.088,20.909],["吴川市",110.781,21.428]],[110.365,21.275]],["茂名","茂名市",[["茂南区",110.921,21.66],["电白区",111.007,21.507],["高州市",110.853,21.915],["化州市",110.638,21.655],["信宜市",110.942,22.353]],[110.919,21.66]],["肇庆","肇庆市",[["端州区",112.472,23.053],["鼎湖区",112.565,23.156],["高要区",112.461,23.028],["广宁县",112.44,23.631],["怀集县",112.182,23.913],["封开县",111.503,23.435],["德庆县",111.782,23.142],["四会市",112.695,23.34]],[112.473,23.052]],["惠州","惠州市",[["惠城区",114.414,23.08],["惠阳区",114.469,22.789],["博罗县",114.284,23.168],["惠东县",114.723,22.983],["龙门县",114.26,23.724]],[114.413,23.079]],["梅州","梅州市",[["梅江区",116.121,24.303],["梅县区",116.083,24.268],["大埔县",116.696,24.352],["丰顺县",116.184,23.753],["五华县",115.775,23.925],["平远县",115.892,24.57],["蕉岭县",116.171,24.653],["兴宁市",115.732,24.138]],[116.118,24.299]],["汕尾","汕尾市",[["城区",115.364,22.776],["海丰县",115.337,22.971],["陆河县",115.658,23.303],["陆丰市",115.644,22.946]],[115.364,22.774]],["河源","河源市",[["源城区",114.697,23.746],["紫金县",115.184,23.634],["龙川县",115.256,24.101],["连平县",114.496,24.364],["和平县",114.941,24.443],["东源县",114.743,23.789]],[114.698,23.746]],["阳江","阳江市",[["江城区",111.969,21.859],["阳东区",112.011,21.865],["阳西县",111.618,21.754],["阳春市",111.79,22.17]],[111.975,21.859]],["清远","清远市",[["清城区",113.049,23.689],["清新区",113.015,23.737],["佛冈县",113.534,23.867],["阳山县",112.634,24.47],["连山壮族瑶族自治县",112.087,24.567],["连南瑶族自治县",112.291,24.719],["英德市",113.405,24.186],["连州市",112.379,24.784]],[113.051,23.685]],["东莞","东莞市",[],[113.746,23.046]],["中山","中山市",[],[113.382,22.521]],["东沙群岛","东沙群岛",[],[116.887,20.618]],["潮州","潮州市",[["湘桥区",116.634,23.665],["潮安区",116.679,23.461],["饶平县",117.002,23.668]],[116.632,23.662]],["揭阳","揭阳市",[["榕城区",116.357,23.536],["揭东区",116.413,23.57],["揭西县",115.839,23.427],["惠来县",116.296,23.03],["普宁市",116.165,23.298]],[116.356,23.544]],["云浮","云浮市",[["云城区",112.045,22.931],["云安区",112.006,23.073],["新兴县",112.231,22.703],["郁南县",111.536,23.238],["罗定市",111.578,22.765]],[112.044,22.93]]]],["广西","广西壮族自治区",[108.32,22.824],[["南宁","南宁市",[["兴宁区",108.32,22.82],["青秀区",108.346,22.817],["江南区",108.31,22.8],["西乡塘区",108.307,22.833],["良庆区",108.322,22.759],["邕宁区",108.484,22.757],["武鸣区",108.281,23.157],["隆安县",107.689,23.175],["马山县",108.173,23.712],["上林县",108.604,23.432],["宾阳县",108.817,23.217],["横县",109.271,22.687]],[108.32,22.824]],["柳州","柳州市",[["城中区",109.412,24.312],["鱼峰区",109.415,24.304],["柳南区",109.396,24.287],["柳北区",109.407,24.359],["柳江区",109.335,24.258],["柳城县",109.246,24.655],["鹿寨县",109.741,24.483],["融安县",109.404,25.215],["融水苗族自治县",109.253,25.069],["三江侗族自治县",109.615,25.786]],[109.412,24.315]],["桂林","桂林市",[["秀峰区",110.292,25.279],["叠彩区",110.301,25.301],["象山区",110.285,25.262],["七星区",110.318,25.254],["雁山区",110.306,25.078],["临桂区",110.205,25.246],["阳朔县",110.495,24.775],["灵川县",110.326,25.409],["全州县",111.073,25.93],["兴安县",110.671,25.61],["永福县",109.989,24.987],["灌阳县",111.16,25.489],["龙胜各族自治县",110.009,25.796],["资源县",110.643,26.034],["平乐县",110.643,24.632],["恭城瑶族自治县",110.83,24.834],["荔浦市",110.4,24.498]],[110.299,25.274]],["梧州","梧州市",[["万秀区",111.316,23.471],["长洲区",111.276,23.478],["龙圩区",111.246,23.41],["苍梧县",111.544,23.845],["藤县",110.932,23.374],["蒙山县",110.523,24.2],["岑溪市",110.998,22.918]],[111.298,23.475]],["北海","北海市",[["海城区",109.108,21.468],["银海区",109.119,21.445],["铁山港区",109.451,21.593],["合浦县",109.201,21.664]],[109.119,21.473]],["防城港","防城港市",[["港口区",108.346,21.614],["防城区",108.358,21.765],["上思县",107.982,22.151],["东兴市",107.97,21.541]],[108.345,21.615]],["钦州","钦州市",[["钦南区",108.627,21.967],["钦北区",108.449,22.133],["灵山县",109.293,22.418],["浦北县",109.556,22.268]],[108.624,21.967]],["贵港","贵港市",[["港北区",109.595,23.108],["港南区",109.605,23.068],["覃塘区",109.416,23.133],["平南县",110.397,23.545],["桂平市",110.075,23.382]],[109.602,23.094]],["玉林","玉林市",[["玉州区",110.155,22.632],["福绵区",110.054,22.582],["容县",110.552,22.856],["陆川县",110.265,22.321],["博白县",109.98,22.271],["兴业县",109.878,22.742],["北流市",110.348,22.702]],[110.154,22.631]],["百色","百色市",[["右江区",106.616,23.898],["田阳区",106.904,23.736],["田东县",107.124,23.6],["平果县",107.58,23.32],["德保县",106.618,23.321],["那坡县",105.834,23.401],["凌云县",106.565,24.346],["乐业县",106.56,24.782],["田林县",106.235,24.29],["西林县",105.095,24.492],["隆林各族自治县",105.342,24.774],["靖西市",106.418,23.135]],[106.616,23.898]],["贺州","贺州市",[["八步区",111.552,24.412],["平桂区",111.524,24.417],["昭平县",110.811,24.173],["钟山县",111.304,24.529],["富川瑶族自治县",111.277,24.819]],[111.552,24.414]],["河池","河池市",[["金城江区",108.062,24.696],["宜州区",108.654,24.492],["南丹县",107.547,24.983],["天峨县",107.175,24.986],["凤山县",107.045,24.545],["东兰县",107.374,24.509],["罗城仫佬族自治县",108.902,24.779],["环江毛南族自治县",108.259,24.828],["巴马瑶族自治县",107.253,24.14],["都安瑶族自治县",108.103,23.935],["大化瑶族自治县",107.995,23.74]],[108.062,24.696]],["来宾","来宾市",[["兴宾区",109.231,23.733],["忻城县",108.667,24.065],["象州县",109.685,23.96],["武宣县",109.663,23.604],["金秀瑶族自治县",110.189,24.135],["合山市",108.889,23.813]],[109.23,23.734]],["崇左","崇左市",[["江州区",107.354,22.405],["扶绥县",107.912,22.636],["宁明县",107.068,22.131],["龙州县",106.858,22.344],["大新县",107.201,22.833],["天等县",107.142,23.082],["凭祥市",106.759,22.109]],[107.354,22.404]]]],["海南","海南省",[110.331,20.032],[["海口","海口市",[["秀英区",110.282,20.008],["龙华区",110.33,20.031],["琼山区",110.355,20.001],["美兰区",110.357,20.031]],[110.331,20.032]],["三亚","三亚市",[["海棠区",109.761,18.408],["吉阳区",109.512,18.247],["天涯区",109.506,18.247],["崖州区",109.174,18.352]],[109.508,18.248]],["三沙","三沙市",[["西沙群岛",111.793,16.205],["南沙群岛",116.75,11.472],["中沙群岛的岛礁及其海域",117.74,15.113]],[112.349,16.831]],["儋州","儋州市",[],[109.577,19.517]],["五指山","五指山市",[],[109.517,18.777]],["琼海","琼海市",[],[110.467,19.246]],["文昌","文昌市",[],[110.754,19.613]],["万宁","万宁市",[],[110.389,18.796]],["东方","东方市",[],[108.654,19.102]],["定安县","定安县",[],[110.349,19.685]],["屯昌县","屯昌县",[],[110.103,19.363]],["澄迈县","澄迈县",[],[110.007,19.737]],["临高县","临高县",[],[109.688,19.908]],["白沙黎族自治县","白沙黎族自治县",[],[109.453,19.225]],["昌江黎族自治县","昌江黎族自治县",[],[109.053,19.261]],["乐东黎族自治县","乐东黎族自治县",[],[109.175,18.748]],["陵水黎族自治县","陵水黎族自治县",[],[110.037,18.505]],["保亭黎族苗族自治县","保亭黎族苗族自治县",[],[109.702,18.636]],["琼中黎族苗族自治县","琼中黎族苗族自治县",[],[109.84,19.036]]]],["重庆","重庆市",[106.505,29.533],[["重庆","重庆市",[["万州区",108.38,30.808],["涪陵区",107.395,29.704],["渝中区",106.563,29.557],["大渡口区",106.486,29.481],["江北区",106.533,29.575],["沙坪坝区",106.454,29.541],["九龙坡区",106.481,29.523],["南岸区",106.561,29.524],["北碚区",106.438,29.825],["綦江区",106.651,29.028],["大足区",105.715,29.7],["渝北区",106.513,29.601],["巴南区",106.519,29.382],["黔江区",108.783,29.528],["长寿区",107.075,29.834],["江津区",106.253,29.283],["合川区",106.266,29.991],["永川区",105.895,29.349],["南川区",107.098,29.157],["璧山区",106.231,29.594],["铜梁区",106.055,29.84],["潼南区",105.842,30.19],["荣昌区",105.594,29.404],["开州区",108.413,31.168],["梁平区",107.8,30.672],["武隆区",107.757,29.324],["城口县",108.665,31.946],["丰都县",107.732,29.866],["垫江县",107.349,30.33],["忠县",108.038,30.292],["云阳县",108.698,30.931],["奉节县",109.466,31.02],["巫山县",109.879,31.075],["巫溪县",109.629,31.397],["石柱土家族自治县",108.112,29.999],["秀山土家族苗族自治县",108.996,28.445],["酉阳土家族苗族自治县",108.767,28.84],["彭水苗族土家族自治县",108.167,29.294]],[106.504962,29.533155]]]],["四川","四川省",[104.066,30.659],[["成都","成都市",[["锦江区",104.081,30.658],["青羊区",104.056,30.668],["金牛区",104.043,30.692],["武侯区",104.052,30.631],["成华区",104.103,30.66],["龙泉驿区",104.269,30.561],["青白江区",104.255,30.883],["新都区",104.16,30.824],["温江区",103.837,30.698],["双流区",103.923,30.573],["郫都区",103.888,30.809],["金堂县",104.416,30.858],["大邑县",103.522,30.587],["蒲江县",103.512,30.194],["新津县",103.812,30.414],["都江堰市",103.628,30.991],["彭州市",103.941,30.985],["邛崃市",103.461,30.413],["崇州市",103.671,30.631],["简阳市",104.55,30.391]],[104.066,30.659]],["自贡","自贡市",[["自流井区",104.778,29.343],["贡井区",104.714,29.346],["大安区",104.783,29.367],["沿滩区",104.876,29.273],["荣县",104.424,29.455],["富顺县",104.984,29.181]],[104.773,29.353]],["攀枝花","攀枝花市",[["东区",101.715,26.581],["西区",101.638,26.597],["仁和区",101.738,26.497],["米易县",102.11,26.887],["盐边县",101.852,26.678]],[101.716,26.58]],["泸州","泸州市",[["江阳区",105.445,28.883],["纳溪区",105.377,28.776],["龙马潭区",105.435,28.898],["泸县",105.376,29.151],["合江县",105.834,28.81],["叙永县",105.438,28.168],["古蔺县",105.813,28.039]],[105.443,28.889]],["德阳","德阳市",[["旌阳区",104.39,31.13],["罗江区",104.507,31.303],["中江县",104.678,31.037],["广汉市",104.282,30.977],["什邡市",104.174,31.127],["绵竹市",104.2,31.343]],[104.399,31.128]],["绵阳","绵阳市",[["涪城区",104.741,31.464],["游仙区",104.77,31.485],["安州区",104.56,31.539],["三台县",105.09,31.091],["盐亭县",105.392,31.223],["梓潼县",105.164,31.635],["北川羌族自治县",104.468,31.616],["平武县",104.531,32.408],["江油市",104.744,31.776]],[104.742,31.464]],["广元","广元市",[["利州区",105.826,32.432],["昭化区",105.964,32.323],["朝天区",105.889,32.643],["旺苍县",106.29,32.228],["青川县",105.239,32.586],["剑阁县",105.527,32.287],["苍溪县",105.94,31.732]],[105.83,32.434]],["遂宁","遂宁市",[["船山区",105.582,30.503],["安居区",105.459,30.346],["蓬溪县",105.714,30.775],["射洪市",105.382,30.869],["大英县",105.252,30.582]],[105.571,30.513]],["内江","内江市",[["市中区",105.065,29.585],["东兴区",105.067,29.6],["威远县",104.668,29.527],["资中县",104.852,29.775],["隆昌市",105.288,29.338]],[105.066,29.587]],["乐山","乐山市",[["市中区",103.755,29.588],["沙湾区",103.55,29.417],["五通桥区",103.817,29.406],["金口河区",103.078,29.246],["犍为县",103.944,29.21],["井研县",104.069,29.652],["夹江县",103.579,29.741],["沐川县",103.902,28.956],["峨边彝族自治县",103.262,29.23],["马边彝族自治县",103.547,28.839],["峨眉山市",103.492,29.597]],[103.761,29.582]],["南充","南充市",[["顺庆区",106.084,30.796],["高坪区",106.109,30.782],["嘉陵区",106.067,30.763],["南部县",106.061,31.349],["营山县",106.565,31.076],["蓬安县",106.413,31.028],["仪陇县",106.297,31.271],["西充县",105.893,30.995],["阆中市",105.975,31.58]],[106.083,30.795]],["眉山","眉山市",[["东坡区",103.832,30.048],["彭山区",103.87,30.192],["仁寿县",104.148,29.997],["洪雅县",103.375,29.905],["丹棱县",103.518,30.013],["青神县",103.846,29.831]],[103.832,30.048]],["宜宾","宜宾市",[["翠屏区",104.63,28.76],["南溪区",104.981,28.84],["叙州区",104.541,28.696],["江安县",105.069,28.728],["长宁县",104.921,28.577],["高县",104.519,28.436],["珙县",104.712,28.449],["筠连县",104.508,28.162],["兴文县",105.237,28.303],["屏山县",104.163,28.642]],[104.631,28.76]],["广安","广安市",[["广安区",106.633,30.456],["前锋区",106.893,30.496],["岳池县",106.444,30.534],["武胜县",106.292,30.344],["邻水县",106.935,30.334],["华蓥市",106.778,30.381]],[106.633,30.456]],["达州","达州市",[["通川区",107.501,31.214],["达川区",107.508,31.199],["宣汉县",107.722,31.355],["开江县",107.864,31.086],["大竹县",107.207,30.736],["渠县",106.971,30.836],["万源市",108.038,32.068]],[107.502,31.209]],["雅安","雅安市",[["雨城区",103.003,29.982],["名山区",103.112,30.085],["荥经县",102.845,29.796],["汉源县",102.677,29.35],["石棉县",102.36,29.234],["天全县",102.763,30.06],["芦山县",102.924,30.153],["宝兴县",102.813,30.369]],[103.001,29.988]],["巴中","巴中市",[["巴州区",106.754,31.858],["恩阳区",106.487,31.816],["通江县",107.248,31.912],["南江县",106.843,32.353],["平昌县",107.102,31.563]],[106.754,31.859]],["资阳","资阳市",[["雁江区",104.642,30.122],["安岳县",105.337,30.099],["乐至县",105.031,30.276]],[104.642,30.122]],["阿坝藏族羌族自治州","阿坝藏族羌族自治州",[["马尔康市",102.221,31.9],["汶川县",103.581,31.475],["理县",103.165,31.437],["茂县",103.851,31.68],["松潘县",103.599,32.638],["九寨沟县",104.236,33.262],["金川县",102.065,31.476],["小金县",102.363,30.999],["黑水县",102.991,32.062],["壤塘县",100.979,32.265],["阿坝县",101.701,32.904],["若尔盖县",102.964,33.576],["红原县",102.545,32.794]],[102.221,31.9]],["甘孜藏族自治州","甘孜藏族自治州",[["康定市",101.964,30.051],["泸定县",102.233,29.912],["丹巴县",101.886,30.877],["九龙县",101.507,29.002],["雅江县",101.016,30.032],["道孚县",101.123,30.979],["炉霍县",100.679,31.393],["甘孜县",99.992,31.62],["新龙县",100.312,30.939],["德格县",98.58,31.807],["白玉县",98.824,31.209],["石渠县",98.101,32.975],["色达县",100.332,32.269],["理塘县",100.27,29.992],["巴塘县",99.109,30.006],["乡城县",99.8,28.931],["稻城县",100.297,29.038],["得荣县",99.288,28.711]],[101.964,30.051]],["凉山彝族自治州","凉山彝族自治州",[["西昌市",102.259,27.886],["木里藏族自治县",101.28,27.927],["盐源县",101.509,27.423],["德昌县",102.179,27.404],["会理县",102.25,26.659],["会东县",102.579,26.631],["宁南县",102.757,27.065],["普格县",102.541,27.377],["布拖县",102.809,27.709],["金阳县",103.249,27.696],["昭觉县",102.844,28.011],["喜德县",102.412,28.305],["冕宁县",102.17,28.551],["越西县",102.509,28.64],["甘洛县",102.776,28.977],["美姑县",103.132,28.328],["雷波县",103.572,28.263]],[102.259,27.887]]]],["贵州","贵州省",[106.713,26.578],[["贵阳","贵阳市",[["南明区",106.716,26.574],["云岩区",106.713,26.583],["花溪区",106.671,26.41],["乌当区",106.762,26.631],["白云区",106.633,26.677],["观山湖区",106.626,26.646],["开阳县",106.969,27.057],["息烽县",106.738,27.093],["修文县",106.599,26.841],["清镇市",106.47,26.551]],[106.713,26.578]],["六盘水","六盘水市",[["钟山区",104.846,26.585],["六枝特区",105.474,26.211],["水城县",104.957,26.54],["盘州市",104.468,25.707]],[104.847,26.585]],["遵义","遵义市",[["红花岗区",106.944,27.694],["汇川区",106.937,27.707],["播州区",106.832,27.535],["桐梓县",106.827,28.132],["绥阳县",107.191,27.951],["正安县",107.442,28.55],["道真仡佬族苗族自治县",107.605,28.88],["务川仡佬族苗族自治县",107.888,28.522],["凤冈县",107.722,27.961],["湄潭县",107.486,27.766],["余庆县",107.893,27.222],["习水县",106.201,28.328],["赤水市",105.698,28.587],["仁怀市",106.412,27.803]],[106.937,27.707]],["安顺","安顺市",[["西秀区",105.946,26.248],["平坝区",106.26,26.406],["普定县",105.746,26.306],["镇宁布依族苗族自治县",105.769,26.056],["关岭布依族苗族自治县",105.618,25.944],["紫云苗族布依族自治县",106.085,25.752]],[105.932,26.246]],["毕节","毕节市",[["七星关区",105.285,27.302],["大方县",105.609,27.144],["黔西县",106.038,27.025],["金沙县",106.222,27.46],["织金县",105.769,26.668],["纳雍县",105.375,26.77],["威宁彝族回族苗族自治县",104.287,26.859],["赫章县",104.726,27.119]],[105.285,27.302]],["铜仁","铜仁市",[["碧江区",109.192,27.719],["万山区",109.212,27.519],["江口县",108.848,27.692],["玉屏侗族自治县",108.918,27.238],["石阡县",108.23,27.519],["思南县",108.256,27.941],["印江土家族苗族自治县",108.406,27.998],["德江县",108.117,28.261],["沿河土家族自治县",108.496,28.56],["松桃苗族自治县",109.203,28.165]],[109.192,27.718]],["黔西南布依族苗族自治州","黔西南布依族苗族自治州",[["兴义市",104.898,25.089],["兴仁市",105.193,25.431],["普安县",104.955,25.786],["晴隆县",105.219,25.833],["贞丰县",105.65,25.386],["望谟县",106.092,25.167],["册亨县",105.812,24.983],["安龙县",105.471,25.109]],[104.898,25.088]],["黔东南苗族侗族自治州","黔东南苗族侗族自治州",[["凯里市",107.978,26.583],["黄平县",107.901,26.897],["施秉县",108.127,27.035],["三穗县",108.681,26.96],["镇远县",108.424,27.05],["岑巩县",108.816,27.173],["天柱县",109.213,26.91],["锦屏县",109.203,26.681],["剑河县",108.44,26.727],["台江县",108.315,26.669],["黎平县",109.137,26.231],["榕江县",108.521,25.931],["从江县",108.913,25.747],["雷山县",108.08,26.381],["麻江县",107.593,26.495],["丹寨县",107.795,26.199]],[107.977,26.583]],["黔南布依族苗族自治州","黔南布依族苗族自治州",[["都匀市",107.517,26.258],["福泉市",107.514,26.703],["荔波县",107.884,25.412],["贵定县",107.234,26.581],["瓮安县",107.478,27.066],["独山县",107.543,25.826],["平塘县",107.324,25.832],["罗甸县",106.75,25.43],["长顺县",106.447,26.022],["龙里县",106.978,26.449],["惠水县",106.658,26.129],["三都水族自治县",107.877,25.985]],[107.517,26.258]]]],["云南","云南省",[102.712,25.041],[["昆明","昆明市",[["五华区",102.704,25.042],["盘龙区",102.729,25.07],["官渡区",102.723,25.021],["西山区",102.706,25.024],["东川区",103.182,26.083],["呈贡区",102.801,24.889],["晋宁区",102.595,24.667],["富民县",102.498,25.22],["宜良县",103.146,24.918],["石林彝族自治县",103.272,24.755],["嵩明县",103.039,25.335],["禄劝彝族苗族自治县",102.469,25.557],["寻甸回族彝族自治县",103.258,25.559],["安宁市",102.486,24.922]],[102.712,25.041]],["曲靖","曲靖市",[["麒麟区",103.798,25.501],["沾益区",103.819,25.601],["马龙区",103.579,25.429],["陆良县",103.655,25.023],["师宗县",103.994,24.826],["罗平县",104.309,24.886],["富源县",104.257,25.671],["会泽县",103.3,26.413],["宣威市",104.096,26.228]],[103.798,25.502]],["玉溪","玉溪市",[["红塔区",102.543,24.351],["江川区",102.75,24.291],["澄江县",102.917,24.67],["通海县",102.76,24.112],["华宁县",102.929,24.19],["易门县",102.162,24.67],["峨山彝族自治县",102.404,24.173],["新平彝族傣族自治县",101.991,24.066],["元江哈尼族彝族傣族自治县",102.0,23.598]],[102.544,24.35]],["保山","保山市",[["隆阳区",99.166,25.112],["施甸县",99.184,24.731],["龙陵县",98.694,24.592],["昌宁县",99.612,24.824],["腾冲市",98.497,25.018]],[99.167,25.112]],["昭通","昭通市",[["昭阳区",103.717,27.337],["鲁甸县",103.549,27.192],["巧家县",102.929,26.912],["盐津县",104.235,28.107],["大关县",103.892,27.747],["永善县",103.637,28.232],["绥江县",103.961,28.6],["镇雄县",104.873,27.436],["彝良县",104.048,27.627],["威信县",105.049,27.843],["水富市",104.415,28.63]],[103.717,27.337]],["丽江","丽江市",[["古城区",100.234,26.872],["玉龙纳西族自治县",100.238,26.831],["永胜县",100.751,26.686],["华坪县",101.268,26.629],["宁蒗彝族自治县",100.852,27.281]],[100.233,26.872]],["普洱","普洱市",[["思茅区",100.973,22.777],["宁洱哈尼族彝族自治县",101.045,23.063],["墨江哈尼族自治县",101.688,23.428],["景东彝族自治县",100.84,24.449],["景谷傣族彝族自治县",100.701,23.5],["镇沅彝族哈尼族拉祜族自治县",101.109,24.006],["江城哈尼族彝族自治县",101.859,22.583],["孟连傣族拉祜族佤族自治县",99.585,22.326],["澜沧拉祜族自治县",99.931,22.553],["西盟佤族自治县",99.594,22.644]],[100.972,22.777]],["临沧","临沧市",[["临翔区",100.086,23.887],["凤庆县",99.919,24.593],["云县",100.126,24.439],["永德县",99.254,24.028],["镇康县",98.827,23.761],["双江拉祜族佤族布朗族傣族自治县",99.824,23.477],["耿马傣族佤族自治县",99.402,23.535],["沧源佤族自治县",99.247,23.147]],[100.087,23.887]],["楚雄彝族自治州","楚雄彝族自治州",[["楚雄市",101.546,25.041],["双柏县",101.638,24.685],["牟定县",101.543,25.312],["南华县",101.275,25.192],["姚安县",101.238,25.505],["大姚县",101.324,25.722],["永仁县",101.671,26.056],["元谋县",101.871,25.703],["武定县",102.407,25.53],["禄丰县",102.076,25.143]],[101.546,25.042]],["红河哈尼族彝族自治州","红河哈尼族彝族自治州",[["个旧市",103.155,23.36],["开远市",103.259,23.714],["蒙自市",103.385,23.367],["弥勒市",103.437,24.408],["屏边苗族自治县",103.687,22.987],["建水县",102.82,23.618],["石屏县",102.484,23.713],["泸西县",103.76,24.532],["元阳县",102.837,23.22],["红河县",102.421,23.369],["金平苗族瑶族傣族自治县",103.228,22.78],["绿春县",102.393,22.994],["河口瑶族自治县",103.962,22.508]],[103.384,23.367]],["文山壮族苗族自治州","文山壮族苗族自治州",[["文山市",104.244,23.369],["砚山县",104.344,23.612],["西畴县",104.676,23.437],["麻栗坡县",104.702,23.124],["马关县",104.399,23.012],["丘北县",104.194,24.041],["广南县",105.057,24.05],["富宁县",105.629,23.626]],[104.244,23.37]],["西双版纳傣族自治州","西双版纳傣族自治州",[["景洪市",100.798,22.002],["勐海县",100.448,21.956],["勐腊县",101.567,21.479]],[100.798,22.002]],["大理白族自治州","大理白族自治州",[["大理市",100.241,25.593],["漾濞彝族自治县",99.958,25.67],["祥云县",100.554,25.477],["宾川县",100.579,25.826],["弥渡县",100.491,25.343],["南涧彝族自治县",100.519,25.041],["巍山彝族回族自治县",100.308,25.231],["永平县",99.534,25.461],["云龙县",99.369,25.885],["洱源县",99.952,26.111],["剑川县",99.906,26.53],["鹤庆县",100.173,26.558]],[100.226,25.589]],["德宏傣族景颇族自治州","德宏傣族景颇族自治州",[["瑞丽市",97.856,24.011],["芒市",98.578,24.437],["梁河县",98.298,24.807],["盈江县",97.934,24.71],["陇川县",97.794,24.184]],[98.578,24.437]],["怒江傈僳族自治州","怒江傈僳族自治州",[["泸水市",98.854,25.851],["福贡县",98.867,26.903],["贡山独龙族怒族自治县",98.666,27.738],["兰坪白族普米族自治县",99.421,26.454]],[98.854,25.851]],["迪庆藏族自治州","迪庆藏族自治州",[["香格里拉市",99.709,27.826],["德钦县",98.915,28.483],["维西傈僳族自治县",99.286,27.181]],[99.706,27.827]]]],["西藏","西藏自治区",[91.132,29.66],[["拉萨","拉萨市",[["城关区",91.133,29.659],["堆龙德庆区",91.003,29.647],["达孜区",91.351,29.67],["林周县",91.262,29.896],["当雄县",91.104,30.475],["尼木县",90.166,29.431],["曲水县",90.738,29.35],["墨竹工卡县",91.731,29.835]],[91.132,29.66]],["日喀则","日喀则市",[["桑珠孜区",88.887,29.267],["南木林县",89.099,29.68],["江孜县",89.605,28.909],["定日县",87.124,28.657],["萨迦县",88.023,28.901],["拉孜县",87.637,29.085],["昂仁县",87.236,29.295],["谢通门县",88.261,29.432],["白朗县",89.264,29.107],["仁布县",89.843,29.23],["康马县",89.683,28.555],["定结县",87.768,28.364],["仲巴县",84.033,29.768],["亚东县",88.907,27.483],["吉隆县",85.298,28.852],["聂拉木县",85.982,28.156],["萨嘎县",85.235,29.328],["岗巴县",88.519,28.274]],[88.885,29.268]],["昌都","昌都市",[["卡若区",97.178,31.137],["江达县",98.218,31.5],["贡觉县",98.271,30.859],["类乌齐县",96.601,31.213],["丁青县",95.598,31.411],["察雅县",97.566,30.653],["八宿县",96.918,30.053],["左贡县",97.841,29.671],["芒康县",98.596,29.687],["洛隆县",95.823,30.742],["边坝县",94.708,30.934]],[97.178,31.137]],["林芝","林芝市",[["巴宜区",94.361,29.654],["工布江达县",93.247,29.884],["米林县",94.214,29.214],["墨脱县",95.332,29.326],["波密县",95.768,29.859],["察隅县",97.465,28.66],["朗县",93.073,29.045]],[94.362,29.655]],["山南","山南市",[["乃东区",91.765,29.236],["扎囊县",91.338,29.246],["贡嘎县",90.985,29.289],["桑日县",92.016,29.26],["琼结县",91.684,29.025],["曲松县",92.201,29.064],["措美县",91.432,28.437],["洛扎县",90.858,28.386],["加查县",92.591,29.141],["隆子县",92.463,28.409],["错那县",91.96,27.992],["浪卡子县",90.399,28.968]],[91.767,29.236]],["那曲","那曲市",[["色尼区",92.062,31.476],["嘉黎县",93.233,30.641],["比如县",93.68,31.48],["聂荣县",92.304,32.108],["安多县",91.682,32.26],["申扎县",88.71,30.929],["索县",93.785,31.886],["班戈县",90.012,31.395],["巴青县",94.054,31.919],["尼玛县",87.237,31.785],["双湖县",88.839,33.187]],[92.06,31.476]],["阿里地区","阿里地区",[["普兰县",81.178,30.292],["札达县",79.803,31.479],["噶尔县",80.105,32.503],["日土县",79.732,33.382],["革吉县",81.143,32.389],["改则县",84.062,32.302],["措勤县",85.159,31.017]],[80.105,32.503]]]],["陕西","陕西省",[108.948,34.263],[["西安","西安市",[["新城区",108.96,34.269],["碑林区",108.947,34.251],["莲湖区",108.933,34.266],["灞桥区",109.067,34.267],["未央区",108.946,34.308],["雁塔区",108.927,34.213],["阎良区",109.228,34.662],["临潼区",109.214,34.372],["长安区",108.942,34.157],["高陵区",109.089,34.535],["鄠邑区",108.607,34.109],["蓝田县",109.318,34.156],["周至县",108.216,34.162]],[108.948,34.263]],["铜川","铜川市",[["王益区",109.076,35.069],["印台区",109.101,35.112],["耀州区",108.963,34.91],["宜君县",109.118,35.399]],[108.98,34.917]],["宝鸡","宝鸡市",[["渭滨区",107.144,34.371],["金台区",107.15,34.375],["陈仓区",107.384,34.353],["凤翔县",107.401,34.522],["岐山县",107.624,34.443],["扶风县",107.891,34.375],["眉县",107.752,34.272],["陇县",106.857,34.893],["千阳县",107.133,34.643],["麟游县",107.797,34.678],["凤县",106.525,33.912],["太白县",107.317,34.059]],[107.145,34.369]],["咸阳","咸阳市",[["秦都区",108.699,34.33],["杨陵区",108.086,34.271],["渭城区",108.731,34.337],["三原县",108.943,34.614],["泾阳县",108.838,34.528],["乾县",108.247,34.527],["礼泉县",108.428,34.483],["永寿县",108.143,34.693],["长武县",107.796,35.206],["旬邑县",108.337,35.112],["淳化县",108.581,34.798],["武功县",108.213,34.26],["兴平市",108.488,34.297],["彬州市",108.084,35.034]],[108.705,34.333]],["渭南","渭南市",[["临渭区",109.503,34.501],["华州区",109.761,34.512],["潼关县",110.247,34.545],["大荔县",109.943,34.795],["合阳县",110.148,35.237],["澄城县",109.938,35.184],["蒲城县",109.59,34.956],["白水县",109.594,35.177],["富平县",109.187,34.747],["韩城市",110.452,35.475],["华阴市",110.09,34.565]],[109.503,34.499]],["延安","延安市",[["宝塔区",109.491,36.596],["安塞区",109.325,36.864],["延长县",110.013,36.578],["延川县",110.19,36.882],["子长市",109.676,37.142],["志丹县",108.769,36.823],["吴起县",108.177,36.925],["甘泉县",109.35,36.278],["富县",109.384,35.996],["洛川县",109.436,35.762],["宜川县",110.176,36.05],["黄龙县",109.835,35.583],["黄陵县",109.262,35.58]],[109.491,36.597]],["汉中","汉中市",[["汉台区",107.028,33.078],["南郑区",106.942,33.003],["城固县",107.33,33.153],["洋县",107.55,33.223],["西乡县",107.766,32.988],["勉县",106.68,33.156],["宁强县",106.257,32.831],["略阳县",106.154,33.33],["镇巴县",107.895,32.536],["留坝县",106.924,33.613],["佛坪县",107.989,33.521]],[107.029,33.078]],["榆林","榆林市",[["榆阳区",109.748,38.299],["横山区",109.293,37.964],["府谷县",111.07,39.029],["靖边县",108.806,37.596],["定边县",107.601,37.595],["绥德县",110.265,37.508],["米脂县",110.179,37.759],["佳县",110.493,38.022],["吴堡县",110.739,37.452],["清涧县",110.121,37.088],["子洲县",110.035,37.612],["神木市",110.497,38.836]],[109.741,38.29]],["安康","安康市",[["汉滨区",109.029,32.691],["汉阴县",108.511,32.891],["石泉县",108.251,33.039],["宁陕县",108.314,33.312],["紫阳县",108.538,32.52],["岚皋县",108.901,32.311],["平利县",109.362,32.388],["镇坪县",109.526,31.883],["旬阳县",109.368,32.834],["白河县",110.114,32.809]],[109.029,32.69]],["商洛","商洛市",[["商州区",109.938,33.869],["洛南县",110.146,34.089],["丹凤县",110.332,33.695],["商南县",110.885,33.526],["山阳县",109.88,33.53],["镇安县",109.151,33.424],["柞水县",109.111,33.683]],[109.94,33.868]]]],["甘肃","甘肃省",[103.824,36.058],[["兰州","兰州市",[["城关区",103.841,36.049],["七里河区",103.784,36.067],["西固区",103.622,36.1],["安宁区",103.724,36.103],["红古区",102.862,36.344],["永登县",103.262,36.734],["皋兰县",103.949,36.331],["榆中县",104.115,35.844]],[103.824,36.058]],["嘉峪关","嘉峪关市",[],[98.277,39.787]],["金昌","金昌市",[["金川区",102.188,38.514],["永昌县",101.972,38.247]],[102.188,38.514]],["白银","白银市",[["白银区",104.174,36.546],["平川区",104.819,36.729],["靖远县",104.687,36.561],["会宁县",105.054,35.692],["景泰县",104.066,37.194]],[104.174,36.546]],["天水","天水市",[["秦州区",105.724,34.579],["麦积区",105.898,34.564],["清水县",106.14,34.753],["秦安县",105.673,34.862],["甘谷县",105.332,34.747],["武山县",104.892,34.722],["张家川回族自治县",106.212,34.993]],[105.725,34.579]],["武威","武威市",[["凉州区",102.634,37.93],["民勤县",103.091,38.625],["古浪县",102.898,37.471],["天祝藏族自治县",103.142,36.972]],[102.635,37.93]],["张掖","张掖市",[["甘州区",100.455,38.932],["肃南裕固族自治县",99.617,38.837],["民乐县",100.817,38.434],["临泽县",100.166,39.152],["高台县",99.817,39.376],["山丹县",101.088,38.785]],[100.455,38.933]],["平凉","平凉市",[["崆峒区",106.684,35.542],["泾川县",107.365,35.335],["灵台县",107.621,35.064],["崇信县",107.031,35.305],["庄浪县",106.042,35.203],["静宁县",105.733,35.525],["华亭市",106.649,35.215]],[106.685,35.543]],["酒泉","酒泉市",[["肃州区",98.511,39.744],["金塔县",98.903,39.983],["瓜州县",95.781,40.517],["肃北蒙古族自治县",94.877,39.512],["阿克塞哈萨克族自治县",94.338,39.632],["玉门市",97.037,40.287],["敦煌市",94.664,40.141]],[98.511,39.744]],["庆阳","庆阳市",[["西峰区",107.639,35.734],["庆城县",107.886,36.014],["环县",107.309,36.569],["华池县",107.986,36.457],["合水县",108.02,35.819],["正宁县",108.361,35.491],["宁县",107.921,35.502],["镇原县",107.196,35.678]],[107.638,35.734]],["定西","定西市",[["安定区",104.626,35.58],["通渭县",105.25,35.209],["陇西县",104.638,35.003],["渭源县",104.212,35.133],["临洮县",103.862,35.376],["漳县",104.467,34.849],["岷县",104.04,34.439]],[104.626,35.58]],["陇南","陇南市",[["武都区",104.93,33.388],["成县",105.734,33.74],["文县",104.682,32.942],["宕昌县",104.394,34.043],["康县",105.61,33.328],["西和县",105.3,34.014],["礼县",105.182,34.189],["徽县",106.086,33.768],["两当县",106.307,33.911]],[104.929,33.389]],["临夏回族自治州","临夏回族自治州",[["临夏市",103.212,35.599],["临夏县",102.994,35.492],["康乐县",103.71,35.372],["永靖县",103.32,35.939],["广河县",103.576,35.482],["和政县",103.35,35.426],["东乡族自治县",103.39,35.664],["积石山保安族东乡族撒拉族自治县",102.877,35.713]],[103.212,35.599]],["甘南藏族自治州","甘南藏族自治州",[["合作市",102.911,34.986],["临潭县",103.353,34.692],["卓尼县",103.509,34.588],["舟曲县",104.37,33.783],["迭部县",103.221,34.055],["玛曲县",102.076,33.998],["碌曲县",102.488,34.59],["夏河县",102.521,35.201]],[102.911,34.986]]]],["青海","青海省",[101.779,36.623],[["西宁","西宁市",[["城东区",101.796,36.616],["城中区",101.785,36.621],["城西区",101.764,36.628],["城北区",101.761,36.648],["大通回族土族自治县",101.684,36.931],["湟中县",101.569,36.5],["湟源县",101.263,36.685]],[101.779,36.623]],["海东","海东市",[["乐都区",102.402,36.48],["平安区",102.104,36.503],["民和回族土族自治县",102.804,36.329],["互助土族自治县",101.957,36.84],["化隆回族自治县",102.262,36.098],["循化撒拉族自治县",102.487,35.847]],[102.103,36.503]],["海北藏族自治州","海北藏族自治州",[["门源回族自治县",101.618,37.377],["祁连县",100.25,38.175],["海晏县",100.9,36.96],["刚察县",100.138,37.326]],[100.901,36.959]],["黄南藏族自治州","黄南藏族自治州",[["同仁县",102.018,35.516],["尖扎县",102.032,35.938],["泽库县",101.469,35.037],["河南蒙古族自治县",101.612,34.735]],[102.02,35.518]],["海南藏族自治州","海南藏族自治州",[["共和县",100.62,36.28],["同德县",100.579,35.254],["贵德县",101.432,36.04],["兴海县",99.987,35.589],["贵南县",100.748,35.587]],[100.62,36.28]],["果洛藏族自治州","果洛藏族自治州",[["玛沁县",100.244,34.473],["班玛县",100.738,32.932],["甘德县",99.903,33.967],["达日县",99.652,33.753],["久治县",101.485,33.43],["玛多县",98.211,34.915]],[100.242,34.474]],["玉树藏族自治州","玉树藏族自治州",[["玉树市",97.009,33.004],["杂多县",95.293,32.892],["称多县",97.111,33.368],["治多县",95.617,33.852],["囊谦县",96.48,32.203],["曲麻莱县",95.801,34.127]],[97.009,33.004]],["海西蒙古族藏族自治州","海西蒙古族藏族自治州",[["格尔木市",94.906,36.402],["德令哈市",97.37,37.375],["茫崖市",90.856,38.247],["乌兰县",98.48,36.93],["都兰县",98.089,36.299],["天峻县",99.021,37.299],["海西蒙古族藏族自治州直辖",95.357,37.854]],[97.371,37.375]]]],["宁夏","宁夏回族自治区",[106.278,38.466],[["银川","银川市",[["兴庆区",106.278,38.467],["西夏区",106.132,38.492],["金凤区",106.228,38.477],["永宁县",106.254,38.28],["贺兰县",106.346,38.555],["灵武市",106.335,38.094]],[106.278,38.466]],["石嘴山","石嘴山市",[["大武口区",106.377,39.014],["惠农区",106.776,39.23],["平罗县",106.545,38.907]],[106.376,39.013]],["吴忠","吴忠市",[["利通区",106.199,37.986],["红寺堡区",106.067,37.422],["盐池县",107.405,37.784],["同心县",105.915,36.983],["青铜峡市",106.075,38.022]],[106.199,37.986]],["固原","固原市",[["原州区",106.285,36.005],["西吉县",105.732,35.965],["隆德县",106.123,35.618],["泾源县",106.339,35.493],["彭阳县",106.642,35.85]],[106.285,36.005]],["中卫","中卫市",[["沙坡头区",105.191,37.515],["中宁县",105.676,37.49],["海原县",105.647,36.562]],[105.19,37.515]]]],["新疆","新疆维吾尔自治区",[87.618,43.793],[["乌鲁木齐","乌鲁木齐市",[["天山区",87.62,43.796],["沙依巴克区",87.597,43.789],["新市区",87.561,43.871],["水磨沟区",87.613,43.817],["头屯河区",87.426,43.876],["达坂城区",88.31,43.362],["米东区",87.692,43.961],["乌鲁木齐县",87.506,43.983]],[87.618,43.793]],["克拉玛依","克拉玛依市",[["独山子区",84.882,44.327],["克拉玛依区",84.869,45.6],["白碱滩区",85.13,45.689],["乌尔禾区",85.698,46.088]],[84.874,45.596]],["吐鲁番","吐鲁番市",[["高昌区",89.182,42.948],["鄯善县",90.213,42.866],["托克逊县",88.656,42.794]],[89.184,42.948]],["哈密","哈密市",[["伊州区",93.509,42.834],["巴里坤哈萨克自治县",93.022,43.599],["伊吾县",94.693,43.252]],[93.513,42.833]],["昌吉回族自治州","昌吉回族自治州",[["昌吉市",87.304,44.013],["阜康市",87.984,44.152],["呼图壁县",86.889,44.189],["玛纳斯县",86.218,44.306],["奇台县",89.591,44.022],["吉木萨尔县",89.181,43.997],["木垒哈萨克自治县",90.283,43.832]],[87.304,44.015]],["博尔塔拉蒙古自治州","博尔塔拉蒙古自治州",[["博乐市",82.072,44.903],["阿拉山口市",82.569,45.168],["精河县",82.893,44.606],["温泉县",81.031,44.974]],[82.075,44.903]],["巴音郭楞蒙古自治州","巴音郭楞蒙古自治州",[["库尔勒市",86.146,41.763],["轮台县",84.249,41.781],["尉犁县",86.263,41.337],["若羌县",88.169,39.024],["且末县",85.533,38.139],["焉耆回族自治县",86.57,42.064],["和静县",86.391,42.317],["和硕县",86.865,42.269],["博湖县",86.632,41.98]],[86.151,41.769]],["阿克苏地区","阿克苏地区",[["阿克苏市",80.263,41.171],["温宿县",80.243,41.273],["库车县",82.963,41.717],["沙雅县",82.781,41.226],["新和县",82.611,41.551],["拜城县",81.87,41.796],["乌什县",79.231,41.216],["阿瓦提县",80.378,40.638],["柯坪县",79.048,40.506]],[80.265,41.171]],["克孜勒苏柯尔克孜自治州","克孜勒苏柯尔克孜自治州",[["阿图什市",76.174,39.713],["阿克陶县",75.945,39.147],["阿合奇县",78.45,40.938],["乌恰县",75.26,39.717]],[76.173,39.713]],["喀什地区","喀什地区",[["喀什市",75.988,39.468],["疏附县",75.863,39.378],["疏勒县",76.054,39.399],["英吉沙县",76.174,38.93],["泽普县",77.274,38.191],["莎车县",77.249,38.414],["叶城县",77.42,37.885],["麦盖提县",77.652,38.903],["岳普湖县",76.772,39.235],["伽师县",76.742,39.494],["巴楚县",78.55,39.783],["塔什库尔干塔吉克自治县",75.228,37.775]],[75.989,39.468]],["和田地区","和田地区",[["和田市",79.928,37.109],["和田县",79.819,37.12],["墨玉县",79.737,37.272],["皮山县",78.282,37.616],["洛浦县",80.184,37.074],["策勒县",80.804,37.002],["于田县",81.668,36.855],["民丰县",82.692,37.065]],[79.925,37.111]],["伊犁哈萨克自治州","伊犁哈萨克自治州",[["伊宁市",81.316,43.922],["奎屯市",84.902,44.423],["霍尔果斯市",80.421,44.202],["伊宁县",81.525,43.978],["察布查尔锡伯自治县",81.151,43.839],["霍城县",80.873,44.05],["巩留县",82.227,43.482],["新源县",83.258,43.434],["昭苏县",81.126,43.158],["特克斯县",81.84,43.215],["尼勒克县",82.504,43.79]],[81.318,43.922]],["塔城地区","塔城地区",[["塔城市",82.984,46.746],["乌苏市",84.678,44.43],["额敏县",83.622,46.523],["沙湾县",85.623,44.33],["托里县",83.605,45.936],["裕民县",82.982,46.203],["和布克赛尔蒙古自治县",85.734,46.793]],[82.986,46.746]],["阿勒泰地区","阿勒泰地区",[["阿勒泰市",88.139,47.849],["布尔津县",86.862,47.705],["富蕴县",89.525,46.993],["福海县",87.495,47.113],["哈巴河县",86.419,48.059],["青河县",90.382,46.672],["吉木乃县",85.876,47.435]],[88.14,47.848]],["石河子","石河子市",[],[86.041,44.306]],["阿拉尔","阿拉尔市",[],[81.286,40.542]],["图木舒克","图木舒克市",[],[79.078,39.867]],["五家渠","五家渠市",[],[87.527,44.167]],["北屯","北屯市",[],[87.825,47.353]],["铁门关","铁门关市",[],[85.501,41.827]],["双河","双河市",[],[82.354,44.841]],["可克达拉","可克达拉市",[],[80.636,43.683]],["昆玉","昆玉市",[],[79.287,37.208]]]],["台湾","台湾省",[121.509,25.044],[["台湾省","台湾省",[],[121.509062,25.044332]]]],["香港","香港特别行政区",[114.173,22.32],[["香港特别行政区","香港特别行政区",[["中西区",114.154,22.282],["湾仔区",114.183,22.276],["东区",114.226,22.28],["南区",114.16,22.246],["油尖旺区",114.173,22.312],["深水埗区",114.163,22.334],["九龙城区",114.193,22.312],["黄大仙区",114.204,22.336],["观塘区",114.214,22.321],["荃湾区",114.121,22.368],["屯门区",113.976,22.394],["元朗区",114.033,22.441],["北区",114.147,22.496],["大埔区",114.172,22.446],["西贡区",114.265,22.314],["沙田区",114.195,22.38],["葵青区",114.139,22.364],["离岛区",113.946,22.286]],[114.173355,22.320048]]]],["澳门","澳门特别行政区",[113.549,22.199],[["澳门特别行政区","澳门特别行政区",[["花地玛堂区",113.553,22.208],["花王堂区",113.549,22.199],["望德堂区",113.55,22.194],["大堂区",113.554,22.188],["风顺堂区",113.542,22.188],["嘉模堂区",113.559,22.154],["路凼填海区",113.569,22.137],["圣方济各堂区",113.56,22.124]],[113.54909,22.198951]]]]];

var A = { y: 2000, m: 1, d: 1, hh: 12, mi: 0, pi: 0, ci: 0, di: 0 };
var ANO = false;

function pad2(n){ return (n < 10 ? "0" : "") + n; }
function saveAstro(){
  try{
    localStorage.setItem("ppt_astro", JSON.stringify({
      y: A.y, m: A.m, d: A.d, hh: A.hh, mm: A.mi,
      pi: A.pi, ci: A.ci, di: A.di, time_known: !ANO
    }));
  }catch(e){}
}
function setTxt(id, txt, isPh){
  var el = document.getElementById(id);
  if (!el) return;
  el.textContent = txt;
  el.className = isPh ? "ph" : "";
}
function updDateTxt(){
  if (!A.y){ setTxt("aDateTxt", "点这里选年月日", true); return; }
  setTxt("aDateTxt", A.y + " 年 " + A.m + " 月 " + A.d + " 日", false);
}
function updTimeTxt(){
  var b = document.getElementById("aTimeBtn");
  if (ANO){
    setTxt("aTimeTxt", "不记得 · 按 12:00 算", false);
    b.className = "aPick off";
    return;
  }
  b.className = "aPick";
  if (A.hh === null || A.hh === undefined){ setTxt("aTimeTxt", "点这里选时分", true); return; }
  setTxt("aTimeTxt", pad2(A.hh) + " : " + pad2(A.mi), false);
}
function updCityTxt(){
  var p = PCD[A.pi] || PCD[0];
  var c = p[3][A.ci] || p[3][0];
  var ds = c[2];
  var s = p[0] + " · " + c[0];
  if (ds.length && A.di < ds.length) s += " · " + ds[A.di][0];
  setTxt("aCityTxt", s, false);
}

/* ==================== 滚轮选择器 ==================== */
var PKH = 44;
var PK = { cols: [], onCol: null, onOk: null, ready: false };

function pkVals(){
  var a = [];
  for (var i = 0; i < PK.cols.length; i++){
    var c = PK.cols[i];
    a.push(c._idx >= 0 ? c._idx : 0);
  }
  return a;
}
function pkMark(col, i){
  var kids = col.children;
  for (var k = 0; k < kids.length; k++) kids[k].className = "pkItem" + (k === i ? " on" : "");
}
function pkAlign(col, i, smooth){
  var max = col.children.length - 1;
  if (i < 0) i = 0;
  if (i > max) i = max;
  col._lock = true;
  if (smooth && col.scrollTo) col.scrollTo({ top: i * PKH, behavior: "smooth" });
  else col.scrollTop = i * PKH;
  pkMark(col, i);
  col._idx = i;
  var unlock = function(){ col._lock = false; };
  if (smooth) setTimeout(unlock, 340); else setTimeout(unlock, 40);
}
function pkSettle(col){
  var n = col.children.length;
  var i = Math.round(col.scrollTop / PKH);
  if (i < 0) i = 0;
  if (i > n - 1) i = n - 1;
  var changed = (col._idx !== i);
  pkAlign(col, i, true);
  if (changed && PK.onCol) PK.onCol(PK.cols.indexOf(col));
}
function pkColEl(items, sel){
  var col = document.createElement("div");
  col.className = "pkCol";
  var html = "";
  for (var i = 0; i < items.length; i++) html += '<div class="pkItem">' + items[i] + "</div>";
  col.innerHTML = html;
  col._idx = 0;
  col._lock = false;
  col.addEventListener("scroll", function(){
    if (col._lock) return;
    if (col._t) clearTimeout(col._t);
    col._t = setTimeout(function(){ pkSettle(col); }, 170);
  }, { passive: true });
  col.addEventListener("click", function(e){
    var it = e.target.closest ? e.target.closest(".pkItem") : null;
    if (!it) return;
    var i = Array.prototype.indexOf.call(col.children, it);
    if (i < 0) return;
    var changed = (col._idx !== i);
    pkAlign(col, i, true);
    if (changed && PK.onCol) PK.onCol(PK.cols.indexOf(col));
  });
  col.addEventListener("pointerdown", function(e){
    if (e.pointerType && e.pointerType !== "mouse") return;
    if (e.button) return;
    var sy = e.clientY, top = col.scrollTop, moved = false;
    col.style.scrollSnapType = "none";
    function mv(ev){
      var dy = ev.clientY - sy;
      if (!moved && Math.abs(dy) > 3) moved = true;
      if (moved){
        col._lock = true;
        col.scrollTop = top - dy;
        if (ev.cancelable) ev.preventDefault();
      }
    }
    function up(){
      window.removeEventListener("pointermove", mv);
      window.removeEventListener("pointerup", up);
      col.style.scrollSnapType = "";
      col._lock = false;
      pkSettle(col);
    }
    window.addEventListener("pointermove", mv, { passive: false });
    window.addEventListener("pointerup", up);
  });
  col._sel = sel || 0;
  return col;
}
function pkOpen(o){
  var wrap = document.getElementById("pkWrap");
  var olds = wrap.querySelectorAll(".pkCol");
  for (var i = 0; i < olds.length; i++) wrap.removeChild(olds[i]);
  PK = { cols: [], onCol: o.onCol || null, onOk: o.onOk || null, ready: false };
  document.getElementById("pkTitle").textContent = o.title || "";
  for (var j = 0; j < o.cols.length; j++){
    var c = pkColEl(o.cols[j].items, o.cols[j].sel);
    PK.cols.push(c);
    wrap.appendChild(c);
  }
  document.getElementById("pkMask").classList.add("show");
  var sels = o.cols.map(function(x){ return x.sel || 0; });
  requestAnimationFrame(function(){
    for (var k = 0; k < PK.cols.length; k++) pkAlign(PK.cols[k], sels[k], false);
    PK.ready = true;
  });
}
function pkSetItems(i, items, sel){
  var wrap = document.getElementById("pkWrap");
  var old = PK.cols[i];
  if (!old) return;
  var col = pkColEl(items, sel);
  wrap.replaceChild(col, old);
  PK.cols[i] = col;
  requestAnimationFrame(function(){ pkAlign(col, sel || 0, false); });
}
function pkClose(){
  document.getElementById("pkMask").classList.remove("show");
}
document.getElementById("pkCancel").onclick = function(){ pkClose(); };
document.getElementById("pkOk").onclick = function(){
  var v = pkVals(), ok = PK.onOk;
  pkClose();
  if (ok) ok(v);
};
document.getElementById("pkMask").addEventListener("click", function(e){
  if (e.target === this) pkClose();
});

/* ==================== 三个选择器 ==================== */
var YEARS = [];
for (var _yy = 1930; _yy <= 2026; _yy++) YEARS.push(_yy + " 年");
var MONTHS = [];
for (var _mm = 1; _mm <= 12; _mm++) MONTHS.push(_mm + " 月");
var HOURS = [], MINS = [];
for (var _h = 0; _h < 24; _h++) HOURS.push(pad2(_h) + " 时");
for (var _mi = 0; _mi < 60; _mi++) MINS.push(pad2(_mi) + " 分");
function daysIn(y, m){ return new Date(y, m, 0).getDate(); }
function mkDays(y, m){
  var n = daysIn(y, m), a = [];
  for (var i = 1; i <= n; i++) a.push(i + " 日");
  return a;
}
function openDatePk(){
  var y = A.y || 2000, m = A.m || 1, d = A.d || 1;
  pkOpen({
    title: "出生日期",
    cols: [
      { items: YEARS, sel: y - 1930 },
      { items: MONTHS, sel: m - 1 },
      { items: mkDays(y, m), sel: d - 1 }
    ],
    onCol: function(i){
      if (i !== 0 && i !== 1) return;
      var v = pkVals();
      var dd = mkDays(1930 + v[0], v[1] + 1);
      pkSetItems(2, dd, Math.min(v[2], dd.length - 1));
    },
    onOk: function(v){
      A.y = 1930 + v[0];
      A.m = v[1] + 1;
      A.d = Math.min(v[2] + 1, daysIn(A.y, A.m));
      updDateTxt();
    }
  });
}
function openTimePk(){
  if (ANO) return;
  pkOpen({
    title: "出生时间",
    cols: [
      { items: HOURS, sel: (A.hh === null || A.hh === undefined) ? 12 : A.hh },
      { items: MINS, sel: A.mi || 0 }
    ],
    onOk: function(v){
      A.hh = v[0];
      A.mi = v[1];
      updTimeTxt();
    }
  });
}
function openCityPk(){
  function cities(pi){ return PCD[pi][3]; }
  function cityItems(pi){
    return cities(pi).map(function(x){ return x[0]; });
  }
  function distItems(pi, ci){
    var ds = cities(pi)[ci][2];
    if (!ds.length) return ["（不用选）"];
    return ds.map(function(x){ return x[0]; });
  }
  var pi = A.pi || 0, ci = A.ci || 0, di = A.di || 0;
  pkOpen({
    title: "出生城市",
    cols: [
      { items: PCD.map(function(x){ return x[0]; }), sel: pi },
      { items: cityItems(pi), sel: ci },
      { items: distItems(pi, ci), sel: di }
    ],
    onCol: function(i){
      var v = pkVals();
      if (i === 0){
        pkSetItems(1, cityItems(v[0]), 0);
        pkSetItems(2, distItems(v[0], 0), 0);
      } else if (i === 1){
        pkSetItems(2, distItems(v[0], v[1]), 0);
      }
    },
    onOk: function(v){
      A.pi = v[0]; A.ci = v[1]; A.di = v[2];
      updCityTxt();
    }
  });
}
function cityCoord(){
  var p = PCD[A.pi] || PCD[0];
  var c = p[3][A.ci] || p[3][0];
  var ds = c[2];
  if (ds.length && A.di < ds.length){
    var d = ds[A.di];
    return { name: c[1], lat: d[2], lon: d[1] };
  }
  return { name: c[1], lat: c[3][1], lon: c[3][0] };
}
function findCity(name){
  var raw = String(name || "");
  var s = raw.replace(/\s+/g, "");
  if (!s) return null;
  var i, j, k, cs, ds;
  for (i = 0; i < PCD.length; i++){
    cs = PCD[i][3];
    for (j = 0; j < cs.length; j++){
      if (cs[j][0] === s || cs[j][1] === s) return { pi: i, ci: j, di: 0 };
    }
  }
  /* 兼容「上海市 黄浦区」这类带区名的写法 */
  var parts = raw.split(/\s+/).filter(function(x){ return !!x; });
  var cityKey = parts.length > 1 ? parts[0] : "";
  var distKey = parts.length > 1 ? parts.slice(1).join("") : s;
  for (i = 0; i < PCD.length; i++){
    cs = PCD[i][3];
    for (j = 0; j < cs.length; j++){
      var cHit = cityKey && (cs[j][0] === cityKey || cs[j][1] === cityKey
        || cs[j][0].indexOf(cityKey) === 0 || cityKey.indexOf(cs[j][0]) === 0);
      if (cityKey && !cHit) continue;
      ds = cs[j][2] || [];
      for (k = 0; k < ds.length; k++){
        if (ds[k][0] === distKey) return { pi: i, ci: j, di: k };
      }
      if (cHit) return { pi: i, ci: j, di: 0 };
    }
  }
  if (distKey){
    for (i = 0; i < PCD.length; i++){
      cs = PCD[i][3];
      for (j = 0; j < cs.length; j++){
        ds = cs[j][2] || [];
        for (k = 0; k < ds.length; k++){
          if (ds[k][0] === distKey) return { pi: i, ci: j, di: k };
        }
      }
    }
  }
  return null;
}

/* ==================== 初始化 ==================== */
(function initAstro(){
  var saved = null;
  try{ saved = JSON.parse(localStorage.getItem("ppt_astro") || "null"); }catch(e){ saved = null; }
  if (saved){
    if (saved.y){ A.y = saved.y; A.m = saved.m; A.d = saved.d; }
    if (typeof saved.hh === "number"){ A.hh = saved.hh; A.mi = saved.mm || 0; }
    if (typeof saved.pi === "number"){
      A.pi = saved.pi || 0; A.ci = saved.ci || 0; A.di = saved.di || 0;
    } else if (saved.city){
      var hit = findCity(saved.city);
      if (hit){ A.pi = hit.pi; A.ci = hit.ci; A.di = hit.di; }
    }
  }
  ANO = false;
  document.getElementById("aNoTime").checked = false;
  updDateTxt();
  updTimeTxt();
  updCityTxt();

  document.getElementById("aDateBtn").addEventListener("click", openDatePk);
  document.getElementById("aTimeBtn").addEventListener("click", openTimePk);
  document.getElementById("aCityBtn").addEventListener("click", openCityPk);
  document.getElementById("aNoTime").addEventListener("change", function(){
    ANO = this.checked;
    updTimeTxt();
  });
  document.getElementById("btnArchAdd").addEventListener("click", function(){ showForm(true); });
  document.getElementById("aFormCancel").addEventListener("click", function(){ hideForm(); });
  document.getElementById("btnAstroGo").addEventListener("click", submitChart);
})();

/* ==================== 星盘档案 ==================== */
/* ===== 匿名行为埋点（只写进你自己的后台统计，不对外展示） ===== */
function pvId(){
  var k = "ppt_vid", v = "";
  try { v = localStorage.getItem(k) || ""; } catch(e){}
  if (!v){
    v = "v" + Date.now().toString(36) + Math.random().toString(36).slice(2, 10);
    try { localStorage.setItem(k, v); } catch(e){}
  }
  return v;
}
function trackEvent(etype, opt){
  opt = opt || {};
  var body = JSON.stringify({
    vid: pvId(),
    etype: etype,
    cat: opt.cat || "",
    q: opt.q || "",
    result: opt.result || "",
    detail: opt.detail ? JSON.stringify(opt.detail) : ""
  });
  try {
    if (navigator.sendBeacon){
      navigator.sendBeacon("/api/track", new Blob([body], { type: "application/json" }));
      return;
    }
  } catch(e){}
  try {
    fetch("/api/track", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body,
      keepalive: true
    }).catch(function(){});
  } catch(e){}
}
try { trackEvent("visit"); } catch(e){}

function postJSON(url, body){
  return fetch(url, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body), cache: "no-store"
  }).then(function(r){ return r.json(); });
}
function esc(s){
  return String(s == null ? "" : s).replace(/[&<>"]/g, function(c){
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
  });
}
function archUid(){
  var k = "ppt_uid", v = "";
  try { v = localStorage.getItem(k) || ""; } catch(e){}
  if (!v){
    v = "u" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
    try { localStorage.setItem(k, v); } catch(e){}
  }
  return v;
}
/* 星盘页内部子层：list=档案列表 form=新增档案 result=星盘结果，进入前记录来路，供返回逐层退 */
var AP_PANE = "";
var AP_SUB = [];
function apPaneSet(n){
  if (AP_PANE === n) return;
  if (AP_PANE) AP_SUB.push(AP_PANE);   /* 刚进视图时基态为空，不记历史，返回直接退出本页 */
  /* 表单只是过程页：提交后进结果页，返回应回档案列表，不停在表单上 */
  AP_SUB = AP_SUB.filter(function(x){ return x !== "form"; });
  if (AP_SUB.length > 12) AP_SUB.shift();
  AP_PANE = n;
}
function apShowPane(n){
  AP_PANE = n;
  var f = document.getElementById("aForm"), r = document.getElementById("aResult"), w = document.getElementById("aArchWrap");
  if (f) f.style.display = (n === "form") ? "flex" : "none";
  if (r) r.style.display = (n === "result") ? "flex" : "none";
  if (w) w.style.display = (n === "list") ? "flex" : "none";
  window.scrollTo(0, 0);
}
function showForm(bjDefault){
  if (bjDefault){
    A.pi = 0; A.ci = 0; A.di = 0;
    try { updCityTxt(); } catch(e){}
  }
  document.getElementById("aArchWrap").style.display = "none";
  document.getElementById("aResult").style.display = "none";
  document.getElementById("aErr").textContent = "";
  document.getElementById("aName").value = "";
  document.getElementById("aForm").style.display = "flex";
  apPaneSet("form");
  window.scrollTo(0, 0);
}
function hideForm(){
  document.getElementById("aForm").style.display = "none";
  document.getElementById("aResult").style.display = "none";
  document.getElementById("aArchWrap").style.display = "flex";
  /* 取消表单等于退回上一层：把刚才进表单时记的那一层出栈，避免返回按钮空转一次 */
  if (AP_PANE === "form" && AP_SUB.length) AP_SUB.pop();
  AP_PANE = "list";
  AP_SUB = AP_SUB.filter(function(x){ return x !== "form"; });
  window.scrollTo(0, 0);
}
function showArchList(){
  document.getElementById("aForm").style.display = "none";
  document.getElementById("aResult").style.display = "none";
  document.getElementById("aArchWrap").style.display = "flex";
  apPaneSet("list");
}
/* 点星盘入口：有档案直接出牌面，没有才拉表单 */
function smartAstro(){
  showView("astro");
  AP_PANE = "list";   /* 进入星盘页：内部层级清零 */
  AP_SUB.length = 0;
  var wrap = document.getElementById("aArchWrap");
  document.getElementById("aForm").style.display = "none";
  document.getElementById("aResult").style.display = "none";
  wrap.style.display = "flex";
  var box = document.getElementById("aArchList");
  if (box) box.innerHTML = '<div class="aEmpty">读取中…</div>';
  loadArch(function(items){
    if (!items.length){ showForm(); return; }
    var last = 0;
    try { last = parseInt(localStorage.getItem("ppt_last_arch") || "0", 10) || 0; } catch(e){}
    var pick = items[0];
    for (var i = 0; i < items.length; i++){ if (String(items[i].id) === String(last)) pick = items[i]; }
    wrap.style.display = "none";
    viewArch(pick.id);
    AP_SUB.length = 0;   /* 直接出结果时列表只是过渡，返回应直接退出星盘页 */
  });
}
function loadArch(cb){
  var box = document.getElementById("aArchList");
  if (!box) return;
  box.innerHTML = '<div class="aEmpty">读取中…</div>';
  postJSON("/api/chart_list", { uid: archUid() }).then(function(d){
    var items = (d && d.ok && d.items) ? d.items : [];
    if (cb) cb(items);
    if (!d || !d.ok || !d.items || !d.items.length){
      box.innerHTML = '<div class="aEmpty">还没有存过的出生时间<br>点下面按钮添一条</div>';
      return;
    }
    box.innerHTML = d.items.map(function(it){
      return '<div class="archItem" data-id="' + it.id + '">'
        + '<div class="ail"><b>' + esc(it.name || "未命名") + '</b>'
        + '<span>' + esc(it.birth) + (it.region ? ' · ' + esc(it.region) : '') + '</span></div>'
        + '<em class="aigo">' + esc(it.sun || "") + (it.moon ? '/' + esc(it.moon) : '') + '</em>'
        + '<button class="archDel" data-id="' + it.id + '">删</button>'
        + '</div>';
    }).join("");
    Array.prototype.forEach.call(box.querySelectorAll(".archItem"), function(el){
      el.addEventListener("click", function(){ viewArch(el.getAttribute("data-id")); });
    });
    Array.prototype.forEach.call(box.querySelectorAll(".archDel"), function(el){
      el.addEventListener("click", function(ev){
        ev.stopPropagation();
        if (el.getAttribute("data-arm") !== "1"){
          el.setAttribute("data-arm", "1");
          el.textContent = "确认?";
          el.style.color = "#e08a8a";
          setTimeout(function(){
            el.removeAttribute("data-arm");
            el.textContent = "删";
            el.style.color = "";
          }, 2600);
          return;
        }
        var id = el.getAttribute("data-id");
        postJSON("/api/chart_del", { uid: archUid(), id: id }).then(function(d){
          if (d && d.ok){ loadArch(); }
        }).catch(function(){});
      });
    });
  }).catch(function(){
    box.innerHTML = '<div class="aEmpty">读取失败，刷新一下再试</div>';
  });
}
/* ==================== 今日运势（直接取已存档案） ==================== */
var FT = { off: 0, busy: false, data: null, id: 0, pick: false, switched: false };
var ARCH_FROM_FT = false;
/* 只取星座名，去掉后面的度数 */
function ftSignOnly(s){
  var t = String(s || "").replace(/[\d°'\u2032\u2019"\s]+/g, "");
  if (t.length <= 1){
    for (var i = 0; i < FT_ZS.length; i++){ if (FT_ZS[i].charAt(0) === t){ t = FT_ZS[i]; break; } }
  }
  return t.replace("座", "");
}
/* 从换档案列表退回今日运势正文，不重新请求 */
function ftPickBack(){
  FT.pick = false;
  FT.switched = false;
  if (FT.data) ftRender(FT.data); else ftLoad(FT.off);
}
function openFortune(){
  showView("fortune");
  if (!FT.data || FT.off !== 0) ftLoad(0);
}
function ftShift(dz){
  var off = FT.off + dz;
  if (off > 7) off = 7;
  if (off < -7) off = -7;
  if (off === FT.off) return;
  ftLoad(off);
}
function ftStars(n){
  var pct = Math.max(0, Math.min(100, (n / 5) * 100));
  return '<div class="fStarBox"><span class="fStarBg">★★★★★</span>'
    + '<span class="fStarFg" style="width:' + pct.toFixed(1) + '%">★★★★★</span></div>';
}
function ftLoad(off){
  if (FT.busy) return;
  FT.busy = true;
  FT.off = off;
  var body = document.getElementById("fBody");
  if (body) body.innerHTML = '<div class="aEmpty">正在算今天的运势…</div>';
  postJSON("/api/fortune", { uid: archUid(), id: FT.id || 0, offset: off }).then(function(d){
    FT.busy = false;
    if (!d || !d.ok){
      if (d && d.no_arch){ ftNoArch(); return; }
      body.innerHTML = '<div class="fEmptyCard"><b>这次没算出来</b><span>'
        + esc((d && d.error) || "再点一下试试") + '</span></div>';
      return;
    }
    FT.data = d;
    FT.id = (d.arch && d.arch.id) || 0;
    ftRender(d);
  }).catch(function(){
    FT.busy = false;
    body.innerHTML = '<div class="fEmptyCard"><b>网络没通</b><span>刷新一下再点进来</span></div>';
  });
}
function ftNoArch(){
  var body = document.getElementById("fBody");
  body.innerHTML = '<div class="fEmptyCard"><b>还没有生日档案</b>'
    + '<span>今日运势要按你的出生时间算。先存一条，以后点进来就直接出结果，不用每次再填。</span>'
    + '<button class="aAgain" id="ftAdd">去添一条出生时间</button></div>';
  var b = document.getElementById("ftAdd");
  if (b) b.addEventListener("click", function(){ showView("astro"); showForm(); });
}
function ftPick(){
  var body = document.getElementById("fBody");
  body.innerHTML = '<div class="aEmpty">读取档案…</div>';
  postJSON("/api/chart_list", { uid: archUid() }).then(function(d){
    var items = (d && d.items) || [];
    if (!items.length){ ftNoArch(); return; }
    FT.pick = true;
    FT.switched = false;
    var h = '<div class="fWho"><b>换一份档案</b></div><div class="fCard">';
    for (var i = 0; i < items.length; i++){
      var it = items[i];
      h += '<div class="archItem" data-id="' + it.id + '"><div class="ail"><b>'
        + esc(it.name || "未命名") + '</b><span>' + esc(it.birth)
        + (it.region ? ' · ' + esc(it.region) : '') + '</span></div>'
        + '<em class="aigo">' + esc(ftSignOnly(it.sun)) + '</em></div>';
    }
    h += '</div><button class="fCrys" id="ftAddNew">新增档案 ›</button>';
    body.innerHTML = h;
    Array.prototype.forEach.call(body.querySelectorAll(".archItem"), function(el){
      el.addEventListener("click", function(){
        FT.id = parseInt(el.getAttribute("data-id"), 10) || 0;
        FT.switched = true;
        ftLoad(FT.off);
      });
    });
    var nb = document.getElementById("ftAddNew");
    if (nb) nb.addEventListener("click", function(){
      FT.pick = false;
      ARCH_FROM_FT = true;
      showView("astro");
      showForm(true);
    });
  }).catch(function(){
    body.innerHTML = '<div class="fEmptyCard"><b>档案读不到</b><span>刷新一下再试</span></div>';
  });
}
var FT_ZS = ["白羊","金牛","双子","巨蟹","狮子","处女","天秤","天蝎","射手","摩羯","水瓶","双鱼"];
var FT_ZG = ["\u2648","\u2649","\u264A","\u264B","\u264C","\u264D","\u264E","\u264F","\u2650","\u2651","\u2652","\u2653"];
function ftZodiacBar(sign){
  var cur = FT_ZS.indexOf(String(sign || "").replace("座", ""));
  var out = '<div class="zBar">';
  for (var i = 0; i < FT_ZS.length; i++){
    out += '<span class="zI' + (i === cur ? " cur" : "") + '" data-z="' + FT_ZS[i] + '"><i>' + FT_ZG[i] + '</i></span>';
  }
  out += '</div>';
  return out;
}
function ftRender(d){
  var a = d.arch || {};
  var offTxt = d.offset === 0 ? "今天" : (d.offset > 0 ? d.offset + " 天后" : (-d.offset) + " 天前");
  var prevDis = d.offset <= -7 ? " disabled" : "";
  var nextDis = d.offset >= 7 ? " disabled" : "";

  var h = '<div class="fWhoRow"><div class="fWho"><b>' + esc(a.name || "我自己") + ' · ' + esc(d.sun_sign) + '座</b>'
    + ftZodiacBar(d.sun_sign) + '</div>'
    + '<button class="fSw" id="ftSw">换档案 ›</button></div>';

  h += '<div class="fNav"><button class="fArr" id="ftPrev"' + prevDis + '>‹</button>'
    + '<div class="fNavMid"><b>' + esc(d.dateLabel) + '</b>'
    + '<em class="' + (d.offset === 0 ? "now" : "") + '">' + esc(offTxt) + '</em></div>'
    + '<button class="fArr" id="ftNext"' + nextDis + '>›</button></div>';

  h += '<div class="fHeroCard"><div class="fHeroTop">'
    + '<div class="fScoreW"><div class="fScore">' + d.score + '</div>'
    + '<div class="fSl">今日运气</div>' + ftStars(d.stars) + '</div>'
    + '<div class="fDims">';
  for (var i = 0; i < d.dims.length; i++){
    var x = d.dims[i];
    var cls = x.v >= 82 ? "hi" : (x.v >= 66 ? "mid" : "low");
    h += '<div class="fDim ' + cls + '"><span class="fDimN">' + esc(x.n) + '</span>'
      + '<span class="fDimBar"><i style="width:' + x.v + '%"></i></span>'
      + '<span class="fDimV">' + x.v + '</span></div>';
  }
  h += '</div></div>'
    + '<div class="fHeroBot"><div class="fTag lv' + d.tag_level + '">' + esc(d.tag) + '</div>'
    + '<p class="fHeadline">' + esc(d.headline) + '</p></div></div>';

  h += '<div class="fLucky">'
    + '<div class="fLk"><em>幸运颜色</em>'
    + '<span class="fDot" style="background:' + esc(d.lucky.color.hex) + '"></span>'
    + '<b>' + esc(d.lucky.color.n) + '</b></div>'
    + '<div class="fLk"><em>幸运数字</em><b>' + esc(d.lucky.number) + '</b></div>'
    + '<div class="fLk"><em>幸运方向</em><b>' + esc(d.lucky.dir) + '</b></div></div>';

  h += '<div class="fCard"><div class="fCardT"><b>综合运势</b><span>'
    + esc(d.moon_sign) + '座月亮 · ' + esc(d.moon_phase) + '</span></div>'
    + '<p class="fP">' + esc(d.overall) + '</p></div>';

  h += '<div class="fCard"><div class="fCardT"><b>分项解读</b><span>按今天的行运说</span></div>';
  for (var j = 0; j < d.sections.length; j++){
    var sec = d.sections[j];
    h += '<div class="fSecBlock"><b>' + esc(sec.t) + '</b>';
    for (var k = 0; k < sec.lines.length; k++){
      h += '<p class="fP">' + esc(sec.lines[k]) + '</p>';
    }
    h += '</div>';
  }
  h += '</div>';

  h += '<div class="fWarn"><b>今天记住一句</b><p>' + esc(d.caution) + '</p></div>';

  h += '<button class="fCrys" id="ftCrys">查看推荐水晶 ›</button>'
    + '<div class="fCrysBody" id="ftCrysBody" style="display:none">'
    + '<b>' + esc(d.crystal.n) + '</b> · ' + esc(d.crystal.use) + '</div>';

  
  var body = document.getElementById("fBody");
  body.innerHTML = h;
  var pv = document.getElementById("ftPrev"), nx = document.getElementById("ftNext");
  if (pv) pv.addEventListener("click", function(){ ftShift(-1); });
  if (nx) nx.addEventListener("click", function(){ ftShift(1); });
  var sw = document.getElementById("ftSw");
  if (sw) sw.addEventListener("click", function(){ ftPick(); });
  var cb = document.getElementById("ftCrys"), cbody = document.getElementById("ftCrysBody");
  if (cb && cbody){
    cb.addEventListener("click", function(){
      var open = cbody.style.display !== "none";
      cbody.style.display = open ? "none" : "block";
      cb.textContent = open ? "查看推荐水晶 ›" : "收起推荐水晶 ‹";
    });
  }
  window.scrollTo(0, 0);
}
/* 切换档案后把出生信息同步到表单缓存，避免新增档案时预填上一个档案 */
function apSyncArch(it){
  try{
    var b = String(it.birth || "");
    var ds = (b.split(" ")[0] || "").split("-");
    var ts = (b.split(" ")[1] || "12:00").split(":");
    var y = parseInt(ds[0], 10), mo = parseInt(ds[1], 10), da = parseInt(ds[2], 10);
    var hh = parseInt(ts[0], 10), mi = parseInt(ts[1], 10);
    if (y){ A.y = y; A.m = mo || 1; A.d = da || 1; }
    if (!isNaN(hh)){ A.hh = hh; A.mi = isNaN(mi) ? 0 : mi; }
    var hit = findCity(it.region || "");
    if (hit){ A.pi = hit.pi; A.ci = hit.ci; A.di = hit.di; }
    if (typeof it.time_known !== "undefined" && it.time_known !== null) ANO = !it.time_known;
    try { localStorage.setItem("ppt_astro", JSON.stringify({
      y: A.y, m: A.m, d: A.d, hh: A.hh, mm: A.mi,
      pi: A.pi, ci: A.ci, di: A.di, time_known: !ANO
    })); } catch(e){}
    var cb = document.getElementById("aNoTime");
    if (cb) cb.checked = ANO;
    updDateTxt(); updTimeTxt(); updCityTxt();
  }catch(e){}
}

function viewArch(id){
  var box = document.getElementById("aResult");
  var meta = { id: id };
  document.getElementById("aArchWrap").style.display = "none";
  document.getElementById("aForm").style.display = "none";
  box.innerHTML = '<div class="aCard aRes"><div class="aEmpty">正在算这一盘…</div></div>';
  box.style.display = "flex";
  apPaneSet("result");
  window.scrollTo(0, 0);
  postJSON("/api/chart_get", { uid: archUid(), id: id }).then(function(d){
    if (!d || !d.ok || !d.item) throw new Error((d && d.error) || "档案读不到");
    var it = d.item;
    meta.name = it.name || "";
    meta.birth = it.birth || "";
    meta.region = it.region || "";
    apSyncArch(it);
    var ds = String(it.birth || "").split(" ")[0].split("-");
    var ts = (String(it.birth || "").split(" ")[1] || "12:00").split(":");
    return postJSON("/api/astro", {
      y: parseInt(ds[0], 10) || 2000, m: parseInt(ds[1], 10) || 1, d: parseInt(ds[2], 10) || 1,
      hh: parseInt(ts[0], 10) || 0, mm: parseInt(ts[1], 10) || 0,
      time_known: !!it.time_known, lat: it.lat, lon: it.lon, city: it.region || ""
    });
  }).then(function(r){
    if (r && r.blocks){
      try { localStorage.setItem("ppt_last_arch", String(id)); } catch(e){}
      if (!meta.name) meta.name = r.city ? r.city + " 的盘" : "我的星盘";
      renderAstro(r, meta);
      return;
    }
    box.innerHTML = '<div class="aCard aRes"><div class="aEmpty">这一盘算不出来：'
      + esc((r && r.error) || "再看看出生时间") + '</div>'
      + '<button class="aAgain" id="btnAgain2">回档案列表</button></div>';
    document.getElementById("btnAgain2").addEventListener("click", function(){ showArchList(); loadArch(); });
  }).catch(function(err){
    box.innerHTML = '<div class="aCard aRes"><div class="aEmpty">'
      + esc(err && err.message ? err.message : "读取失败") + '</div>'
      + '<button class="aAgain" id="btnAgain3">回档案列表</button></div>';
    document.getElementById("btnAgain3").addEventListener("click", function(){ showArchList(); loadArch(); });
  });
}
function submitChart(){
  var btn = document.getElementById("btnAstroGo"), err = document.getElementById("aErr");
  if (!A.y){ err.textContent = "先把出生日期选上"; return; }
  var co = cityCoord();
  var noTime = document.getElementById("aNoTime").checked;
  var hh = noTime ? 12 : A.hh;
  var mi = noTime ? 0 : A.mi;
  if (!noTime && (hh === null || hh === undefined)){ err.textContent = "出生时间选一下，或者勾上不记得"; return; }
  var nm = (document.getElementById("aName").value || "").trim();
  var body = {
    uid: archUid(),
    name: nm || ("档案 " + (A.y + "." + A.m + "." + A.d)),
    y: A.y, m: A.m, d: A.d, hh: hh, mm: mi, time_known: !noTime,
    lat: co.lat, lon: co.lon, city: co.name
  };
  err.textContent = "";
  btn.disabled = true; btn.textContent = "存一下…";
  postJSON("/api/chart_save", body).then(function(res){
    btn.disabled = false; btn.textContent = "存下来并看今天 →";
    if (!res || !res.ok){ err.textContent = (res && res.error) || "算不出来，再试一次"; return; }
    saveAstro();
    if (res.city === undefined || !res.city) res.city = co.name;
    renderAstro(res, {
      id: res.id || 0, name: body.name, region: co.name,
      birth: A.y + "-" + (A.m < 10 ? "0" : "") + A.m + "-" + (A.d < 10 ? "0" : "") + A.d
             + " " + (hh < 10 ? "0" : "") + hh + ":" + (mi < 10 ? "0" : "") + mi
    });
  }).catch(function(){
    btn.disabled = false; btn.textContent = "存下来并看今天 →";
    err.textContent = "网络出问题，再试一次";
  });
}

var SIGN_CN = ["白羊","金牛","双子","巨蟹","狮子","处女","天秤","天蝎","射手","摩羯","水瓶","双鱼"];
var ASP_COL = { "冲":"#d4695a", "刑":"#c98b3f", "拱":"#4f9787", "六分":"#5b7fb8", "合":"#9a7fc0" };
var PL_SHORT = { "太阳":"日","月亮":"月","水星":"水","金星":"金","火星":"火",
                 "木星":"木","土星":"土","天王星":"天","海王星":"海","冥王星":"冥" };

function fmtDeg(lon){
  var x = lon % 30;
  if (x < 0) x += 30;
  var d = Math.floor(x), m = Math.floor((x - d) * 60);
  if (m === 60){ m = 0; d += 1; }
  return (d < 10 ? "0" : "") + d + "\u00b0" + (m < 10 ? "0" : "") + m + "'";
}

function drawChart(c){
  if (!c || !c.planets || !c.planets.length) return "";
  var CX = 190, RO = 176, RS = 152, RHE = 152, RHE2 = 120, RHN = 110, RP = 95, RPD = 82, RI = 52;
  var asc = (typeof c.asc === "number") ? c.asc : 0;
  var hasH = (typeof c.asc === "number") && c.cusps && c.cusps.length === 12;

  function XY(lon, r){
    var th = (180 + (lon - asc)) * Math.PI / 180;
    return [CX + r * Math.cos(th), CX - r * Math.sin(th)];
  }
  function seg(lon1, r1, lon2, r2, col, w, dash){
    var p = XY(lon1, r1), q = XY(lon2, r2);
    return '<line x1="' + p[0].toFixed(1) + '" y1="' + p[1].toFixed(1) + '" x2="' + q[0].toFixed(1) + '" y2="' + q[1].toFixed(1) + '" stroke="' + col + '" stroke-width="' + w + '"' + (dash ? ' stroke-dasharray="2 2"' : '') + '/>';
  }
  function txt(lon, r, t, size, fill, weight){
    var p = XY(lon, r);
    return '<text x="' + p[0].toFixed(1) + '" y="' + (p[1] + size * 0.36).toFixed(1) + '" font-size="' + size + '" fill="' + fill + '" text-anchor="middle" font-family="inherit"' + (weight ? ' font-weight="' + weight + '"' : '') + '>' + t + '</text>';
  }

  var s = '<svg viewBox="0 0 380 380" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:320px;height:auto;display:block;flex:0 0 auto">';
  s += '<circle cx="190" cy="190" r="' + RO + '" fill="none" stroke="rgba(240,215,156,.55)" stroke-width="1"/>';
  s += '<circle cx="190" cy="190" r="' + RS + '" fill="none" stroke="rgba(240,215,156,.4)" stroke-width="1"/>';

  for (var i = 0; i < 12; i++){
    s += seg(i * 30, RS, i * 30, RO, "rgba(240,215,156,.26)", 1);
    s += txt(i * 30 + 15, (RO + RS) / 2, SIGN_CN[i], 10.5, "#cbbfd8");
  }

  if (c.aspects && c.aspects.length){
    s += '<circle cx="190" cy="190" r="' + RI + '" fill="none" stroke="rgba(240,215,156,.16)" stroke-width="1"/>';
    var pm = {};
    for (var k = 0; k < c.planets.length; k++) pm[c.planets[k].n] = c.planets[k].lon;
    for (var j = 0; j < c.aspects.length; j++){
      var as = c.aspects[j];
      if (!(as.a in pm) || !(as.b in pm)) continue;
      var w = Math.max(0.55, 1.5 - as.orb * 0.14);
      s += seg(pm[as.a], RI, pm[as.b], RI, ASP_COL[as.t] || "#888", w.toFixed(2));
    }
  }

  if (hasH){
    for (var h = 0; h < 12; h++){
      var c0 = c.cusps[h], c1 = c.cusps[(h + 1) % 12];
      var isAsc = (h === 0);
      s += seg(c0, RHE, c0, RHE2, isAsc ? "rgba(240,215,156,.85)" : "rgba(150,135,200,.45)", isAsc ? 1.6 : 0.9);
      var span = ((c1 - c0) % 360 + 360) % 360;
      s += txt(c0 + span / 2, RHN, (h + 1), 8.5, "rgba(196,184,220,.7)");
    }
    var t1 = XY(c.cusps[0] - 2.6, RO - 13), t2 = XY(c.cusps[0] + 2.6, RO - 13), t3 = XY(c.cusps[0], RO - 4);
    s += '<polygon points="' + t1[0].toFixed(1) + ',' + t1[1].toFixed(1) + ' ' + t2[0].toFixed(1) + ',' + t2[1].toFixed(1) + ' ' + t3[0].toFixed(1) + ',' + t3[1].toFixed(1) + '" fill="#f0d79c"/>';
  }

  // 行星：按黄经排序后做角度避让，只放单字标记
  var ord = c.planets.slice().sort(function(x, y){ return x.lon - y.lon; });
  var n = ord.length, need = 10.0, pos = [], i2;
  for (i2 = 0; i2 < n; i2++){
    if (i2 === 0){ pos.push(ord[0].lon); continue; }
    var prev = pos[i2 - 1];
    var gap = ((ord[i2].lon - prev) % 360 + 360) % 360;
    pos.push(gap < need ? prev + need : ord[i2].lon);
  }
  if (n > 1 && pos[n - 1] - ord[0].lon > 360 - need){
    for (i2 = 0; i2 < n; i2++) pos[i2] = ord[0].lon + i2 * (360 / n);
  }
  for (i2 = 0; i2 < n; i2++){
    var pl = ord[i2], showLon = pos[i2];
    var big = (pl.n === "月亮");
    var shifted = Math.abs(showLon - pl.lon) > 0.4;
    if (shifted) s += seg(pl.lon, RHE2, showLon, (big ? RP - 9 : RP - 6), "rgba(240,215,156,.28)", 0.6);
    var q = XY(pl.lon, RI);
    s += '<circle cx="' + q[0].toFixed(1) + '" cy="' + q[1].toFixed(1) + '" r="1.7" fill="' + (big ? "#f0d79c" : "#b9a9d8") + '"/>';
    s += txt(showLon, RP, (PL_SHORT[pl.n] || pl.n) + (pl.retro ? "R" : ""), big ? 11 : 10, big ? "#f5e0a8" : "#d6c9ea", big ? "bold" : "");
  }

  s += '</svg>';
  return '<div style="margin:2px 0 8px;display:flex;justify-content:center">' + s + '</div>';
}

var APC = { "上升": ["#8a76c8", "#332a5e"], "太阳": ["#f5c96a", "#a8672a"], "月亮": ["#cfd4ec", "#565c88"],
  "水星": ["#7fd0c0", "#2f6a68"], "金星": ["#f3a8bf", "#8d3f63"], "火星": ["#f08a6a", "#8a3524"],
  "木星": ["#c9a2e8", "#5c3d84"], "土星": ["#bcb5a6", "#4f4843"], "婚神星": ["#8fc7e8", "#2f5b78"] };
var APCHART = { data: null, uid: 0 };
var APCARD = {};

/* 文案换行转 <br>（用字符码拼，避开转义） */
function nlb(t){
  return esc(t == null ? "" : String(t)).split(String.fromCharCode(10)).join("<br>");
}

/* 点卡片：弹窗看这颗星落的宫位以及这一宫的含义 */
function apHouse(el){
  var n = (el && el.getAttribute) ? el.getAttribute("data-pl") : el;
  var c = APCARD[n];
  var m = document.getElementById("plMask");
  var t = document.getElementById("plTitle");
  var b = document.getElementById("plBody");
  if (!c || !m || !t || !b) return;
  var cc = APC[c.n] || ["#6d5aa8", "#2a2350"];
  t.textContent = c.n + " 详解";
  var h = '<div class="plHead">'
    + '<div class="plSym' + (c.n === "上升" ? " asc" : "") + '" style="--c1:' + cc[0] + ';--c2:' + cc[1] + '">'
    + (c.sym || c.n.charAt(0)) + '</div>'
    + '<div style="min-width:0">'
    + '<div class="plName">' + c.n + ' · ' + (c.sign || "—") + '座' + (c.deg ? " " + c.deg : "") + '</div>'
    + '<div class="plSub">' + (c.tag || "") + (c.retro ? ' · 逆行' : '') + '</div>'
    + '</div>'
    + (c.motto ? '<div class="plMotto">' + c.motto + '</div>' : '')
    + '</div>';
  if (c.house){
    h += '<div style="margin-top:2px"><span class="plH">第' + c.house + '宫 · ' + (c.hname || "") + '</span></div>';
  }
  /* ① 星体 × 星座 */
  h += '<div class="plSec">① ' + c.n + ' 落 ' + (c.sign || "—") + '座</div>'
    + '<div class="plP">' + nlb(c.detail || (c.tag || "")) + '</div>';
  /* ② 星体 × 宫位 */
  if (c.house){
    h += '<div class="plSec">② ' + c.n + ' 落 第' + c.house + '宫</div>'
      + '<div class="plP">' + nlb(c.htext || "") + '</div>';
  }
  /* ③ 星体 × 星座 × 宫位 */
  if (c.house && c.combo){
    h += '<div class="plSec">③ ' + c.n + ' 落 ' + (c.sign || "—") + '座 · 第' + c.house + '宫</div>'
      + '<div class="plP">' + nlb(c.combo) + '</div>';
  }
  if (!c.house){
    h += '<div class="aNo">没填出生时间，宫位算不出来，② ③ 两层先跳过，只按星座这一层看。</div>';
  }
  b.innerHTML = h;
  m.classList.add("show");
}
function apCloseHouse(){
  var m = document.getElementById("plMask");
  if (m) m.classList.remove("show");
}

function renderAstro(r, meta){
  meta = meta || {};
  var cards = r.cards || [];
  var dets = r.details || [];

  var h = '<div class="apTop"><div class="apWho"><div class="apName">'
    + esc(meta.name || "我的星盘")
    + (r.sun_sign ? '<span class="apSg">' + r.sun_sign + '座</span>' : '')
    + (meta.birth ? '<span class="apBd">' + esc(String(meta.birth).split(" ")[0]) + '</span>' : '')
    + '</div></div>'
    + '<div class="apMe" onclick="apPickArch()"><i>⇄</i>切换档案</div></div>';

  if (cards.length){
    h += '<div class="apGrid">';
    for (var i = 0; i < cards.length; i++){
      var c = cards[i], cc = APC[c.n] || ["#6d5aa8", "#2a2350"];
      APCARD[c.n] = c;
      h += '<div class="apCard" style="--c1:' + cc[0] + ';--c2:' + cc[1] + '" data-pl="' + c.n + '" onclick="apHouse(this)">'
        + (c.retro ? '<span class="apRetro">R</span>' : '')
        + '<span class="apDeg">' + (c.deg || "") + '</span>'
        + '<div class="apSym' + (c.n === "上升" ? " asc" : "") + '">' + (c.sym || c.n.charAt(0)) + '</div>'
        + '<div class="apPn">' + c.n + '</div>'
        + '<div class="apSgn">' + (c.sign || "—") + '</div>'
        + '<div class="apTag">' + (c.tag || "") + '</div>'
        + (c.house ? '<span class="apHs">' + c.house + '宫 ›</span>' : '')
        + '</div>';
    }
    h += '</div>';
  }

  h += '<button class="apChartBtn" onclick="apOpenChart()"><i>✳</i>看完整星盘图</button>';

  if (r.blocks && r.blocks.length){
    h += '<div class="aCard aRes" style="gap:10px">';
    h += '<div class="aSec"><h4>这几天的行运</h4>';
    for (var b = 0; b < r.blocks.length; b++){
      h += '<p style="color:#9c93bd;font-size:11px;letter-spacing:1px;margin:6px 0 2px">'
        + r.blocks[b].t + '</p>';
      for (var j = 0; j < r.blocks[b].lines.length; j++) h += '<p>' + r.blocks[b].lines[j] + '</p>';
    }
    h += '</div></div>';
  }

  if (!r.time_known) h += '<div class="aNo">没填出生时间，上升和宫位算不细，上面以太阳月亮为主看。</div>';

  APCHART.data = r.chart || null;
  APCHART.uid = meta.id || 0;

  var box = document.getElementById("aResult");
  box.innerHTML = h;
  box.style.display = "flex";
  document.getElementById("aForm").style.display = "none";
  document.getElementById("aArchWrap").style.display = "none";
  apPaneSet("result");
  window.scrollTo(0, 0);
}

/* 切换档案：结果页内直接换盘，不进档案管理页 */
function apPickArch(){
  var m = document.getElementById("archPick"), box = document.getElementById("apPickList");
  if (!m || !box) return;
  m.classList.add("show");
  box.innerHTML = '<div class="aEmpty">读取中…</div>';
  postJSON("/api/chart_list", { uid: archUid() }).then(function(d){
    var items = (d && d.ok && d.items) ? d.items : [];
    if (!items.length){
      box.innerHTML = '<div class="aEmpty">还没有别的档案</div>';
      return;
    }
    box.innerHTML = items.map(function(it){
      var cur = String(it.id) === String(APCHART.uid) ? " isCur" : "";
      return '<div class="archItem' + cur + '" data-id="' + it.id + '">'
        + '<div class="ail"><b>' + esc(it.name || "未命名") + '</b>'
        + '<span>' + esc(it.birth) + (it.region ? ' · ' + esc(it.region) : '') + '</span></div>'
        + '<em class="aigo">' + esc(it.sun || "") + (it.moon ? '/' + esc(it.moon) : '') + '</em>'
        + '</div>';
    }).join("");
    Array.prototype.forEach.call(box.querySelectorAll(".archItem"), function(el){
      el.addEventListener("click", function(){
        var id = el.getAttribute("data-id");
        apClosePick();
        if (String(id) !== String(APCHART.uid)) viewArch(id);
      });
    });
  }).catch(function(){
    box.innerHTML = '<div class="aEmpty">读取失败，关掉再点一次</div>';
  });
}
function apClosePick(){
  var m = document.getElementById("archPick");
  if (m) m.classList.remove("show");
}

function apOpenChart(){
  var m = document.getElementById("chartMask");
  var body = document.getElementById("chartBody");
  if (!m || !body) return;
  var c = APCHART.data;
  if (!c || !c.planets || !c.planets.length){
    body.innerHTML = '<div class="aEmpty">这一盘没有可画的度数</div>';
  } else {
    var h = '<div class="csSvg">' + drawChart(c) + '</div>';
    var pRows = "";
    for (var i = 0; i < c.planets.length; i++){
      var o = c.planets[i];
      var cc = APC[o.n] || ["#9c93bd", "#2a2350"];
      var sg = SIGN_CN[o.sign] || "";
      pRows += '<tr><td style="color:' + cc[0] + ';font-weight:600">' + o.n
        + (o.retro ? '<span class="rR">R</span>' : '') + '</td>'
        + '<td>' + sg + ' ' + fmtDeg(o.lon) + '</td>'
        + '<td style="text-align:right;color:#8e86ad">' + (o.house ? o.house + "宫" : "—") + '</td></tr>';
    }
    h += '<div class="csSec">行星落座</div>'
      + '<table class="aspTable csPos"><thead><tr><th>行星</th><th>落座</th><th style="text-align:right">宫位</th></tr></thead>'
      + '<tbody>' + pRows + '</tbody></table>';
    if (c.aspects && c.aspects.length){
      var as = c.aspects.slice().sort(function(a, b){ return a.orb - b.orb; });
      var rows = as.slice(0, 12).map(function(x){
        var col = ASP_COL[x.t] || "#9c93bd";
        return '<tr><td style="color:' + col + ';font-weight:600">' + x.t + '</td>'
          + '<td>' + (PL_SHORT[x.a] || x.a) + ' — ' + (PL_SHORT[x.b] || x.b) + '</td>'
          + '<td style="text-align:right;color:#8e86ad">' + x.orb.toFixed(1) + '\u00b0</td></tr>';
      }).join("");
      h += '<div class="csSec">主要相位</div>'
        + '<table class="aspTable"><thead><tr><th>相位</th><th>之间</th><th style="text-align:right">容许度</th></tr></thead>'
        + '<tbody>' + rows + '</tbody></table>';
    }
    body.innerHTML = h;
  }
  m.classList.add("show");
}

function apCloseChart(){
  var m = document.getElementById("chartMask");
  if (m) m.classList.remove("show");
}


/* ==================== 首页 banner ==================== */
/* 蝴蝶扇翅层定位：套用与 img object-fit:cover 相同的几何，保证左右半翅像素级贴合 */
function fitBnrShape(){
  var box = document.getElementById("bnrLink"), img = document.getElementById("bnrImg");
  if (!box || !img || !img.naturalWidth || !img.naturalHeight) return;
  var r = img.naturalWidth / img.naturalHeight;
  if (!r || !isFinite(r)) return;
  if (window.innerWidth >= 720){        /* PC：走 CSS 的固定高度 + 全宽，比例交给 contain */
    box.style.aspectRatio = ""; box.style.maxWidth = "";
  } else {                              /* 手机：容器比例贴合原图，正好填满 */
    box.style.aspectRatio = String(r); box.style.maxWidth = "";
  }
}
function fitBnrFly(){
  var box = document.getElementById("bnrLink");
  var lay = document.getElementById("bnrFly");
  if (!box || !lay) return;
  var W = box.clientWidth, Hc = box.clientHeight;
  if (!W || !Hc){                       /* 布局还没算出来，下一帧重试 */
    if ((window.__bnrRetry = (window.__bnrRetry || 0) + 1) < 40) requestAnimationFrame(fitBnrFly);
    return;
  }
  fitBnrShape();
  W = box.clientWidth; Hc = box.clientHeight;
  if (!W || !Hc) return;
  var IW = 1080, IH = 360;
  /* 前景图用 object-fit:contain，这里套同一几何（取 min），半翅才能像素级贴合 */
  var s = Math.min(W / IW, Hc / IH);
  var ox = (W - IW * s) / 2, oy = (Hc - IH * s) / 2;
  var BX = 633, BY = 28.67, BW = 403, BH = 316.67, MID = BX + BW / 2;
  var lx = ox + BX * s, ly = oy + BY * s, lh = BH * s;
  var lw = (MID - BX) * s, rw = (BX + BW - MID) * s;
  var wl = lay.querySelector(".wl"), wr = lay.querySelector(".wr");
  if (wl){ wl.style.left = lx + "px"; wl.style.top = ly + "px"; wl.style.width = lw + "px"; wl.style.height = lh + "px"; }
  if (wr){ wr.style.left = (lx + lw) + "px"; wr.style.top = ly + "px"; wr.style.width = rw + "px"; wr.style.height = lh + "px"; }
}
window.addEventListener("resize", fitBnrFly);
window.addEventListener("load", fitBnrFly);
document.addEventListener("DOMContentLoaded", fitBnrFly);
if (document.readyState !== "loading") fitBnrFly();
requestAnimationFrame(function(){ window.__bnrRetry = 0; fitBnrFly(); });
setTimeout(fitBnrFly, 150);
setTimeout(fitBnrFly, 600);

(function loadSite(){
  if (!window.fetch) return;
  fetch("/api/site?t=" + Date.now(), { cache: "no-store" }).then(function(r){
    return r.json();
  }).then(function(d){
    if (!d) return;
    var img = document.getElementById("bnrImg");
    var bg = document.getElementById("bnrBg");
    var ph = document.getElementById("bnrPh");
    var link = document.getElementById("bnrLink");
    var fly = document.getElementById("bnrFly");
    if (img && ph){
      img.onerror = function(){ img.style.display = "none"; ph.style.display = "flex"; if (fly) fly.style.display = "none"; };
      img.onload = function(){ img.style.display = "block"; ph.style.display = "none"; fitBnrFly(); };
      img.style.display = "block";
      if (d.banner_img && d.banner_img !== img.getAttribute("src")) img.src = d.banner_img;
      if (bg) bg.src = img.getAttribute("src");
      if (fly && d.banner_img && d.banner_img.indexOf("banner_base") < 0) fly.style.display = "none";
    }
    if (d.banner_link){
      link.setAttribute("href", d.banner_link);
      link.setAttribute("target", "_blank");
      link.setAttribute("rel", "noopener");
    } else {
      link.removeAttribute("href");
      link.style.cursor = "default";
    }
    if (d.site_title) document.title = d.site_title;
  }).catch(function(){});
})();

renderHomeCats();
renderDrawCats();
resetDeck();
updCnt();

/* 预览开关：#dir → 直接进方向页；#dirB → 走 B 方案（牌在右微倾、蝶停牌顶） */
(function(){
  var h = (location.hash || "").toLowerCase();
  if (h === "#dirg"){ showView("dir"); document.getElementById("view-dir").classList.add("vg"); }
  else if (h === "#dir"){ showView("dir"); }
})();

/* ==================== 每日塔罗 · 一天只能抽一次 ==================== */
var dlyBusy = false, dlyOpened = false, DLY_KEY = "ppt_daily_record";
function dlyToday(){
  var d = new Date();
  return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2);
}
function dlyDateText(){
  var d = new Date(), wd = ["日","一","二","三","四","五","六"][d.getDay()];
  return d.getFullYear() + " 年 " + (d.getMonth() + 1) + " 月 " + d.getDate() + " 日 · 星期" + wd;
}
function dlyLoad(){
  try {
    var raw = localStorage.getItem(DLY_KEY);
    if (!raw) return null;
    var o = JSON.parse(raw);
    if (!o || o.d !== dlyToday()) return null;
    if (typeof o.i !== "number" || !CARDS || !CARDS[o.i]) return null;
    return o;
  } catch (e) { return null; }
}
function dlyRender(rec, animated){
  var c = (CARDS && CARDS[rec.i]) ? CARDS[rec.i] : null;
  if (!c) return;
  var w = document.getElementById("dlyWrap");
  var btn = document.getElementById("btnDlyGo");
  document.getElementById("dlyImg").src = c.u;
  document.getElementById("dlyName").textContent = c.n;
  var pe = document.getElementById("dlyPos");
  pe.textContent = rec.rev ? "逆位" : "正位";
  pe.className = rec.rev ? "neg" : "";
  document.getElementById("dlyKw").textContent = rec.rev ? c.kr : c.k;
  var t = dlyReading(c.n, rec.rev, rec.rev ? c.kr : c.k);
  document.getElementById("dlyP1").textContent = t[0];
  document.getElementById("dlyP2").textContent = t[1];
  document.getElementById("dlyP3").textContent = t[2];
  w.classList.remove("shake");
  if (rec.rev) w.classList.add("rev"); else w.classList.remove("rev");
  w.classList.add("open");
  document.getElementById("dlyAsk").style.display = "none";
  document.getElementById("dlyRes").style.display = "block";
  if (btn) btn.style.display = "none";
  document.getElementById("dlyDate").textContent = dlyDateText();
  dlyOpened = true;
}
function resetDaily(){
  dlyBusy = false; dlyOpened = false;
  var w = document.getElementById("dlyWrap");
  w.classList.remove("open"); w.classList.remove("rev"); w.classList.remove("shake");
  document.getElementById("dlyImg").removeAttribute("src");
  document.getElementById("dlyRes").style.display = "none";
  document.getElementById("dlyAsk").style.display = "block";
  var btn = document.getElementById("btnDlyGo");
  btn.style.display = ""; btn.textContent = "立即开启";
  document.getElementById("dlyDate").textContent = dlyDateText();
}
function syncDaily(){
  var rec = dlyLoad();
  if (rec) dlyRender(rec, false);
  else resetDaily();
}
function openDaily(){
  showView("daily");
  syncDaily();
}
function dlyReading(name, rev, kw){
  var good = kw && kw.indexOf("未收录") < 0;
  var k = good ? kw : "眼前这件事本身";
  if (!rev){
    return [
      "「" + name + "」今天正着站在你这边，气是往外走的。今天的主调是" + k + "。这股劲儿在你身上是活的，想做的事、想说的话，往外推一步不费劲。",
      "它不是让你原地等。你现在最耗力气的地方，不在事情本身，在心里那场反复演的戏——演一百遍，现实一步没动。",
      "把想了最久的那件事，拆出一个五分钟就能做完的小动作，现在就做掉。做完你会松一口气。"
    ];
  }
  return [
    "「" + name + "」今天是倒着的，气往回走。这张牌本来的主题是" + k + "，但它现在卡在你里面——可能是时机还不对，也可能是你自己还没准备好。",
    "倒着的牌不是坏消息。它是在说：这件事现在推不动，先别推。你越急，越容易把自己推去做一个后悔的决定。",
    "今天不做决定，只观察。把这事先放着，明天再看一眼，很多结自己会松。"
  ];
}
function drawDaily(){
  if (dlyBusy) return;
  if (!CARDS || !CARDS.length) return;
  if (dlyLoad()) return;
  dlyBusy = true;
  var w = document.getElementById("dlyWrap");
  var btn = document.getElementById("btnDlyGo");
  w.classList.add("shake");
  if (btn) btn.textContent = "开启中…";
  var idx = Math.floor(Math.random() * CARDS.length);
  var rev = Math.random() < 0.5;
  var rec = { d: dlyToday(), i: idx, rev: rev };
  setTimeout(function(){
    try { localStorage.setItem(DLY_KEY, JSON.stringify(rec)); } catch (e) {}
    dlyRender(rec, true);
    dlyBusy = false;
    try {
      var _dc = CARDS[idx];
      if (_dc && typeof trackEvent === "function"){
        trackEvent("daily", {
          result: _dc.n + " · " + (rev ? "逆位" : "正位"),
          detail: { 牌名: _dc.n, 位置: rev ? "逆位" : "正位",
                    关键词: rev ? _dc.kr : _dc.k, 日期: rec.d }
        });
      }
    } catch(e){}
  }, 620);
}
setInterval(function(){
  var el = document.getElementById("view-daily");
  if (!el || el.style.display === "none") return;
  if (!dlyLoad()) { if (dlyOpened) resetDaily(); }
}, 30000);
document.getElementById("btnDlyGo").addEventListener("click", drawDaily);
document.getElementById("btnHomeDaily").addEventListener("click", function(){ openDaily(); });

</script>
</body>
</html>"""


def build_front(cards_json, wechat):
    """把牌库 JSON 与微信号注入模板。"""
    html = FRONT_TEMPLATE.replace("/*__FRONT_CARDS__*/[]", "/*__FRONT_CARDS__*/" + cards_json)
    html = html.replace("__WECHAT__", wechat)
    return html


# ==================== 管理后台登录页 ====================
LOGIN_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>PPTAROT🔮 后台登录</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;color:#eae4f6;min-height:100vh;
background:radial-gradient(1200px 700px at 18% 0%,#2a1f4d 0%,#141a30 45%,#070b14 100%);padding:20px}
.loginwrap{min-height:100vh;display:flex;align-items:center;justify-content:center}
.loginbox{width:100%;max-width:340px}
.lgbrand{text-align:center;font-size:22px;letter-spacing:4px;color:#f0d79c;font-weight:700;text-shadow:0 0 18px rgba(240,215,156,.45);margin-bottom:6px}
.lgsub{text-align:center;font-size:12px;color:#8e86ad;letter-spacing:2px;margin-bottom:24px}
.lgcard{background:rgba(255,255,255,.045);border:1px solid rgba(240,215,156,.22);border-radius:18px;padding:22px 20px 16px}
.lgcard label{display:block;font-size:12px;color:#9c93bd;letter-spacing:1px;margin:0 0 6px}
.lgcard input{width:100%;background:rgba(10,10,20,.55);border:1px solid rgba(168,160,220,.35);border-radius:10px;
color:#eae4f6;font-size:14px;padding:11px 12px;margin-bottom:14px;font-family:inherit;outline:none}
.lgcard input:focus{border-color:rgba(240,215,156,.7)}
.lgbtn{width:100%;border:none;border-radius:10px;padding:12px;font-size:14px;letter-spacing:2px;font-family:inherit;
background:linear-gradient(120deg,#f0d79c,#e0b978);color:#1a1428;font-weight:700;cursor:pointer}
.lgbtn:active{opacity:.85}
.lgbtn:disabled{opacity:.55}
.lgerr{min-height:18px;text-align:center;font-size:12px;color:#ff9aa2;margin-top:10px;letter-spacing:.5px}
.lgback{display:block;text-align:center;font-size:12px;color:#8e86ad;margin-top:16px;text-decoration:none;letter-spacing:1px}
</style>
</head>
<body>
<div class="loginwrap">
  <div class="loginbox">
    <div class="lgbrand">PPTAROT<span style="letter-spacing:0">🔮</span></div>
    <div class="lgsub">管 理 后 台</div>
    <div class="lgcard">
      <label>账号</label>
      <input id="lgUser" autocomplete="username" placeholder="请输入账号">
      <label>密码</label>
      <input id="lgPass" type="password" autocomplete="current-password" placeholder="请输入密码">
      <button class="lgbtn" id="lgBtn">进 入 后 台</button>
      <div class="lgerr" id="lgErr"></div>
    </div>
    <a class="lgback" href="/">← 回前台抽牌页</a>
  </div>
</div>
<script>
function lgLogin(){
  var u=document.getElementById('lgUser').value.trim();
  var p=document.getElementById('lgPass').value;
  var e=document.getElementById('lgErr'), b=document.getElementById('lgBtn');
  if(!u || !p){ e.textContent='账号和密码都要填'; return; }
  b.disabled=true; e.textContent='';
  fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({username:u,password:p})})
    .then(function(r){ return r.json(); })
    .then(function(d){
      if(d && d.ok){ location.href='/admin'; }
      else { b.disabled=false; e.textContent=(d && d.error) ? d.error : '账号或密码不对'; }
    })
    .catch(function(){ b.disabled=false; e.textContent='连不上服务，检查一下是不是没启动'; });
}
document.getElementById('lgBtn').addEventListener('click', lgLogin);
document.addEventListener('keydown', function(ev){ if(ev.key==='Enter') lgLogin(); });
</script>
</body>
</html>
"""


def build_login():
    """返回后台登录页 HTML"""
    return LOGIN_TEMPLATE
