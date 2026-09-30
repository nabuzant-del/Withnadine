#!/usr/bin/env python3
"""Check and render Nadine's bilingual client summary PDF.

usage: build_summary.py summary.json OUT_DIR [--iso YYYY-MM-DD] [--file-name Reem] [--private TERM ...] [--check-only]

Rendering is delegated to the withnadinea-brand skill (client_summary type).
"""
import argparse, datetime, json, pathlib, re, shutil, sys, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _brand import render

BANNED = re.compile(
    r"(علاج|شفاء|يشفي|مضمون|نضمن|تشخيص|اكتئاب|اضطراب|صدمة نفسية|دواء|أدوية|حبوب|فتوى|حرام|"
    r"therap|\bcure|\bheal|guarantee|diagnos|depress|disorder|\bADHD\b|trauma|medication|reclaim your life|"
    r"in \d+ days|خلال \d+ (يوم|أيام|أسبوع)|\bleave him\b|cut (him|her|them) off|اتركيه|قاطعي)", re.I)


def texts(o):
    if isinstance(o, str): yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k != "skill": yield from texts(v)
    elif isinstance(o, list):
        for v in o: yield from texts(v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("out")
    ap.add_argument("--iso", default=str(datetime.date.today()))
    ap.add_argument("--file-name"); ap.add_argument("--private", action="append", default=[])
    ap.add_argument("--check-only", action="store_true")
    a = ap.parse_args()
    spec = json.loads(pathlib.Path(a.spec).read_text(encoding="utf-8"))
    E, W = [], []

    name = spec.get("client_first_name", "").strip()
    if not name: E.append("client_first_name is missing")
    elif len(name.split()) > 1 or "@" in name: E.append(f"client_first_name '{name}': first name only")
    langs = spec.get("languages", [])
    if sorted(langs) != ["ar", "en"]: E.append("languages must be ['ar','en'] or ['en','ar'] (her language first)")
    if spec.get("zone") not in ("past", "present", "future"): E.append("zone must be past, present or future")
    fs = spec.get("focus_skills", [])
    if not fs or any(s not in range(1, 7) for s in fs): E.append("focus_skills: 1–3 numbers from 1 to 6")
    elif len(fs) > 3: W.append("focus_skills: more than 3 dilutes the summary")

    secs = spec.get("sections", {})
    for L in ("ar", "en"):
        s = secs.get(L)
        if not s: E.append(f"sections.{L} is missing"); continue
        ws = s.get("where_you_stand", {})
        if not ws.get("title") or not ws.get("body"): E.append(f"{L}: where_you_stand needs title and body")
        if not 3 <= len(s.get("uncovered", [])) <= 4: E.append(f"{L}: uncovered needs 3–4 items")
        recs = s.get("recommendations", [])
        if len(recs) != 3: E.append(f"{L}: exactly 3 recommendations")
        for i, r in enumerate(recs, 1):
            if r.get("skill") not in range(1, 7): E.append(f"{L}: recommendation {i} needs a skill number 1–6")
            elif fs and r["skill"] not in fs: W.append(f"{L}: recommendation {i} uses skill {r['skill']}, not in focus_skills")
        if len(s.get("journal_prompts", [])) != 3: E.append(f"{L}: exactly 3 journal prompts")
        for k in ("this_week", "next_step"):
            if not s.get(k): E.append(f"{L}: {k} is missing")
        for u in s.get("uncovered", []):
            if len(u.split()) > 22: W.append(f"{L}: an uncovered item is long ({len(u.split())} words)")
    if secs.get("ar") and secs.get("en"):
        ra = [r.get("skill") for r in secs["ar"].get("recommendations", [])]
        re_ = [r.get("skill") for r in secs["en"].get("recommendations", [])]
        if ra != re_: W.append("ar and en recommendations point to different skills")

    alltext = list(texts({k: v for k, v in spec.items() if k not in ("languages", "zone", "type", "name")}))
    for t in alltext:
        m = BANNED.search(t)
        if m: E.append(f"banned word in the PDF: '{m.group(0)}' — rewrite")
        for p in a.private:
            if p.strip() and p.strip().lower() in t.lower():
                E.append(f"private term '{p}' appears in the PDF")

    for w in dict.fromkeys(W): print("WARN:", w)
    for e in dict.fromkeys(E): print("ERROR:", e)
    if E: sys.exit("BLOCKED: fix the errors above, then run again.")
    if a.check_only: print("CHECKS PASSED"); return

    fname = re.sub(r"[^\w\-]+", "", (a.file_name or name)) or "Client"
    stem = f"{fname}_Summary_{a.iso}"
    spec = dict(spec, type="client_summary", name=stem)
    out = pathlib.Path(a.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path(tempfile.mkdtemp()) / "summary.json"
    tmp.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    for line in render(tmp, out).splitlines():
        if line.startswith(("QA:", "OUT:")): print(line)
    print("DONE")


if __name__ == "__main__":
    main()
