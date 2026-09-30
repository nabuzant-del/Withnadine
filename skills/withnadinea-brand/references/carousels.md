# The 9 carousel types

Each type has a trigger, a length, a slide recipe, and rules. `python scripts/render.py --recipe <type>` prints a starter spec.

---

## 1. Story Arc · القصة · `story_arc` · 7 slides
**Trigger:** a full client journey with emotion and a turn (Repurposing Agent angle C). Source moment ≥ 150 words.
**Recipe:** cover → text (context) → statement (tension) → text (emotion) → statement (realization) → skill (insight) → cta
**Rules:** the client is the character, not Nadine. The realization slide is the peak; highlight the turning word. Context slide ≤ 2 short paragraphs.

## 2. Belief Shift · كانت فاكرة… طلع · `belief_shift` · 5 slides
**Trigger:** a clear "what she thought vs what was actually happening".
**Recipe:** cover → compare → compare → statement → cta
**Rules:** each compare slide is one pair. Top card = her belief (muted), bottom card = what it was (bold). Keep each side ≤ 12 words.

## 3. Skill Spotlight · مهارة · `skill_spotlight` · 5 slides
**Trigger:** the lesson is one named skill.
**Recipe:** cover → skill → text (what it looks like in life) → steps (try it, 3 items) → cta
**Rules:** set `skill` to the number; zone follows the skill (1–2 past, 3–4 present, 5–6 future). The CTA closer says "هاي المهارة N من ٦".

## 4. Diagnostic · إذا هاد عم يصير معك · `diagnostic` · 5 slides
**Trigger:** 3–5 recognisable symptoms / "if this keeps happening to you".
**Recipe:** cover → checklist → statement (why it happens) → skill → cta
**Rules:** checklist items are behaviours she'd recognise, ≤ 10 words each, written as she'd say them. Never diagnose; describe.

## 5. Coach's Notebook · دفتر نادين · `notebook` · 3–5 slides
**Trigger:** Nadine's own view or philosophy (angle A/B), reflective, 120–300 words.
**Recipe:** statement (opening line, `theme: cream`) → notebook (1–3) → cta
**Rules:** first person, calm, no headline on notebook slides. Mustard glow background. Up to 420 characters per notebook slide.

## 6. Quote Drop · جملة · `quote_drop` · 1–3 slides
**Trigger:** one strong line ≤ 25 words that stands alone.
**Recipe:** quote (× 1–3)
**Rules:** night background only. Arabic line, then the English line in caps (`en`). No CTA slide; the caption carries the CTA. Use line breaks (`\n`) to shape the quote into 2–3 balanced lines.

## 7. Zone Map · خريطة الأزمنة · `zone_map` · 6 slides
**Trigger:** a situation read across past, present and future.
**Recipe:** cover (`zone: neutral`) → zonemap → text (`theme: past`) → text (`theme: present`) → text (`theme: future`) → cta
**Rules:** each zone text slide uses its zone theme and a `title` of the zone name. `focus` on the zonemap = the zone the source content is mostly about.

## 8. Micro Case · حالة قصيرة · `micro_case` · 4 slides
**Trigger:** a short transformation, source moment < 120 words.
**Recipe:** cover → compare (before / after) → statement (insight) → cta
**Rules:** labels can be overridden: `label_a: "قبل"`, `label_b: "بعد"`.

## 9. Try This · جرّبي هيك · `try_this` · 4–6 slides
**Trigger:** an exercise with 3–6 concrete steps.
**Recipe:** cover → steps (1–3) → steps (4–6, `start: 4`) → statement → cta
**Rules:** every step starts with a verb. If only 3 steps, drop the second steps slide.

---

## Layout fields

| Layout | Fields | Default theme |
|---|---|---|
| `cover` | `title`, `sub`, `hl` (word in sub), `hl_title`, `kicker` [en, ar] | cream + zone shapes |
| `statement` | `text`, `hl`, `en` | zone colour |
| `text` | `paragraphs` [1–3], `title` (optional), `hl` | cream |
| `notebook` | `paragraphs`, `hl` | present (mustard glow) |
| `skill` | `skill` (1–6), `title` (optional; defaults to the skill name), `body`, `hl` | zone colour |
| `quote` | `text` (use `\n`), `en` | night |
| `steps` | `title`, `items` [≤5], `start` | cream |
| `compare` | `a`, `b`, `label_a`, `label_b` | cream |
| `checklist` | `title`, `items` [≤5] | zone colour |
| `zonemap` | `title`, `zones` {past, present, future}, `focus` | cream |
| `cta` | `cta_kind` (method/book), `closer`, `text`, `sub` | burgundy |
| `photo` | `image` (path), `title`, `sub`, `hl` | image + tint |

Every slide also accepts `theme`, `zone`, and `lang` ("ar" default, "en" for an English slide).

## Length rules (checked by the renderer's QA)
- Cover title ≤ 45 characters · statement ≤ 90 · quote ≤ 110 · step/checklist item ≤ 90 / 60 · text slide ≤ 420 total.
- Over the limit? Cut words or split the slide. Don't reduce type size by hand.
