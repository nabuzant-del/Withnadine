# The content pack (`pack.json`)

One file holds everything from one session (or one week). `scripts/build_pack.py` checks it and renders it through `withnadinea-brand`.

## 1. Shape
```json
{
  "date": "2026-09-22",
  "name": "week_2026_09_22",
  "safety": {"consent": true, "care_flag": false, "composite": true},
  "reels": [
    {"angle": "Client story", "perspective": "Client", "hook_type": "Story",
     "hook": "…", "script": "line\nline\nline", "cta": "method",
     "takeaway_en": "…", "on_screen": ["…", "…"],
     "zone": "past", "cover": {"line1": "…", "line2": "…"}}
  ],
  "carousels": [
    {"title": "internal title", "perspective": "Client",
     "caption": "Arabic lines…\nEnglish line\nاعرفي أكتر عن الطريقة — الرابط بالبايو\n#… #…",
     "image_prompts": ["slide 1: …"],
     "spec": {"type": "carousel", "carousel": "belief_shift", "zone": "present", "lang": "ar", "slides": [ … ]}}
  ]
}
```
- `cta`: `"method"` or `"book"` (the script adds the full Arabic line).
- `script`: one spoken breath per line, 55–85 words, CTA not included.
- `cover`: optional. Reel covers render for every reel that has one; give one per selected angle (usually the stronger script).
- `spec`: a normal brand carousel spec (see `withnadinea-brand/references/carousels.md`). `name` is filled in for you.
- Only the **top 3** carousels go in `carousels`. The rest of the carousel bank stays in Part 2 text.

## 2. Command
```bash
python scripts/build_pack.py pack.json out/ --transcript transcript.txt --client "Reem" --client "ريم"
```
- `--transcript`: the transcript saved as text, one `Speaker: words` per line (Fireflies `[00:05 - 00:08] Speaker: text` also works).
- `--client`: the client's speaker label and every name she or others are called by (repeat the flag). Used to find her lines and to catch name leaks.
- `--nadine "Nadine"`: Nadine's speaker label if it is not "Nadine".
- `--check-only`: run the checks, render nothing.

**Blocking errors** (nothing renders until fixed): consent false · care flag true · a 9+ word run copied from the client's lines · a client name in any copy · a CTA not in the two allowed · no carousel CTA slide.
**Warnings** (fix, then re-run): reel outside 55–85 words · claims or diagnosis words · long cover/statement · fewer than 6 reels.

Output in `out/`: `shooting_sheet.pdf` · `reel_cover_01.png…` · `<carousel>_01.png…` + `_preview.png` per carousel · `captions.txt` · `image_prompts.txt`.

## 3. Agent storyboard → carousel type
Pick the type with the brand selector (first match wins). Then map the agent's slides onto the recipe:

| Agent slide | story_arc | belief_shift | micro_case | diagnostic | zone_map |
|---|---|---|---|---|---|
| 1 Cover | cover | cover | cover | cover | cover |
| 2 Context | text | — | compare (before) | checklist | zonemap |
| 3 Tension | statement | compare (thought) | compare (before) | checklist | text past |
| 4 Emotional consequence | text | — | — | — | text present |
| 5 Realization | statement (hl the turn) | compare (actually) | compare (after) | statement | text future |
| 6 Insight / method | skill | statement | statement | skill | — |
| 7 Takeaway | cta closer | cta closer | cta closer | cta closer | cta closer |

`skill_spotlight`, `try_this`, `notebook` and `quote_drop` are Coach POV / philosophy formats: build them straight from the recipe, not from the 7 slides.

Give the three carousels three different types where the content allows, and at least one Client and one Coach perspective.
