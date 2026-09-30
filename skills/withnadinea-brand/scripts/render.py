#!/usr/bin/env python3
"""
@withnadinea brand renderer.

Usage:
  python render.py spec.json OUT_DIR            # render a spec
  python render.py --recipe story_arc           # print a starter spec for a carousel type
  python render.py --list                       # list carousel types

Engines: Playwright/Chromium (preferred, auto-fits text) -> WeasyPrint + pdftoppm (fallback).
All fonts and textures are bundled in ../assets, so output never depends on system fonts.
"""
import json, sys, os, re, html, pathlib, subprocess, shutil, base64

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
FONTS = ASSETS / "fonts"

# ------------------------------------------------------------------ tokens
C = {
    "cream": "#F5EFE4", "paper": "#EDE4D3", "burgundy": "#6B1D25", "ink": "#3B1418",
    "terracotta": "#C4692F", "peach": "#EFA385", "mustard": "#E7B863", "blue": "#C2D2DA",
    "night": "#1C1114", "white": "#FFFFFF",
}
ZONE_COLOR = {"past": C["blue"], "present": C["mustard"], "future": C["peach"], "neutral": C["terracotta"]}
ZONE_LABEL = {
    "past": ("THE PAST", "الماضي"), "present": ("THE PRESENT", "الحاضر"),
    "future": ("THE FUTURE", "المستقبل"), "neutral": ("THE METHOD", "الطريقة"),
}
SKILLS = {
    1: ("Observe without judgment", "لاحظي بدون حكم", "past"),
    2: ("Catch patterns, not incidents", "التقطي النمط مش الحادثة", "past"),
    3: ("Know your energy", "اعرفي طاقتك", "present"),
    4: ("Be here", "كوني هون", "present"),
    5: ("Decide on purpose", "قرّري بوعي", "future"),
    6: ("Smart flexibility", "مرونة ذكية", "future"),
}
HANDLE = "@withnadinea"
CTA = {
    "method": ("اعرفي أكتر عن الطريقة", "Know more about the method"),
    "book": ("احجزي جلسة معي", "Book a session with me"),
}

# theme -> background css, fg, accent, grain, highlight style
THEMES = {
    "cream":    dict(bg=C["cream"], fg=C["ink"], acc=C["burgundy"], grain="dark", hl=C["mustard"]),
    "past":     dict(bg=C["blue"], fg=C["ink"], acc=C["burgundy"], grain="dark", hl=C["mustard"]),
    "present":  dict(bg=f"radial-gradient(ellipse 80% 60% at 50% 45%, #F3CF86 0%, {C['mustard']} 55%, #D9A54E 100%)",
                     fg=C["ink"], acc=C["burgundy"], grain="dark", hl=C["cream"]),
    "future":   dict(bg=C["peach"], fg=C["ink"], acc=C["burgundy"], grain="dark", hl=C["mustard"]),
    "night":    dict(bg=f"radial-gradient(ellipse 70% 55% at 45% 42%, #3a2327 0%, {C['night']} 62%, #0e0809 100%)",
                     fg="#FFFFFF", acc=C["mustard"], grain="light", hl=None),
    "burgundy": dict(bg=C["burgundy"], fg=C["cream"], acc=C["mustard"], grain="light", hl=None),
}
DEFAULT_THEME = {
    "cover": "cream", "statement": "zone", "text": "cream", "skill": "zone", "quote": "night",
    "steps": "cream", "compare": "cream", "checklist": "zone", "zonemap": "cream", "cta": "burgundy",
    "photo": "night", "notebook": "present",
}

# ------------------------------------------------------------------ carousel system (9 types)
CAROUSELS = {
    "story_arc": dict(ar="القصة", en="Story Arc", slides=["cover", "text", "statement", "text", "statement", "skill", "cta"],
                      trigger="A full client journey with emotion and a turn (Angle C). Source moment >= 150 words.", length="7"),
    "belief_shift": dict(ar="كانت فاكرة… طلع", en="Belief Shift", slides=["cover", "compare", "compare", "statement", "cta"],
                         trigger="A clear 'what she thought vs what was actually happening'.", length="5"),
    "skill_spotlight": dict(ar="مهارة", en="Skill Spotlight", slides=["cover", "skill", "text", "steps", "cta"],
                            trigger="The lesson is one named skill (1-6).", length="5"),
    "diagnostic": dict(ar="إذا هاد عم يصير معك", en="Diagnostic", slides=["cover", "checklist", "statement", "skill", "cta"],
                       trigger="A set of 3-5 recognisable symptoms / 'if this keeps happening'.", length="5"),
    "notebook": dict(ar="دفتر نادين", en="Coach's Notebook", slides=["statement", "notebook", "notebook", "cta"],
                     trigger="Coach POV or philosophy (Angle A/B), reflective, 120-300 words.", length="3-5"),
    "quote_drop": dict(ar="جملة", en="Quote Drop", slides=["quote"],
                       trigger="One strong line <= 25 words that stands alone.", length="1-3"),
    "zone_map": dict(ar="خريطة الأزمنة", en="Zone Map", slides=["cover", "zonemap", "text", "text", "text", "cta"],
                     trigger="A situation read across past, present and future.", length="6"),
    "micro_case": dict(ar="حالة قصيرة", en="Micro Case", slides=["cover", "compare", "statement", "cta"],
                       trigger="A short transformation, source moment < 120 words.", length="4"),
    "try_this": dict(ar="جرّبي هيك", en="Try This", slides=["cover", "steps", "steps", "statement", "cta"],
                     trigger="An exercise with 3-6 concrete steps.", length="4-6"),
}

# ------------------------------------------------------------------ helpers
def esc(s): return html.escape(str(s or ""))

def hl(text, word, color):
    """Wrap first occurrence of `word` in a highlighter span."""
    t = esc(text)
    if word and color:
        w = esc(word)
        t = t.replace(w, f"<span class='hl' style='background:linear-gradient(transparent 10%,{color} 10%,{color} 92%,transparent 92%)'>{w}</span>", 1)
    elif word:
        w = esc(word)
        t = t.replace(w, f"<span style='color:{C['mustard']}'>{w}</span>", 1)
    return t.replace("\n", "<br>")

def size_for(text, steps):
    n = len(str(text or ""))
    for limit, px in steps:
        if n <= limit: return px
    return steps[-1][1]

def font_face():
    u = lambda f: (FONTS / f).as_uri()
    return f"""
@font-face{{font-family:'Lalezar';src:url('{u('Lalezar-Regular.ttf')}')}}
@font-face{{font-family:'Cairo';src:url('{u('Cairo-VF.ttf')}');font-weight:200 1000}}
@font-face{{font-family:'Figtree';src:url('{u('Figtree-VF.ttf')}');font-weight:300 900}}
@font-face{{font-family:'Figtree';src:url('{u('Figtree-Italic-VF.ttf')}');font-weight:300 900;font-style:italic}}
"""

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
.slide{position:relative;overflow:hidden}
.grain{position:absolute;left:0;top:0;right:0;bottom:0;background-repeat:repeat;pointer-events:none}
.disp{font-family:'Lalezar';line-height:1.14}
.disp.en{font-family:'Figtree';font-weight:800;letter-spacing:-.02em;line-height:1.02}
.body{font-family:'Cairo';font-weight:500;line-height:1.7}
.body.en{font-family:'Figtree';font-weight:400;line-height:1.45}
.lab{font-family:'Figtree';font-weight:700;letter-spacing:.16em;font-size:22px}
.hl{padding:0 10px;border-radius:4px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.fit{overflow:hidden;flex-shrink:0}
"""

def mark_svg(color, h=40):
    return (f"<svg width='{h*2.2:.0f}' height='{h}' viewBox='0 0 110 50'>"
            f"<path d='M5 20 A15 15 0 0 0 35 20 Z' fill='{color}'/><circle cx='55' cy='25' r='13' fill='{color}'/>"
            f"<path d='M75 32 A15 15 0 0 1 105 32 Z' fill='{color}'/></svg>")

def lockup(color, scale=1.0):
    s = scale
    return (f"<div style='display:flex;align-items:center;color:{color}'>{mark_svg(color, int(40*s))}"
            f"<div style='margin-left:{14*s}px;line-height:1;white-space:nowrap'><div class='disp' style='font-size:{34*s}px;direction:rtl'>مع نادين</div>"
            f"<div class='lab' style='font-size:{14*s}px;letter-spacing:.22em;margin-top:{4*s}px'>WITH NADINE</div></div></div>")

def zone_shape(zone, color, w, h):
    """Descending half (past), circle (present), rising half (future), stacked arches (neutral)."""
    if zone == "past":
        return f"<svg width='{w}' height='{h}' viewBox='0 0 200 100'><path d='M0 0 A100 100 0 0 0 200 0Z' fill='{color}'/></svg>"
    if zone == "present":
        return f"<svg width='{w}' height='{w}' viewBox='0 0 200 200'><circle cx='100' cy='100' r='100' fill='{color}'/></svg>"
    if zone == "future":
        return f"<svg width='{w}' height='{h}' viewBox='0 0 200 100'><path d='M0 100 A100 100 0 0 1 200 100Z' fill='{color}'/></svg>"
    return f"<svg width='{w}' height='{h}' viewBox='0 0 200 100'><path d='M0 100 A100 100 0 0 1 200 100Z' fill='{color}'/></svg>"

def arch_cluster(zone, accent):
    """Bottom-right cluster of zone shapes for covers."""
    col = ZONE_COLOR.get(zone, C["terracotta"])
    if zone == "past":
        d = [("M260 0 A130 130 0 0 0 520 0Z", col), ("M0 170 A130 130 0 0 0 260 170Z", col),
             ("M260 170 A130 130 0 0 0 520 170Z", col), ("M0 340 A130 130 0 0 0 260 340Z", accent),
             ("M260 340 A130 130 0 0 0 520 340Z", col)]
        return "<svg style='position:absolute;right:0;bottom:0' width='520' height='470' viewBox='0 0 520 470'>" + \
               "".join(f"<path d='{p}' fill='{c}'/>" for p, c in d) + "</svg>"
    if zone == "future":
        d = [("M0 470 A130 130 0 0 1 260 470Z", col), ("M260 470 A130 130 0 0 1 520 470Z", accent),
             ("M260 300 A130 130 0 0 1 520 300Z", col), ("M0 300 A130 130 0 0 1 260 300Z", col),
             ("M260 130 A130 130 0 0 1 520 130Z", col)]
        return "<svg style='position:absolute;right:0;bottom:0' width='520' height='470' viewBox='0 0 520 470'>" + \
               "".join(f"<path d='{p}' fill='{c}'/>" for p, c in d) + "</svg>"
    if zone == "present":
        return (f"<svg style='position:absolute;right:-80px;bottom:-80px' width='560' height='560' viewBox='0 0 200 200'>"
                f"<circle cx='100' cy='100' r='100' fill='{col}'/><circle cx='100' cy='100' r='46' fill='{accent}'/></svg>")
    return (f"<svg style='position:absolute;right:0;bottom:0' width='520' height='300' viewBox='0 0 520 300'>"
            f"<path d='M0 300 A130 130 0 0 1 260 300Z' fill='{C['blue']}'/><path d='M260 300 A130 130 0 0 1 520 300Z' fill='{C['peach']}'/>"
            f"<circle cx='260' cy='110' r='90' fill='{C['mustard']}'/></svg>")

# ------------------------------------------------------------------ slide builders
W, H = 1080, 1350

def chrome(t, i, n, show_counter=False, mark_pos="bottom"):
    """Brand chrome: logo only. No slide counters or page pills (Instagram shows position)."""
    out = ""
    if mark_pos == "bottom":
        out += f"<div style='position:absolute;bottom:64px;left:80px'>{lockup(t['acc'] if t['grain']=='dark' else t['fg'])}</div>"
    elif mark_pos == "top":
        out += f"<div style='position:absolute;top:64px;left:80px'>{mark_svg(t['acc'], 34)}</div>"
    return out

def d(lang): return "rtl" if lang == "ar" else "ltr"
def al(lang): return "right" if lang == "ar" else "left"

def kicker(txt_en, txt_ar, color, lang):
    return (f"<div class='lab' style='color:{color};direction:ltr;text-align:{al(lang)};margin-bottom:26px'>"
            f"{esc(txt_en)}{' · ' + esc(txt_ar) if txt_ar and lang=='ar' else ''}</div>")

def L_cover(s, t, z, lang):
    title = s.get("title", ""); sub = s.get("sub", "")
    k = s.get("kicker") or (ZONE_LABEL[z][0], ZONE_LABEL[z][1])
    k_en, k_ar = (k if isinstance(k, (list, tuple)) else (k, ""))
    fs = size_for(title, [(18, 132), (30, 116), (44, 98), (70, 84), (999, 72)])
    return (arch_cluster(z, t["acc"]) +
            f"<div style='position:absolute;top:230px;right:80px;left:80px;direction:{d(lang)};text-align:{al(lang)};color:{t['fg']}'>"
            f"{kicker(k_en, k_ar, t['acc'], lang)}"
            f"<div class='disp fit {'' if lang=='ar' else 'en'}' style='font-size:{fs}px;max-height:520px'>{hl(title, s.get('hl_title'), t['hl'])}</div>"
            f"<div class='body fit {'' if lang=='ar' else 'en'}' style='font-size:{size_for(sub,[(60,40),(120,36),(999,32)])}px;margin-top:34px;max-width:800px;{'margin-left:auto' if lang=='ar' else ''};opacity:.88;max-height:260px'>{hl(sub, s.get('hl'), t['hl'])}</div>"
            f"</div>")

def L_statement(s, t, z, lang):
    txt = s.get("text", "")
    fs = size_for(txt, [(20, 132), (36, 112), (60, 94), (90, 80), (999, 68)])
    en = s.get("en")
    shape = zone_shape(z, t["acc"] if t['grain']=='dark' else C['mustard'], 260, 130)
    return (f"<div style='position:absolute;left:80px;bottom:150px;opacity:.9'>{shape}</div>"
            f"<div style='position:absolute;top:0;bottom:0;right:80px;left:80px;display:flex;flex-direction:column;justify-content:center;"
            f"direction:{d(lang)};text-align:{al(lang)};color:{t['fg']}'>"
            f"<div class='disp fit {'' if lang=='ar' else 'en'}' style='font-size:{fs}px;max-height:760px'>{hl(txt, s.get('hl'), t['hl'])}</div>"
            + (f"<div class='lab' style='font-size:34px;letter-spacing:.02em;margin-top:30px;color:{t['acc']};direction:ltr;text-align:{al(lang)}'>{esc(en).upper()}</div>" if en else "")
            + "</div>")

def L_text(s, t, z, lang):
    paras = s.get("paragraphs") or [s.get("text", "")]
    total = sum(len(p) for p in paras)
    fs = size_for("x" * total, [(160, 46), (260, 42), (380, 38), (999, 34)])
    title = s.get("title")
    return (f"<div style='position:absolute;top:190px;bottom:190px;right:90px;left:90px;display:flex;flex-direction:column;justify-content:center;direction:{d(lang)};text-align:{al(lang)};color:{t['fg']}'>"
            + (f"<div class='disp {'' if lang=='ar' else 'en'}' style='font-size:72px;margin-bottom:30px;color:{t['acc']}'>{esc(title)}</div>" if title else "")
            + "".join(f"<p class='body {'' if lang=='ar' else 'en'}' style='font-size:{fs}px;margin:17px 0'>{hl(p, s.get('hl'), t['hl'])}</p>" for p in paras)
            + "</div>")

def L_notebook(s, t, z, lang):
    return L_text(s, t, z, lang)

def L_skill(s, t, z, lang):
    n = int(s.get("skill", 1)); en_name, ar_name, sz = SKILLS[n]
    title = s.get("title") or (ar_name if lang == "ar" else en_name)
    body = s.get("body", "")
    fs = size_for(title, [(14, 108), (26, 92), (40, 78), (999, 66)])
    top_col = C["cream"]; bot_col = t["acc"] if t["grain"] == "dark" else C["mustard"]
    return (f"<svg style='position:absolute;left:60px;bottom:170px' width='440' height='440' viewBox='0 0 640 640'>"
            f"<circle cx='320' cy='320' r='300' fill='{top_col}'/><path d='M20 320 A300 300 0 0 0 620 320Z' fill='{bot_col}'/></svg>"
            f"<div style='position:absolute;left:60px;width:440px;text-align:center;bottom:395px;font-family:Lalezar;font-size:190px;color:{C['burgundy']};line-height:1'>{n}</div>"
            f"<div style='position:absolute;top:210px;right:80px;width:560px;direction:{d(lang)};text-align:{al(lang)};color:{t['fg']}'>"
            f"{kicker(f'SKILL {n} OF 6', f'المهارة {n} من ٦', t['acc'], lang)}"
            f"<div class='disp fit {'' if lang=='ar' else 'en'}' style='font-size:{fs}px;max-height:420px'>{esc(title)}</div>"
            f"<div class='body fit {'' if lang=='ar' else 'en'}' style='font-size:{size_for(body,[(80,36),(150,32),(999,29)])}px;margin-top:30px;max-height:420px'>{hl(body, s.get('hl'), t['hl'])}</div></div>")

def L_quote(s, t, z, lang):
    txt = s.get("text", ""); en = s.get("en", "")
    fs = size_for(txt, [(24, 116), (44, 104), (70, 90), (110, 76), (999, 64)])
    return (f"<div style='position:absolute;left:90px;right:90px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center'>"
            f"<div class='disp fit {'' if lang=='ar' else 'en'}' style='font-size:{fs}px;color:#fff;line-height:1.25;direction:{d(lang)};text-align:{al(lang)};max-height:700px'>{hl(txt, s.get('hl'), None)}</div>"
            + (f"<div style='font:800 {size_for(en,[(40,48),(90,42),(999,36)])}px/1.12 Figtree;color:{C['mustard']};margin-top:34px;text-align:{al(lang)};text-transform:uppercase'>{esc(en)}</div>" if en else "")
            + "</div>")

def L_steps(s, t, z, lang):
    items = s.get("items", [])[:5]; start = int(s.get("start", 1)); title = s.get("title", "")
    fs = size_for(" ".join(items), [(120, 38), (220, 34), (999, 30)])
    rows = "".join(
        f"<div style='display:flex;align-items:flex-start;margin-bottom:34px;flex-direction:{'row-reverse' if lang=='ar' else 'row'}'>"
        f"<div style='flex:none;width:70px;height:70px;border-radius:50%;background:{C['mustard'] if t['bg']!=C['mustard'] else C['cream']};color:{C['ink']};"
        f"font-family:Lalezar;font-size:40px;display:flex;align-items:center;justify-content:center;{'margin-left:26px' if lang=='ar' else 'margin-right:26px'}'>{start+i}</div>"
        f"<div class='body {'' if lang=='ar' else 'en'}' style='font-size:{fs}px;padding-top:6px;direction:{d(lang)};text-align:{al(lang)};flex:1'>{esc(it)}</div></div>"
        for i, it in enumerate(items))
    return (f"<div style='position:absolute;top:200px;right:80px;left:80px;color:{t['fg']}'>"
            + (f"<div class='disp {'' if lang=='ar' else 'en'}' style='font-size:{size_for(title,[(20,96),(36,80),(999,66)])}px;direction:{d(lang)};text-align:{al(lang)};margin-bottom:50px'>{esc(title)}</div>" if title else "")
            + rows + "</div>")

def L_compare(s, t, z, lang):
    la = s.get("label_a") or ("كانت فاكرة" if lang == "ar" else "She thought"); a = s.get("a", "")
    lb = s.get("label_b") or ("طلع" if lang == "ar" else "It was actually"); b = s.get("b", "")
    fa = size_for(a, [(30, 64), (60, 54), (999, 44)]); fb = size_for(b, [(30, 70), (60, 58), (999, 48)])
    zc = ZONE_COLOR.get(z, C["terracotta"])
    return (f"<div style='position:absolute;left:80px;right:80px;top:190px;height:430px;border-radius:36px;background:rgba(59,20,24,.07);padding:50px 56px;direction:{d(lang)};text-align:{al(lang)};color:{t['fg']}'>"
            f"<div class='lab' style='color:{t['acc']};direction:{d(lang)};font-family:{'Cairo' if lang=='ar' else 'Figtree'};font-size:30px;letter-spacing:{0 if lang=='ar' else '.12em'}'>{esc(la)}</div>"
            f"<div class='disp {'' if lang=='ar' else 'en'}' style='font-size:{fa}px;margin-top:20px;opacity:.75'>{esc(a)}</div></div>"
            f"<svg style='position:absolute;left:470px;top:596px' width='140' height='70' viewBox='0 0 200 100'><path d='M0 0 A100 100 0 0 0 200 0Z' fill='{zc}'/></svg>"
            f"<div style='position:absolute;left:80px;right:80px;top:680px;height:470px;border-radius:36px;background:{t['acc'] if t['grain']=='dark' else C['mustard']};padding:50px 56px;direction:{d(lang)};text-align:{al(lang)};color:{C['cream'] if t['grain']=='dark' else C['ink']}'>"
            f"<div class='lab' style='font-family:{'Cairo' if lang=='ar' else 'Figtree'};font-size:30px;letter-spacing:{0 if lang=='ar' else '.12em'};opacity:.85'>{esc(lb)}</div>"
            f"<div class='disp {'' if lang=='ar' else 'en'}' style='font-size:{fb}px;margin-top:20px'>{esc(b)}</div></div>")

def L_checklist(s, t, z, lang):
    items = s.get("items", [])[:5]; title = s.get("title", "")
    rows = "".join(
        f"<div style='display:flex;align-items:center;margin-bottom:30px;flex-direction:{'row-reverse' if lang=='ar' else 'row'}'>"
        f"<div style='flex:none;{'margin-left:24px' if lang=='ar' else 'margin-right:24px'}'>{zone_shape('past', t['acc'], 64, 32)}</div>"
        f"<div class='body {'' if lang=='ar' else 'en'}' style='font-size:{size_for(it,[(30,40),(60,36),(999,32)])}px;direction:{d(lang)};text-align:{al(lang)};flex:1'>{esc(it)}</div></div>"
        for it in items)
    return (f"<div style='position:absolute;top:200px;right:80px;left:80px;color:{t['fg']}'>"
            f"<div class='disp {'' if lang=='ar' else 'en'}' style='font-size:{size_for(title,[(20,96),(36,80),(999,66)])}px;direction:{d(lang)};text-align:{al(lang)};margin-bottom:50px'>{esc(title)}</div>"
            + rows + "</div>")

def L_zonemap(s, t, z, lang):
    zones = s.get("zones", {}); focus = s.get("focus", z); title = s.get("title", "")
    cols = ""
    order = ["past", "present", "future"] if lang == "en" else ["future", "present", "past"]
    for zz in order:
        on = zz == focus
        name = ZONE_LABEL[zz][1] if lang == "ar" else ZONE_LABEL[zz][0].title()
        cols += (f"<div style='flex:1;margin:0 12px;border-radius:30px;padding:36px 26px;text-align:center;"
                 f"background:{'rgba(107,29,37,.95)' if on else 'rgba(59,20,24,.06)'};color:{C['cream'] if on else t['fg']}'>"
                 f"<div style='height:130px;display:flex;align-items:center;justify-content:center'>{zone_shape(zz, ZONE_COLOR[zz], 150, 75)}</div>"
                 f"<div class='disp {'' if lang=='ar' else 'en'}' style='font-size:52px;margin-top:10px'>{esc(name)}</div>"
                 f"<div class='body {'' if lang=='ar' else 'en'}' style='font-size:28px;margin-top:14px;direction:{d(lang)}'>{esc(zones.get(zz,''))}</div></div>")
    return (f"<div style='position:absolute;top:200px;right:80px;left:80px;direction:{d(lang)};text-align:{al(lang)};color:{t['fg']}'>"
            f"<div class='disp {'' if lang=='ar' else 'en'}' style='font-size:{size_for(title,[(20,96),(36,80),(999,66)])}px'>{esc(title)}</div></div>"
            f"<div style='position:absolute;left:68px;right:68px;top:520px;display:flex;direction:ltr'>{cols}</div>")

def L_cta(s, t, z, lang):
    kind = s.get("cta_kind", "method")
    line = s.get("text") or (CTA[kind][0] if lang == "ar" else CTA[kind][1])
    sub = s.get("sub") or ("الرابط بالبايو" if lang == "ar" else "Link in bio")
    closer = s.get("closer", "")
    return (f"<svg style='position:absolute;left:0;right:0;bottom:0' width='1080' height='420' viewBox='0 0 1080 420'>"
            f"<path d='M0 420 A180 180 0 0 1 360 420Z' fill='{C['blue']}'/><path d='M360 420 A180 180 0 0 1 720 420Z' fill='{C['mustard']}'/>"
            f"<path d='M720 420 A180 180 0 0 1 1080 420Z' fill='{C['peach']}'/></svg>"
            f"<div style='position:absolute;top:220px;right:80px;left:80px;direction:{d(lang)};text-align:{al(lang)};color:{t['fg']}'>"
            + (f"<div class='body {'' if lang=='ar' else 'en'}' style='font-size:36px;opacity:.85;margin-bottom:40px'>{esc(closer)}</div>" if closer else "")
            + f"<div class='disp {'' if lang=='ar' else 'en'}' style='font-size:{size_for(line,[(22,110),(40,92),(999,76)])}px'>{esc(line)}</div>"
            + f"<div class='{'body' if lang=='ar' else 'lab'}' style='margin-top:30px;font-size:40px;letter-spacing:{0 if lang=='ar' else '.08em'};color:{C['mustard']}'>{esc(sub)}</div>"
            + f"<div style='margin-top:26px;font:700 44px Figtree;direction:ltr;text-align:{al(lang)};color:{t['fg']}'>{HANDLE}</div></div>")

def L_photo(s, t, z, lang):
    img = s.get("image")
    uri = pathlib.Path(img).resolve().as_uri() if img and os.path.exists(img) else None
    bg = (f"<div style='position:absolute;left:0;top:0;right:0;bottom:0;background:url(\"{uri}\") center/cover'></div>" if uri else "")
    title = s.get("title", ""); sub = s.get("sub", "")
    return (bg + "<div style='position:absolute;left:0;top:0;right:0;bottom:0;background:linear-gradient(180deg,rgba(28,17,20,.25) 0%,rgba(28,17,20,.15) 40%,rgba(28,17,20,.85) 100%)'></div>"
            f"<div style='position:absolute;left:80px;right:80px;bottom:190px;direction:{d(lang)};text-align:{al(lang)};color:#fff'>"
            f"<div class='disp {'' if lang=='ar' else 'en'}' style='font-size:{size_for(title,[(20,110),(40,92),(999,76)])}px'>{hl(title, s.get('hl'), None)}</div>"
            + (f"<div class='body {'' if lang=='ar' else 'en'}' style='font-size:36px;margin-top:20px;opacity:.9'>{esc(sub)}</div>" if sub else "")
            + "</div>")

LAYOUTS = dict(cover=L_cover, statement=L_statement, text=L_text, notebook=L_notebook, skill=L_skill, quote=L_quote,
               steps=L_steps, compare=L_compare, checklist=L_checklist, zonemap=L_zonemap, cta=L_cta, photo=L_photo)
MARK_POS = dict(cover="bottom", statement="bottom", text="top", notebook="top", skill="bottom", quote="top",
                steps="top", compare="top", checklist="top", zonemap="top", cta="none", photo="top")

def theme_for(layout, s, zone):
    name = s.get("theme") or DEFAULT_THEME.get(layout, "cream")
    if name == "zone":
        name = {"past": "past", "present": "present", "future": "future"}.get(zone, "cream")
    return name, THEMES[name]

def slide_html(s, i, n, zone, lang, single=False):
    layout = s["layout"]; tname, t = theme_for(layout, s, s.get("zone", zone))
    z = s.get("zone", zone)
    lang = s.get("lang", lang)
    body = LAYOUTS[layout](s, t, z, lang)
    grain = (ASSETS / f"grain_{t['grain']}.png").as_uri()
    return (f"<div class='slide' style='width:{W}px;height:{H}px;background:{t['bg']}'>"
            f"{body}<div class='grain' style='background-image:url(\"{grain}\");opacity:{.55 if t['grain']=='dark' else .35}'></div>"
            f"{chrome(t, i, n, show_counter=not single, mark_pos=MARK_POS[layout])}</div>")

# ------------------------------------------------------------------ vertical formats (reel cover / story / highlight)
def reel_cover_html(s, zone):
    img = s.get("image"); uri = pathlib.Path(img).resolve().as_uri() if img and os.path.exists(img) else None
    bg = (f"background:url(\"{uri}\") center/cover" if uri else
          f"background:radial-gradient(ellipse 80% 55% at 50% 40%, #4a2e30 0%, {C['night']} 65%, #0e0809 100%)")
    shape = "" if uri else f"<div style='position:absolute;left:340px;top:620px;opacity:.9'>{zone_shape(zone, ZONE_COLOR.get(zone, C['mustard']), 400, 200)}</div>"
    name = s.get("speaker", "نادين أبو زنط"); role = s.get("role", "كوتش · المناطق الزمنية الثلاث")
    l1 = s.get("line1", ""); l2 = s.get("line2", "")
    return (f"<div class='slide' style='width:1080px;height:1920px;{bg}'>{shape}"
            "<div style='position:absolute;left:0;top:0;right:0;bottom:0;background:linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,.05) 35%,rgba(0,0,0,.55) 72%,rgba(0,0,0,.8) 100%)'></div>"
            f"<div class='grain' style='background-image:url(\"{(ASSETS/'grain_light.png').as_uri()}\");opacity:.3'></div>"
            f"<div style='position:absolute;top:300px;right:170px;left:90px;direction:rtl;text-align:right'>"
            f"<div class='disp' style='font-size:54px;color:{C['mustard']}'>{esc(name)}</div>"
            f"<div class='body' style='font-size:28px;color:rgba(255,255,255,.85)'>{esc(role)}</div></div>"
            f"<div style='position:absolute;left:90px;right:170px;top:1120px;text-align:center;direction:rtl'>"
            f"<div style='font:700 {size_for(l1,[(26,54),(44,46),(999,40)])}px Cairo;color:#fff;text-shadow:0 2px 12px rgba(0,0,0,.5)'>{esc(l1)}</div>"
            f"<div class='disp' style='font-size:{size_for(l2,[(16,100),(28,84),(999,70)])}px;color:{C['mustard']}'>{esc(l2)}</div></div>"
            f"<div style='position:absolute;left:0;right:0;top:1390px;display:flex;justify-content:center'>{lockup('#fff')}</div></div>")

def story_html(s, zone):
    t = THEMES[s.get("theme", {"past":"past","present":"present","future":"future"}.get(zone, "cream"))]
    txt = s.get("text", ""); sub = s.get("sub", "")
    return (f"<div class='slide' style='width:1080px;height:1920px;background:{t['bg']}'>"
            f"<div style='position:absolute;left:0;right:0;bottom:440px;display:flex;justify-content:center;opacity:.9'>{zone_shape(zone, t['acc'], 420, 210)}</div>"
            f"<div style='position:absolute;top:360px;left:100px;right:160px;direction:rtl;text-align:right;color:{t['fg']}'>"
            f"<div class='disp' style='font-size:{size_for(txt,[(24,120),(44,100),(999,82)])}px'>{hl(txt, s.get('hl'), t['hl'])}</div>"
            + (f"<div class='body' style='font-size:40px;margin-top:30px'>{esc(sub)}</div>" if sub else "")
            + f"</div><div class='grain' style='background-image:url(\"{(ASSETS/('grain_'+t['grain']+'.png')).as_uri()}\");opacity:.5'></div>"
            f"<div style='position:absolute;top:280px;left:100px'>{lockup(t['acc'] if t['grain']=='dark' else t['fg'])}</div></div>")

def highlight_html(item):
    z = item.get("zone", "neutral"); label = item.get("label", "")
    num = item.get("skill")
    inner = (f"<div style='font-family:Lalezar;font-size:300px;color:{C['cream']};line-height:1'>{num}</div>" if num else
             zone_shape(z, C["cream"], 420, 210))
    return (f"<div class='slide' style='width:1080px;height:1920px;background:{C['burgundy'] if num else ZONE_COLOR.get(z, C['burgundy'])}'>"
            f"<div style='position:absolute;left:0;right:0;top:0;bottom:0;display:flex;align-items:center;justify-content:center'>{inner}</div>"
            f"<div style='position:absolute;left:0;right:0;top:1300px;text-align:center' class='disp'><span style='font-size:70px;color:{C['cream']}'>{esc(label)}</span></div></div>")

# ------------------------------------------------------------------ A4 documents
SKILL_AR = {k: v[1] for k, v in SKILLS.items()}; SKILL_EN = {k: v[0] for k, v in SKILLS.items()}

def summary_section(sec, lang, zone, focus, name, date, page, total):
    """Two A4 pages per language: (A) where you stand, skills, uncovered, recommendations;
    (B) this week, journal prompts with writing lines, next step."""
    ar = lang == "ar"; dirr = "rtl" if ar else "ltr"; ta = "right" if ar else "left"
    L = (lambda a, e: a if ar else e)
    body_font = 'Cairo' if ar else 'Figtree'
    skills = "".join(
        f"<div style='flex:1;margin:0 1.5mm;border-radius:4mm;padding:4mm 2mm;text-align:center;"
        f"background:{C['burgundy'] if k in focus else 'rgba(107,29,37,.06)'};color:{C['cream'] if k in focus else C['ink']}'>"
        f"<div style='font-family:Lalezar;font-size:24pt;line-height:1'>{k}</div>"
        f"<div style='font-family:{body_font};font-size:8.5pt;line-height:1.35;margin-top:1.5mm'>{esc(SKILL_AR[k] if ar else SKILL_EN[k])}</div></div>"
        for k in (range(1, 7)))
    recs = "".join(
        f"<div style='display:flex;flex-direction:row;margin-bottom:3.5mm;align-items:flex-start'>"
        f"<div style='flex:none;width:8mm;height:8mm;border-radius:50%;background:{C['mustard']};font-family:Lalezar;font-size:13pt;display:flex;align-items:center;justify-content:center;{'margin-left' if ar else 'margin-right'}:3mm'>{i+1}</div>"
        f"<div style='font-family:{body_font};font-size:10.5pt;line-height:1.65;direction:{dirr};text-align:{ta};flex:1'>{esc(r.get('text',''))} <b>{L('المهارة','Skill')} {r.get('skill','')}</b></div></div>"
        for i, r in enumerate(sec.get("recommendations", [])))
    unc = "".join(f"<li style='margin-bottom:1mm'>{esc(u)}</li>" for u in sec.get("uncovered", []))
    jp = "".join(
        f"<div style='margin-bottom:7mm'><div style='display:flex;flex-direction:row;align-items:baseline'>"
        f"<span style='font-family:Lalezar;font-size:15pt;color:{C['burgundy']};{'margin-left' if ar else 'margin-right'}:3mm'>{i+1}</span>"
        f"<span style='font-family:{body_font};font-size:11.5pt;font-weight:600;line-height:1.6;flex:1;text-align:{ta}'>{esc(u)}</span></div>"
        + "".join("<div style='border-bottom:1px solid rgba(107,29,37,.22);height:9mm'></div>" for _ in range(3))
        + "</div>" for i, u in enumerate(sec.get("journal_prompts", [])))
    ws = sec.get("where_you_stand", {})
    head = (f"<div style='display:flex;justify-content:space-between;align-items:center;border-bottom:1.5px solid rgba(107,29,37,.25);padding-bottom:5mm;direction:ltr'>"
            f"{lockup(C['burgundy'])}"
            f"<div style='text-align:right'><div class='lab' style='font-size:8pt;color:{C['burgundy']}'>{L('ملخّص الجلسة','SESSION SUMMARY')}</div>"
            f"<div style='font:600 11.5pt {body_font};direction:{dirr}'><bdi>{esc(name)}</bdi> · <bdi>{esc(date)}</bdi></div></div></div>")
    foot = lambda n: (f"<div style='position:absolute;left:18mm;right:18mm;bottom:11mm;display:flex;justify-content:space-between;font:500 8pt Figtree;color:rgba(59,20,24,.55);border-top:1px solid rgba(107,29,37,.2);padding-top:3mm;direction:ltr'>"
                      f"<span>Coaching, not therapy · كوتشينغ، مش علاج · {HANDLE}</span><span>{n} / {total}</span></div>")
    lab = lambda a, e, mb=3: f"<div class='lab' style='font-size:8pt;color:{C['burgundy']};text-align:{ta};margin-bottom:{mb}mm'>{L(a, e)}</div>"
    page_a = f"""
<div class='a4' style='direction:{dirr}'>
 {head}
 <div style='margin-top:7mm;border-radius:6mm;padding:7mm 8mm;background:{ZONE_COLOR.get(zone, C['blue'])};position:relative;min-height:38mm'>
   <div style='position:absolute;{'left' if ar else 'right'}:8mm;top:8mm'>{zone_shape(zone, C['burgundy'], 130, 65)}</div>
   <div style='{'margin-left' if ar else 'margin-right'}:45mm;text-align:{ta}'>
    <div class='lab' style='font-size:8pt;color:{C['burgundy']}'>{L('وين واقفة','WHERE YOU STAND')}</div>
    <div class='disp {'' if ar else 'en'}' style='font-size:26pt;margin-top:2mm'>{esc(ws.get('title',''))}</div>
    <div style='font-family:{body_font};font-size:10.5pt;line-height:1.65;margin-top:2mm'>{esc(ws.get('body',''))}</div></div></div>
 <div style='margin-top:8mm'>{lab('مهاراتك الست','YOUR SIX SKILLS')}<div style='display:flex;direction:{dirr}'>{skills}</div></div>
 <div style='margin-top:8mm;text-align:{ta}'>{lab('شو اكتشفنا','WHAT WE UNCOVERED',2)}
   <ul style='font-family:{body_font};font-size:10.5pt;line-height:1.7;padding-{'right' if ar else 'left'}:5mm;margin:0'>{unc}</ul></div>
 <div style='margin-top:8mm'>{lab('توصياتي إلك','YOUR RECOMMENDATIONS')}{recs}</div>
 {foot(page)}
</div>"""
    page_b = f"""
<div class='a4' style='direction:{dirr}'>
 {head}
 <div style='margin-top:8mm;border-radius:6mm;padding:7mm 8mm;background:{C['mustard']};text-align:{ta}'>
   <div class='lab' style='font-size:8pt'>{L('هالأسبوع','THIS WEEK')}</div>
   <div style='font-family:{body_font};font-size:12pt;line-height:1.7;margin-top:1.5mm'>{esc(sec.get('this_week',''))}</div></div>
 <div style='margin-top:9mm'>{lab('أسئلة للدفتر','JOURNAL PROMPTS',4)}{jp}</div>
 <div style='position:absolute;left:18mm;right:18mm;bottom:26mm;border-radius:6mm;padding:7mm 8mm;background:{C['burgundy']};color:{C['cream']};text-align:{ta}'>
   <div class='lab' style='font-size:8pt;color:{C['mustard']}'>{L('الخطوة الجاية','NEXT STEP')}</div>
   <div style='font-family:{body_font};font-size:11.5pt;line-height:1.65;margin-top:1.5mm'>{esc(sec.get('next_step','')).replace(HANDLE, '<bdi>'+HANDLE+'</bdi>')}</div>
   <div class='disp {'' if ar else 'en'}' style='font-size:16pt;margin-top:3mm;color:{C['cream']}'>{L('اعرفي وين واقفة','Know where you stand')}</div></div>
 {foot(page + 1)}
</div>"""
    return page_a + page_b

def summary_html(spec):
    langs = spec.get("languages", ["ar", "en"])
    total = 2 * len(langs)
    secs = [summary_section(spec["sections"][l], l, spec.get("zone", "past"), spec.get("focus_skills", []),
                            spec.get("client_first_name", ""), spec.get("date", ""), 2 * i + 1, total)
            for i, l in enumerate(langs)]
    return a4_doc("".join(secs))

def sheet_html(spec):
    rows = ""
    for i, r in enumerate(spec.get("reels", [])):
        rows += (f"<div style='border-radius:5mm;background:rgba(107,29,37,.06);padding:5mm 6mm;margin-bottom:5mm;direction:rtl;text-align:right;page-break-inside:avoid'>"
                 f"<div class='lab' style='font-size:8pt;color:{C['burgundy']};direction:ltr;text-align:right'>REEL {i+1} · {esc(r.get('hook_type','')).upper()} · {esc(r.get('angle',''))}</div>"
                 f"<div class='disp' style='font-size:17pt;margin-top:1.5mm'>{esc(r.get('hook',''))}</div>"
                 f"<div style='font-family:Cairo;font-size:11pt;line-height:1.75;margin-top:2mm'>{esc(r.get('script','')).replace(chr(10),'<br>')}</div>"
                 f"<div style='font-family:Cairo;font-size:10pt;margin-top:2mm;color:{C['burgundy']}'><b>CTA:</b> {esc(r.get('cta',''))}</div>"
                 + (f"<div style='font:italic 9pt Figtree;margin-top:1.5mm;direction:ltr;text-align:left;opacity:.7'>{esc(r.get('takeaway_en',''))}</div>" if r.get('takeaway_en') else "")
                 + "</div>")
    body = (f"<div class='a4 flow'><div style='display:flex;justify-content:space-between;align-items:center;border-bottom:1.5px solid rgba(107,29,37,.25);padding-bottom:5mm;margin-bottom:6mm'>"
            f"{lockup(C['burgundy'])}<div class='lab' style='font-size:8pt;color:{C['burgundy']}'>SHOOTING SHEET · {esc(spec.get('date',''))}</div></div>{rows}</div>")
    return a4_doc(body, flow=True)

def a4_doc(body, flow=False):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{font_face()}{BASE}"
            f"@page{{size:A4;margin:{'16mm 18mm' if flow else '0'}}}"
            f"body{{background:{C['cream']};color:{C['ink']}}}"
            f".a4{{{'' if flow else 'width:210mm;height:297mm;padding:16mm 18mm;position:relative;overflow:hidden;page-break-after:always;'}background:{C['cream']}}}"
            f"</style></head><body>{body}</body></html>")

# ------------------------------------------------------------------ engines
FIT_JS = """
() => { for (const el of document.querySelectorAll('.fit')) {
  const mh = parseFloat(getComputedStyle(el).maxHeight); if (!mh) continue;
  el.style.maxHeight = 'none'; el.style.overflow = 'visible';
  let fs = parseFloat(getComputedStyle(el).fontSize), guard = 0;
  while (el.getBoundingClientRect().height > mh + 4 && fs > 18 && guard++ < 40) {
    fs *= 0.95; el.style.fontSize = fs + 'px'; } } }
"""

def wrap(pages_html, w, h):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{font_face()}{BASE}"
            f"@page{{size:{w}px {h}px;margin:0}} body{{margin:0}} .slide{{page-break-after:always}}</style></head>"
            f"<body>{''.join(pages_html)}</body></html>")

def have_playwright():
    if os.environ.get('NADINE_ENGINE') == 'weasy':
        return False
    try:
        import playwright.sync_api  # noqa
        return True
    except Exception:
        return False

def render_images(pages, w, h, out_dir, prefix):
    out_dir.mkdir(parents=True, exist_ok=True)
    files = []
    if have_playwright():
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            try:
                b = p.chromium.launch()
            except Exception:
                b = None
            if b:
                for i, ph in enumerate(pages, 1):
                    f = out_dir / f"_tmp_{prefix}_{i}.html"; f.write_text(wrap([ph], w, h), encoding="utf-8")
                    pg = b.new_page(viewport={"width": w, "height": h}); pg.goto(f.as_uri())
                    pg.wait_for_timeout(300); pg.evaluate(FIT_JS); pg.wait_for_timeout(100)
                    png = out_dir / f"{prefix}_{i:02d}.png"
                    pg.screenshot(path=str(png), clip={"x": 0, "y": 0, "width": w, "height": h}); pg.close(); f.unlink()
                    files.append(png)
                b.close()
                return files
    # fallback: WeasyPrint -> PDF -> PNG
    import weasyprint
    pdf = out_dir / f"_{prefix}.pdf"
    weasyprint.HTML(string=wrap(pages, w, h), base_url=str(HERE)).write_pdf(str(pdf))
    subprocess.run(["pdftoppm", "-png", "-r", "96", str(pdf), str(out_dir / f"{prefix}")], check=True)
    for i, f in enumerate(sorted(out_dir.glob(f"{prefix}-*.png")), 1):
        dst = out_dir / f"{prefix}_{i:02d}.png"; f.rename(dst); files.append(dst)
    pdf.unlink()
    return files

def render_pdf(doc_html, out_pdf):
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    if have_playwright():
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            try:
                b = p.chromium.launch()
                f = out_pdf.with_suffix(".html"); f.write_text(doc_html, encoding="utf-8")
                pg = b.new_page(); pg.goto(f.as_uri()); pg.wait_for_timeout(300)
                pg.pdf(path=str(out_pdf), prefer_css_page_size=True, print_background=True); b.close(); f.unlink()
                return out_pdf
            except Exception:
                pass
    import weasyprint
    weasyprint.HTML(string=doc_html, base_url=str(HERE)).write_pdf(str(out_pdf))
    return out_pdf

def contact_sheet(files, out, cols=4, tw=360):
    try:
        from PIL import Image
    except Exception:
        return None
    ims = [Image.open(f) for f in files]
    th = int(tw * ims[0].height / ims[0].width); rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 12, rows * th + (rows + 1) * 12), C["paper"])
    for i, im in enumerate(ims):
        sheet.paste(im.convert("RGB").resize((tw, th)), (12 + (i % cols) * (tw + 12), 12 + (i // cols) * (th + 12)))
    sheet.save(out); return out

# ------------------------------------------------------------------ QA
AR_LIMITS = dict(cover_title=45, statement=90, skill_body=160, quote=110, step=90, check=60, text_total=420)

def qa(spec):
    warn = []
    for i, s in enumerate(spec.get("slides", []), 1):
        L = s.get("layout")
        if L not in LAYOUTS: warn.append(f"slide {i}: unknown layout '{L}'")
        if L == "cover" and len(s.get("title", "")) > AR_LIMITS["cover_title"]: warn.append(f"slide {i}: cover title long ({len(s['title'])} chars)")
        if L == "quote" and len(s.get("text", "")) > AR_LIMITS["quote"]: warn.append(f"slide {i}: quote long")
        if L in ("steps", "checklist") and len(s.get("items", [])) > 5: warn.append(f"slide {i}: max 5 items; extra dropped")
        if L in ("text", "notebook") and sum(len(p) for p in s.get("paragraphs", [])) > AR_LIMITS["text_total"]: warn.append(f"slide {i}: text over {AR_LIMITS['text_total']} chars; split into two slides")
        for k in ("title", "text", "sub", "body"):
            v = s.get(k, "")
            if re.search(r"(علاج|شفاء|مضمون|guarantee|cure|therapy|reclaim your life)", str(v), re.I):
                warn.append(f"slide {i}: claims word found in '{k}' — check the claims rule")
    ct = spec.get("carousel")
    if ct and ct in CAROUSELS and spec.get("slides"):
        if spec["slides"][-1].get("layout") not in ("cta", "quote") and ct != "quote_drop":
            warn.append("last slide should be a CTA")
    return warn

# ------------------------------------------------------------------ main
def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return
    if a[0] == "--list":
        for k, v in CAROUSELS.items(): print(f"{k:16} {v['en']:18} {v['length']:4}  {v['trigger']}")
        return
    if a[0] == "--recipe":
        k = a[1]; r = CAROUSELS[k]
        print(json.dumps({"type": "carousel", "carousel": k, "zone": "past", "lang": "ar", "name": k,
                          "slides": [{"layout": L} for L in r["slides"]]}, ensure_ascii=False, indent=2)); return
    spec = json.loads(pathlib.Path(a[0]).read_text(encoding="utf-8"))
    out = pathlib.Path(a[1] if len(a) > 1 else "out").resolve(); out.mkdir(parents=True, exist_ok=True)
    typ = spec.get("type", "carousel"); zone = spec.get("zone", "neutral"); lang = spec.get("lang", "ar")
    name = spec.get("name", typ)
    if typ in ('carousel','post'):
        for w in qa(spec): print("QA:", w)
    if typ in ("carousel", "post"):
        slides = spec["slides"]; n = len(slides)
        pages = [slide_html(s, i, n, zone, lang, single=(typ == "post" or n == 1)) for i, s in enumerate(slides, 1)]
        files = render_images(pages, W, H, out, name)
        if len(files) > 1: contact_sheet(files, out / f"{name}_preview.png")
    elif typ == "reel_cover":
        files = render_images([reel_cover_html(spec, zone)], 1080, 1920, out, name)
    elif typ == "story":
        files = render_images([story_html(s, s.get("zone", zone)) for s in spec["slides"]], 1080, 1920, out, name)
    elif typ == "highlights":
        files = render_images([highlight_html(it) for it in spec["items"]], 1080, 1920, out, name)
    elif typ == "client_summary":
        files = [render_pdf(summary_html(spec), out / f"{name}.pdf")]
    elif typ == "shooting_sheet":
        files = [render_pdf(sheet_html(spec), out / f"{name}.pdf")]
    else:
        raise SystemExit(f"unknown type {typ}")
    for f in files: print("OUT:", f)

if __name__ == "__main__":
    main()
