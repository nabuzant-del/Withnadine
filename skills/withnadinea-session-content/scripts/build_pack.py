#!/usr/bin/env python3
"""Check and render a @withnadinea content pack.

usage: build_pack.py pack.json OUT_DIR [--transcript t.txt] [--client NAME ...] [--nadine NAME] [--check-only]

Blocking errors stop the render. Warnings print as WARN: and should be fixed, then re-run.
Rendering is delegated to the withnadinea-brand skill (scripts/render.py).
"""
import argparse, datetime, json, pathlib, re, sys, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _brand import render

CTA_LINES = {
    "method": "اعرفي أكتر عن الطريقة — الرابط بالبايو",
    "book": "احجزي جلسة معي — الرابط بالبايو",
}
CLAIMS = re.compile(
    r"(علاج|شفاء|يشفي|بتشفي|مضمون|نضمن|تشخيص|اكتئاب|اضطراب|صدمة نفسية|دواء|أدوية|حبوب|فتوى|"
    r"therap|\bcure|\bheal|guarantee|diagnos|depress|disorder|\bADHD\b|trauma|medication|reclaim your life|"
    r"in \d+ days|خلال \d+ يوم|بـ?\d+ يوم)", re.I)
N = 9  # a run of 9+ words copied from the client = a quote over 8 words

AR_NORM = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ة": "ه", "ى": "ي", "ؤ": "و", "ئ": "ي", "ـ": None})


def norm_tokens(s):
    s = re.sub(r"[ً-ْٰ]", "", s or "").translate(AR_NORM).lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return [t for t in s.split() if t]


def parse_transcript(path, clients, nadine):
    lines = []
    for raw in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        raw = re.sub(r"^\s*\[[^\]]*\]\s*", "", raw)
        m = re.match(r"^\s*([^:：]{1,60})[:：]\s*(.+)$", raw)
        if m:
            lines.append((m.group(1).strip(), m.group(2).strip()))
    if not lines:
        return []
    cl = {c.lower() for c in clients}
    mine = [t for sp, t in lines if sp.lower() in cl]
    if not mine:  # fall back: everyone who isn't Nadine or a bot
        mine = [t for sp, t in lines if nadine.lower() not in sp.lower() and "fireflies" not in sp.lower()]
    return mine


def ngrams(tokens, n=N):
    return {tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)}


def all_text(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k not in ("image_prompts", "layout", "carousel", "type", "zone", "theme", "cta_kind", "lang", "name"):
                yield from all_text(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from all_text(v)


def nice_date(d):
    try:
        return datetime.date.fromisoformat(d).strftime("%-d %b %Y")
    except Exception:
        return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pack"); ap.add_argument("out")
    ap.add_argument("--transcript"); ap.add_argument("--client", action="append", default=[])
    ap.add_argument("--nadine", default="Nadine"); ap.add_argument("--check-only", action="store_true")
    a = ap.parse_args()

    pack = json.loads(pathlib.Path(a.pack).read_text(encoding="utf-8"))
    errors, warns = [], []
    saf = pack.get("safety", {})
    if saf.get("consent") is not True:
        errors.append("safety.consent is not true: no content from a session without clear consent")
    if saf.get("care_flag"):
        errors.append("safety.care_flag is true: no content from this session")

    reels, cars = pack.get("reels", []), pack.get("carousels", [])
    if len(reels) < 6: warns.append(f"{len(reels)} reel scripts; the agent asks for 6–8 (3–4 angles × 2)")
    if len(cars) != 3: warns.append(f"{len(cars)} carousels; render the top 3")

    for i, r in enumerate(reels, 1):
        w = len(norm_tokens(r.get("script", "")))
        if not 55 <= w <= 85: warns.append(f"reel {i}: {w} spoken words (target 55–85)")
        if r.get("cta") not in CTA_LINES: errors.append(f"reel {i}: cta must be 'method' or 'book'")
        if not r.get("takeaway_en"): warns.append(f"reel {i}: missing takeaway_en")
        cv = r.get("cover")
        if cv:
            if len(cv.get("line1", "")) > 44: warns.append(f"reel {i} cover: line1 over 44 chars")
            if len(cv.get("line2", "")) > 28: warns.append(f"reel {i} cover: line2 over 28 chars")
    kinds = [r.get("cta") for r in reels]
    if reels and (kinds.count("method") == 0 or kinds.count("book") == 0):
        warns.append("CTAs don't rotate: use both 'method' and 'book'")

    types = []
    for i, c in enumerate(cars, 1):
        s = c.get("spec", {}); types.append(s.get("carousel"))
        sl = s.get("slides", [])
        if s.get("carousel") != "quote_drop" and (not sl or sl[-1].get("layout") != "cta"):
            errors.append(f"carousel {i}: must end with a cta slide")
        if not c.get("caption"): warns.append(f"carousel {i}: missing caption")
        elif not any(x.split(" — ")[0] in c["caption"] for x in CTA_LINES.values()):
            warns.append(f"carousel {i}: caption has no CTA line")
    if len(types) != len(set(types)): warns.append("two carousels share a type; vary them if the content allows")

    # copy checks across everything that will be published
    texts = []
    for i, r in enumerate(reels, 1): texts += [(f"reel {i}", t) for t in all_text(r)]
    for i, c in enumerate(cars, 1): texts += [(f"carousel {i}", t) for t in all_text({k: v for k, v in c.items() if k != "image_prompts"})]
    for where, t in texts:
        m = CLAIMS.search(t)
        if m: warns.append(f"{where}: claims/diagnosis word '{m.group(0)}' — rewrite")
        for name in a.client:
            if len(name) >= 2 and re.search(rf"(?<!\w){re.escape(name)}(?!\w)", t, re.I):
                errors.append(f"{where}: client name '{name}' appears in the copy")
    if a.transcript:
        client_lines = parse_transcript(a.transcript, a.client, a.nadine)
        if not client_lines: warns.append("could not find client lines in the transcript; quote check skipped")
        grams = set().union(*(ngrams(norm_tokens(l)) for l in client_lines)) if client_lines else set()
        for where, t in texts:
            hit = ngrams(norm_tokens(t)) & grams
            if hit:
                errors.append(f"{where}: copies {N}+ words from the client: «{' '.join(next(iter(hit)))}…» — paraphrase")
    else:
        warns.append("no --transcript given; the 8-word quote check did not run")

    for w in dict.fromkeys(warns): print("WARN:", w)
    for e in dict.fromkeys(errors): print("ERROR:", e)
    if errors:
        sys.exit("BLOCKED: fix the errors above, then run again.")
    if a.check_only:
        print("CHECKS PASSED"); return

    out = pathlib.Path(a.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path(tempfile.mkdtemp())
    date = pack.get("date", str(datetime.date.today()))

    def go(spec, fname):
        p = tmp / f"{fname}.json"; p.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
        for line in render(p, out).splitlines():
            if line.startswith(("QA:", "OUT:")): print(line)

    if reels:
        go({"type": "shooting_sheet", "name": "shooting_sheet", "date": nice_date(date),
            "reels": [{"angle": r.get("angle", ""), "hook_type": r.get("hook_type", ""), "hook": r.get("hook", ""),
                       "script": r.get("script", ""), "cta": CTA_LINES[r["cta"]], "takeaway_en": r.get("takeaway_en", "")}
                      for r in reels]}, "shooting_sheet")
        for n, r in enumerate(reels, 1):
            if r.get("cover"):
                go({"type": "reel_cover", "name": f"reel{n}_cover", "zone": r.get("zone", "neutral"), **r["cover"]},
                   f"reel{n}_cover")
    for i, c in enumerate(cars, 1):
        spec = dict(c["spec"]); spec["type"] = "carousel"
        spec["name"] = f"carousel{i}_{spec.get('carousel', 'x')}"
        go(spec, spec["name"])

    # text companions
    rl = []
    for i, r in enumerate(reels, 1):
        rl += [f"REEL {i} · {r.get('angle', '')} · {r.get('hook_type', '')}",
               f"Hook: {r.get('hook', '')}", r.get("script", ""), CTA_LINES[r["cta"]],
               f"On screen: {' | '.join(r.get('on_screen', []))}", f"EN: {r.get('takeaway_en', '')}", ""]
    (out / "reels.txt").write_text("\n".join(rl), encoding="utf-8")
    (out / "captions.txt").write_text("\n\n".join(
        f"CAROUSEL {i} · {c['spec'].get('carousel')} · {c.get('title', '')}\n{c.get('caption', '')}" for i, c in enumerate(cars, 1)),
        encoding="utf-8")
    (out / "image_prompts.txt").write_text("\n\n".join(
        f"CAROUSEL {i} · {c.get('title', '')}\n" + "\n".join(c.get("image_prompts", [])) for i, c in enumerate(cars, 1)),
        encoding="utf-8")
    print("OUT:", out / "reels.txt"); print("OUT:", out / "captions.txt"); print("OUT:", out / "image_prompts.txt")
    print("DONE")


if __name__ == "__main__":
    main()
