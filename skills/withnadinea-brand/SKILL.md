---
name: withnadinea-brand
description: Nadine's (@withnadinea, مع نادين) brand system and asset engine. Use for ANY visual or written asset for Nadine — Instagram carousels (9 types), single posts, quote cards, reel covers/thumbnails, stories, highlight covers, the bilingual client session summary PDF, the reel shooting sheet PDF, and image-generation prompts. Also use to check copy against her voice and claims rules. Triggers: "carousel for Nadine", "كاروسيل", "post", "reel cover", "thumbnail", "story", "highlight", "client summary", "shooting sheet", "brand", "make it on brand". Always render through scripts/render.py — never hand-draw layouts.
---

# @withnadinea — Brand System + Asset Engine

Brand: **مع نادين · With Nadine** · handle **@withnadinea** · line **اعرفي وين واقفة / Know where you stand**
Method: The Three Time Zones (past · present · future) and six numbered skills.
Fonts: **Lalezar** (primary, Arabic display) · **Cairo** (secondary, Arabic body and subtitles) · **Figtree** (Latin). TTF used for rendering; OTF copies in `assets/fonts/otf/` for design apps.
No slide counters or page numbers on carousels — Instagram already shows position.

Everything you make goes through `scripts/render.py` with a JSON spec. The renderer owns colours, fonts, grain, safe areas and the logo, so every asset stays on brand. You write the words and pick the layout; the engine does the design.

## 0. Before anything
1. Read `references/voice.md` (language, dialect, claims, safety). Non-negotiable.
2. For carousels, read `references/carousels.md` and pick the type with the selector in §2.
3. For anything else, read `references/formats.md`.
4. `references/brand.md` holds the tokens and do/don't rules if you need to explain or check a choice.

## 1. Render
```bash
python scripts/render.py spec.json out/                 # render
python scripts/render.py --list                         # the 9 carousel types
python scripts/render.py --recipe story_arc > spec.json # starter spec for a type
```
- Engine: Playwright/Chromium if present (auto-shrinks overflowing text), otherwise WeasyPrint + pdftoppm. Both use the bundled fonts in `assets/fonts`. If neither is installed: `pip install weasyprint` (and `apt-get install poppler-utils` if pdftoppm is missing).
- Output: PNG per slide (`name_01.png …`), a `name_preview.png` contact sheet for carousels, PDFs for documents.
- The script prints `QA:` warnings (length, claims words, missing CTA). Fix every warning and re-render before delivering.
- Look at the preview image before delivering. If any text is cramped, shorten the words — never shrink the design.
- Worked examples of every format live in `examples/` (01–15). Copy the closest one.

## 2. Carousel selector — pick exactly one type
Go down the list; the first rule that matches wins.

| # | If the content is… | Type | Slides |
|---|---|---|---|
| 1 | one line ≤ 25 words that stands alone | `quote_drop` | 1–3 |
| 2 | an exercise with 3–6 concrete steps | `try_this` | 4–6 |
| 3 | 3–5 recognisable symptoms ("if this keeps happening…") | `diagnostic` | 5 |
| 4 | a clear "she thought X, it was actually Y" | `belief_shift` | 5 |
| 5 | the lesson is one named skill (1–6) | `skill_spotlight` | 5 |
| 6 | a situation read across past, present and future | `zone_map` | 6 |
| 7 | a full client journey with emotion and a turn, source ≥ 150 words | `story_arc` | 7 |
| 8 | a short transformation, source < 120 words | `micro_case` | 4 |
| 9 | Nadine's own view / philosophy, reflective, 120–300 words | `notebook` | 3–5 |

Zone: set `"zone"` to the time zone the content is about (`past` / `present` / `future`; `neutral` for the whole method). The zone drives the colour and the shape — never pick a colour by taste.

## 3. Spec format (carousel)
```json
{"type":"carousel","carousel":"belief_shift","zone":"present","lang":"ar","name":"belief_shift_2026_09_22",
 "slides":[
  {"layout":"cover","title":"مش تعبانة. غايبة.","sub":"…","hl":"word to highlight"},
  {"layout":"compare","a":"what she thought","b":"what it actually was"},
  {"layout":"statement","text":"…","hl":"…","en":"optional English line"},
  {"layout":"cta","cta_kind":"book","closer":"هاي المهارة ٤ من ٦."}]}
```
Layouts: `cover · statement · text · notebook · skill · quote · steps · compare · checklist · zonemap · cta · photo`. Fields per layout are in `references/carousels.md`. Any slide can override `theme` (`cream · past · present · future · night · burgundy`) or `zone`, but only when the carousel type calls for it.

Other types: `post` (one slide) · `reel_cover` · `story` · `highlights` · `client_summary` · `shooting_sheet` — see `references/formats.md`.

## 4. Hard rules (the renderer enforces the visual ones; you enforce the words)
- Arabic first, flat Levantine, feminine address. English is secondary: a short caps line under a quote or statement, or a full English version only when asked.
- One idea per slide. Cover title ≤ 45 characters. Statement ≤ 90. Text slide ≤ 420 characters total — split otherwise.
- Every carousel ends with a `cta` slide (except `quote_drop`). CTA is one of two: `method` (اعرفي أكتر عن الطريقة) or `book` (احجزي جلسة معي). Both say "link in bio" and show @withnadinea.
- Skill references by number: "المهارة ٢ من ٦". Name the skill; never teach the full method.
- Client content: anonymised composites only, no quote over 8 words, nothing from a non-consenting or care-flagged session.
- No claims: therapy, cure, guaranteed, timelines, "reclaim your life".

## 5. Images
Phase 1 carousels are typographic + shapes (no photos needed). When a slide calls for an image, write an image-generation prompt with the recipe in `references/formats.md` §Images, and if Nadine supplies a photo, use the `photo` layout (it applies the brand tint and grain). Never place generated text inside images.

## 6. Companion skills
`withnadinea-session-content` (Fireflies transcript → reels + carousels) and `withnadinea-session-summary` (Fireflies + Gmail → client PDF + private notes) write the words and call this renderer. Keep all three installed together.

## 7. Delivering
Give Nadine: the PNGs (numbered in posting order), the caption (Arabic, one English line, 5–8 hashtags), and the preview image. For PDFs: the file, named `ClientFirstName_Summary_YYYY-MM-DD.pdf`.
